import discord
import datetime

def init():
    embed = discord.Embed(timestamp = datetime.datetime.now())
    embed.set_footer(text="Crystal", icon_url="https://i.imgur.com/jsMle7g.jpeg")
    return embed

def basic(title = None, description = None, color = None):
    embed = init()
    embed.title = title
    embed.description = description
    embed.color = color
    return embed

def request_error(title = None):
    embed = init()
    embed.title = title
    embed.description = "處理請求時發生問題"
    embed.color = 0xff0000
    return embed