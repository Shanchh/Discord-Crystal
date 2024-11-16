import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import has_permissions
import threading
import configparser
from app import FlaskApp
from utils import c_embed, monthly
from utils.firebase_db import Db_Client


config = configparser.ConfigParser()
config.read('setting/botToken.ini')

botToken = config['setting']['botToken']

bot = commands.Bot(
    command_prefix="$",
    intents=discord.Intents.all(),
    owner_id=316548382308958208
)

adminmonthly_group = app_commands.Group(name="adminmonthly", description="管理月度訂閱")
monthly_group = app_commands.Group(name="monthly", description="訂閱查詢功能")
bot.tree.add_command(adminmonthly_group)
bot.tree.add_command(monthly_group)

# ----- Basic -----

@bot.event
async def on_ready():
    print(f"Discord 機器人已登入，使用者名稱: {bot.user}")
    slash = await bot.tree.sync()
    print(f"載入 {len(bot.tree.get_commands())} 個斜線指令")

@bot.command()
async def ping(ctx):
    await ctx.send("測試測試")

def is_owner():
    async def predicate(interaction: discord.Interaction):
        return await bot.is_owner(interaction.user)
    return app_commands.check(predicate)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        msg = c_embed.basic("權限不足", "你沒有權限執行此指令。", 0xffa82e)
        await interaction.response.send_message(embed = msg, ephemeral=True)
    else:
        raise error
    
# ----- Monthly ----- #

@monthly_group.command(name="details", description="列出個人訂閱明細")
@app_commands.describe()
async def listsubdetails(interaction: discord.Interaction):
    db = Db_Client()
    author = interaction.user
    s = db.list_subscriber_details(author.id)
    if s == None:
        await interaction.response.send_message(embed = c_embed.basic("個人訂閱明細", "查無相關訂閱資料", 0xffa82e))
    else:
        await interaction.response.send_message(embed = c_embed.getDetail_embed(author.avatar.url))
        for count, data in enumerate(s):
            await interaction.channel.send(embed = c_embed.getDetail_info(count, data, author.avatar.url))


@monthly_group.command(name="check", description="確認個人訂閱狀態")
@app_commands.describe()
async def checkstatus(interaction: discord.Interaction):
    db = Db_Client()
    author = interaction.user
    if (db.list_subscriber_details(author.id) == None):
        await interaction.response.send_message(embed = c_embed.basic("訂閱狀態查詢", "查無相關訂閱資料", 0xffa82e))
        return
    s, dateDeadLine = monthly.check_subscriber_state(author.id)
    if not s:
        await interaction.response.send_message(embed = c_embed.checkstatus("您目前不在訂閱期間內！", 0xffa82e, author.avatar.url))
    else:
        formatted_date = dateDeadLine.strftime("%Y-%m-%d")
        await interaction.response.send_message(embed = c_embed.checkstatus(f"您目前在訂閱期間！ 期限至: {formatted_date}", 0x00ff11, author.avatar.url))

# ----- AdminMonthly ----- #

@is_owner()
@adminmonthly_group.command(name="adduser", description="新增訂閱者")
@app_commands.describe(member = "@使用者")
async def adduser(interaction: discord.Interaction, member:discord.Member):
    db = Db_Client()
    s = db.add_subscriber_user(member.id, member.name)
    embed = c_embed.basic("新增訂閱者", "你已成功新增一名訂閱者", 0x00ff11) if s else c_embed.request_error("新增訂閱者")
    await interaction.response.send_message(embed = embed)

@is_owner()
@adminmonthly_group.command(name="adddetail", description="新增訂閱明細")
@app_commands.describe(member = "@使用者", purchase_date = "購買日期", quantity = "數量", payment = "付款方式")
@commands.has_permissions(administrator=True)
async def adddetail(interaction: discord.Interaction, member: discord.Member, purchase_date: str, quantity: int, payment: str):
    db = Db_Client()
    s, dataId = db.add_subscriber_detail(member.id, member.name, purchase_date, quantity, payment)
    embed = c_embed.basic("新增訂閱明細", f"你已成功新增一條明細,ID:{dataId}", 0x00ff11) if s else c_embed.request_error("新增訂閱明細")
    await interaction.response.send_message(embed = embed)

@is_owner()
@adminmonthly_group.command(name="deluser", description="刪除訂閱者")
@app_commands.describe(member="@使用者")
async def deluser(interaction: discord.Interaction, member:discord.Member):
    db = Db_Client()
    s = db.del_subscriber_user(member.id)
    if s == None:
        embed = c_embed.basic("刪除訂閱者", "查無此訂閱者", 0xffa82e)
    else:
        embed = c_embed.basic("刪除訂閱者", "你已成功刪除一位訂閱者", 0x00ff11) if s else c_embed.request_error("刪除訂閱者")
    await interaction.response.send_message(embed = embed)

@is_owner()
@adminmonthly_group.command(name="deldatail", description="刪除訂閱明細")
@app_commands.describe(dataid="識別號碼")
async def deldetail(interaction: discord.Interaction, dataid: int):
    db = Db_Client()
    s = db.del_subscriber_detail(dataid)
    if s == None:
        embed = c_embed.basic("刪除訂閱明細", "查無此訂閱明細", 0xffa82e)
    else:
        embed = c_embed.basic("刪除訂閱明細", "你已成功刪除一條訂閱明細", 0x00ff11) if s else c_embed.request_error("刪除訂閱明細")
    await interaction.response.send_message(embed = embed)

@is_owner()
@adminmonthly_group.command(name="listdetails", description="列出所有訂閱明細")
@app_commands.describe()
async def listalldetails(interaction: discord.Interaction):
    db = Db_Client()
    channel = interaction.channel
    await interaction.response.send_message(embed=c_embed.basic("列出所有訂閱明細", "已收到請求！", 0x00ff11))
    all_details = [db.get_detail(dataId) for dataId in db.get_all_detail_lists()]
    for i in range(0, len(all_details), 5):
        embed = await c_embed.listDetail_embed(bot, all_details[i:i+5], i)
        await channel.send(embed = embed)

def run_flask():
    flask_app = FlaskApp()
    flask_app.run(host="127.0.0.1", port=6620)

if __name__ == '__main__':
    # flask_thread = threading.Thread(target=run_flask)
    # flask_thread.start()

    bot.run(botToken)