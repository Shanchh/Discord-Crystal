import discord
from discord import app_commands

from discord_bot import bot
from common.basic import is_owner
import common.monthly as monthly
import discord_embed.basic_embed as bm
import discord_embed.monthly_embed as mm

adminmonthly_group = app_commands.Group(name="adminmonthly", description="管理月度訂閱")

@is_owner()
@adminmonthly_group.command(name="adduser", description="新增訂閱者")
@app_commands.describe(member = "@使用者")
async def adduser(interaction: discord.Interaction, member:discord.Member):
    s = monthly.add_subscriber_user(member.id, member.name)
    embed = bm.basic("新增訂閱者", "你已成功新增一名訂閱者", 0x00ff11) if s else bm.request_error("新增訂閱者")
    await interaction.response.send_message(embed = embed)

@is_owner()
@adminmonthly_group.command(name="adddetail", description="新增訂閱明細")
@app_commands.describe(member = "@使用者", purchase_date = "購買日期", quantity = "數量", payment = "付款方式", amount = "金額")
async def adddetail(interaction: discord.Interaction, member: discord.Member, purchase_date: str, quantity: int, payment: str, amount: int):
    s, dataId = monthly.add_subscriber_detail(member.id, member.name, purchase_date, quantity, payment, amount)
    embed = bm.basic("新增訂閱明細", f"你已成功新增一條明細,ID:{dataId}", 0x00ff11) if s else bm.request_error("新增訂閱明細")
    await interaction.response.send_message(embed = embed)

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
    result = []
    userList = monthly.get_all_subscriber_user()
    for user in userList:
        userId = user["discord_id"]
        isActive, dateDeadLine = monthly.check_subscriber_state(userId)
        if isActive:
            result.append({
                "userId": userId,
                "dateDeadLine": dateDeadLine
            })
    await interaction.channel.send(embed = mm.active_result(len(result), len(userList) - len(result), interaction.guild.icon.url))
    for count, active in enumerate(result):
        user = await interaction.client.fetch_user(active["userId"])
        avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
        await interaction.channel.send(embed = mm.active_user(count, user.mention, active["dateDeadLine"].strftime("%Y-%m-%d"), avatar_url))

@is_owner()
@adminmonthly_group.command(name="checkexisting", description="核實身分組存在狀況")
@app_commands.describe()
async def check_existing(interaction: discord.Interaction, role: discord.Role):
    userList = discord.utils.get(interaction.guild.roles, name = "🚉《高速列申方案訂閱中》").members

@is_owner()
@adminmonthly_group.command(name="statistics", description="總計月數金額")
@app_commands.describe()
async def statistics(interaction: discord.Interaction):
    total_amount, total_quantity = monthly.get_statistics()
    await interaction.response.send_message(embed = mm.statistics(total_quantity, total_amount, interaction.guild.icon.url), ephemeral=True)