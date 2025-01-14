import discord
from discord.ext import commands

bot = commands.Bot(
    command_prefix="$",
    intents=discord.Intents.all(),
    owner_id=316548382308958208
)