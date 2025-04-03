import os
import discord
from discord.ext import commands

async def send_log(bot: discord.Bot, title: str, description: str, color: discord.Colour, fields: list[tuple]):
    log_channel_id = int(os.getenv('LOG_CHANNEL_ID') or '0')
    channel = bot.get_channel(log_channel_id)
    if channel is None:
        return

    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )

    for field in fields:
        embed.add_field(name=field[0], value=field[1], inline=field[2] if len(field) > 2 else False)

    await channel.send(embed=embed)

