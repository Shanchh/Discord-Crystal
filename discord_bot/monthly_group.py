import discord
from discord import app_commands

from utils import Db_Client
from tools import check_subscriber_state
import discord_embed.basic_embed as bm
import discord_embed.monthly_embed as mm

monthly_group = app_commands.Group(name="monthly", description="訂閱查詢功能")

@monthly_group.command(name="details", description="列出個人訂閱明細")
@app_commands.describe()
async def listsubdetails(interaction: discord.Interaction):
    db = Db_Client()
    author = interaction.user
    s = db.list_subscriber_details(author.id)
    if s == None:
        await interaction.response.send_message(embed = bm.basic("個人訂閱明細", "查無相關訂閱資料", 0xffa82e))
    else:
        await interaction.response.send_message(embed = mm.getDetail_embed(author.avatar.url))
        for count, data in enumerate(s):
            await interaction.channel.send(embed = mm.getDetail_info(count, data, author.avatar.url))

@monthly_group.command(name="check", description="確認個人訂閱狀態")
@app_commands.describe()
async def checkstatus(interaction: discord.Interaction):
    db = Db_Client()
    author = interaction.user
    if (db.list_subscriber_details(author.id) == None):
        await interaction.response.send_message(embed = bm.basic("訂閱狀態查詢", "查無相關訂閱資料", 0xffa82e))
        return
    s, dateDeadLine = check_subscriber_state(author.id)
    if not s:
        await interaction.response.send_message(embed = mm.checkstatus("您目前不在訂閱期間內！", 0xffa82e, author.avatar.url))
    else:
        formatted_date = dateDeadLine.strftime("%Y-%m-%d")
        await interaction.response.send_message(embed = mm.checkstatus(f"您目前在訂閱期間！ 期限至: {formatted_date}", 0x00ff11, author.avatar.url))