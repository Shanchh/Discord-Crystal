import discord
from discord import app_commands

from discord_bot import bot
from common.basic import is_owner
import common.monthly as monthly
import discord_embed.basic_embed as bm
import discord_embed.monthly_embed as mm

MONTHLY_ROLE_ID = 969780381391929345

adminmonthly_group = app_commands.Group(name="adminmonthly", description="管理月度訂閱")

@is_owner()
@adminmonthly_group.command(name="adduser", description="新增訂閱者")
@app_commands.describe(member = "@使用者")
async def adduser(interaction: discord.Interaction, member:discord.Member):
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    s = monthly.add_subscriber_user(member.id, member.name, avatar_url)
    embed = bm.basic("新增訂閱者", "你已成功新增一名訂閱者", 0x00ff11) if s else bm.request_error("新增訂閱者")
    await interaction.response.send_message(embed = embed)

@is_owner()
@adminmonthly_group.command(name="adddetail", description="新增訂閱明細")
@app_commands.describe(member = "@使用者", purchase_date = "購買日期", quantity = "數量", payment = "付款方式", amount = "金額")
async def adddetail(interaction: discord.Interaction, member: discord.Member, purchase_date: str, quantity: int, payment: str, amount: int):
    userId = member.id
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    s, dataId = monthly.add_subscriber_detail(userId, member.name, avatar_url, purchase_date, quantity, payment, amount)
    embed = bm.basic("新增訂閱明細", f"你已成功新增一條明細,ID:{dataId}", 0x00ff11) if s else bm.request_error("新增訂閱明細")
    await interaction.response.send_message(embed = embed)
    active, _ = monthly.check_subscriber_state(userId)
    if active:
        try:
            guild = interaction.guild
            role = guild.get_role(MONTHLY_ROLE_ID)
            await member.add_roles(role)
            await interaction.followup.send(embed = bm.basic("添加身分組", "執行成功", 0x00ff11))
        except discord.HTTPException as e:
            await interaction.followup.send(embed = bm.request_error(f"添加角色時發生錯誤: {e}", ephemeral=True))

@is_owner()
@adminmonthly_group.command(name="deluser", description="刪除訂閱者")
@app_commands.describe(member="@使用者")
async def deluser(interaction: discord.Interaction, member:discord.Member):
    s = monthly.del_subscriber_user(member.id)
    if s == None:
        embed = bm.basic("刪除訂閱者", "查無此訂閱者", 0xffa82e)
    else:
        embed = bm.basic("刪除訂閱者", "你已成功刪除一位訂閱者", 0x00ff11) if s else bm.request_error("刪除訂閱者")
    await interaction.response.send_message(embed = embed)

@is_owner()
@adminmonthly_group.command(name="deldatail", description="刪除訂閱明細")
@app_commands.describe(dataid="識別號碼")
async def deldetail(interaction: discord.Interaction, dataid: str):
    s = monthly.del_subscriber_detail(dataid)
    if s == None:
        embed = bm.basic("刪除訂閱明細", "查無此訂閱明細", 0xffa82e)
    else:
        embed = bm.basic("刪除訂閱明細", "你已成功刪除一條訂閱明細", 0x00ff11) if s else bm.request_error("刪除訂閱明細")
    await interaction.response.send_message(embed = embed)

@is_owner()
@adminmonthly_group.command(name="listdetails", description="列出所有訂閱明細")
@app_commands.describe()
async def listalldetails(interaction: discord.Interaction):
    channel = interaction.channel
    await interaction.response.send_message(embed=bm.basic("列出所有訂閱明細", "已收到請求！", 0x00ff11))
    all_details = monthly.get_all_detail_lists()
    for i in range(0, len(all_details), 5):
        embed = await mm.listDetail_embed(bot, all_details[i:i+5], i)
        await channel.send(embed = embed)

@is_owner()
@adminmonthly_group.command(name="active", description="列出所有活躍者")
@app_commands.describe()
async def listactive(interaction: discord.Interaction):
    await interaction.response.send_message(embed=bm.basic("列出所有訂閱明細", "已收到請求！", 0x00ff11))
    result = monthly.get_active_user()
    await interaction.channel.send(embed = mm.active_result(len(result), interaction.guild.icon.url))
    for count, active in enumerate(result):
        user = await interaction.client.fetch_user(active["userId"])
        avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
        await interaction.channel.send(embed = mm.active_user(count, user.mention, active["dateDeadLine"].strftime("%Y-%m-%d"), avatar_url))

@is_owner()
@adminmonthly_group.command(name="checkexisting", description="核實身分組存在狀況")
@app_commands.describe()
async def check_existing(interaction: discord.Interaction):
    await interaction.response.send_message(embed=bm.basic("核實身分組存在狀況", "已收到請求！", 0x00ff11))
    guild = interaction.guild
    channel = interaction.channel
    role = guild.get_role(MONTHLY_ROLE_ID)
    
    # 檢查持有身分組的用戶
    members_with_role = role.members
    for member in members_with_role:
        active, dead_line = monthly.check_subscriber_state(member.id)
        if not active:
            await member.remove_roles(role)
            await channel.send(embed = bm.basic("刪除過期訂閱者", f"用戶: {member.mention}\n到期時間: {dead_line}", 0xe63333))

    # 檢查活躍中缺失身分組的用戶
    active_members = monthly.get_active_user()
    for member in active_members:
        member = guild.get_member(member["userId"])
        if member and role not in member.roles:
            await member.add_roles(role)
            await channel.send(embed = bm.basic("添加缺失身分組", f"已為活躍用戶 {member.mention} 添加角色 '{role.name}'\n到期日: {member['dateDeadLine']}", 0x00ff11))

    await channel.send(embed = bm.basic("核實身分組存在狀況", "執行完畢！", 0x00ff11))

@is_owner()
@adminmonthly_group.command(name="statistics", description="總計月數金額")
@app_commands.describe()
async def statistics(interaction: discord.Interaction):
    total_amount, total_quantity = monthly.get_statistics()
    await interaction.response.send_message(embed = mm.statistics(total_quantity, total_amount, interaction.guild.icon.url), ephemeral=True)

@is_owner()
@adminmonthly_group.command(name="userdetails", description="查詢單一訂閱者的詳細訂閱資訊")
@app_commands.describe(member="@使用者")
async def userdetails(interaction: discord.Interaction, member: discord.Member):
    user_details = monthly.list_subscriber_details(member.id)
    if not user_details:
        embed = bm.basic("查詢訂閱者明細", "該用戶無任何訂閱資料", 0xffa82e)
        await interaction.response.send_message(embed = embed)
        return
    
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    for count, detail in enumerate(user_details):
        await interaction.channel.send(embed=mm.getDetail_info(count, detail, avatar_url))
    await interaction.response.send_message(embed=bm.basic("查詢訂閱者明細", f"已列出 {member.mention} 的所有訂閱明細！", 0x00ff11))