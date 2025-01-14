import discord
from discord import app_commands

from discord_bot import bot, adminmonthly_group, monthly_group
import discord_embed.basic_embed as bm

@bot.event
async def on_ready():
    print(f"Discord 機器人已登入，使用者名稱: {bot.user}")
    slash = await bot.tree.sync()
    print(f"載入 {len(bot.tree.get_commands())} 個斜線指令")

@bot.command()
async def ping(ctx):
    await ctx.send("測試測試")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        msg = bm.basic("權限不足", "你沒有權限執行此指令。", 0xffa82e)
        await interaction.response.send_message(embed = msg, ephemeral=True)
    else:
        raise error

bot.tree.add_command(adminmonthly_group)
bot.tree.add_command(monthly_group)