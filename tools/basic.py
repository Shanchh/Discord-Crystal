import discord
from discord import app_commands

from discord_bot import bot

def is_owner():
    """確認是否為持有者"""
    async def predicate(interaction: discord.Interaction):
        return await bot.is_owner(interaction.user)
    return app_commands.check(predicate)