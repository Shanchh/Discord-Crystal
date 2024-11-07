import discord
from discord.ext import commands
from discord import app_commands
import threading
import configparser
from app import FlaskApp

config = configparser.ConfigParser()
config.read('setting/botToken.ini')

botToken = config['setting']['botToken']

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f"Discord 機器人已登入，使用者名稱: {bot.user}")
    print(f"載入 {len(slash)} 個斜線指令")

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

class Discord_Monthly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="monthly", description="管理月度訂閱")
    async def monthly(self, interaction: discord.Interaction):
        await interaction.response.send_message("請使用具體的子命令")

    @app_commands.command(name="adduser", description="新增訂閱者資料")
    @app_commands.describe(userAt="@使用者")
    async def adduser(self, interaction: discord.Interaction, userAt: str):
        await interaction.response.send_message(f"你@了 {userAt}")

def run_flask():
    flask_app = FlaskApp()
    flask_app.run(host="127.0.0.1", port=6620)

if __name__ == '__main__':
    # flask_thread = threading.Thread(target=run_flask)
    # flask_thread.start()

    bot.run("YOUR_BOT_TOKEN")