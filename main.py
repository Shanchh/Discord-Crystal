import discord
from discord.ext import commands
import threading
import configparser
from app import FlaskApp

config = configparser.ConfigParser()
config.read('setting/botToken.ini')

botToken = config['setting']['botToken']

bot = commands.Bot(command_prefix="!!", intents=discord.Intents.all(), case_insensitive=True)

@bot.event
async def on_ready():
    print(f"Discord 機器人已登入，使用者名稱: {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

def run_flask():
    flask_app = FlaskApp()
    flask_app.run(host = "127.0.0.1", port = 6620)

if __name__ == '__main__':
    flask_thread = threading.Thread(target = run_flask)
    flask_thread.start()
    
    bot.run(botToken)