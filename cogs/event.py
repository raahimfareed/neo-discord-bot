import os
from discord import ApplicationContext, Option, asyncio
import discord
from discord.ext import commands


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='announce', description='Create an announcement')
    async def announce(
        self,
        ctx: ApplicationContext,
    ):
        announcement_channel_id = int(os.getenv('ANNOUNCEMENT_CHANNEL_ID') or '0')
        channel = self.bot.get_channel(announcement_channel_id)
        
        if channel is None:
            return await ctx.respond("Unable to find announcement channel")

        await ctx.defer(ephemeral=True)
        await ctx.respond("Please write the body for your announcement, send - to cancel the announcment", ephemeral=True)


        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            message = await self.bot.wait_for('message', timeout=120.0, check=check)
            content = message.content.strip()
            if len(content) == 1 and content == '-':
                await message.delete()
                return await ctx.respond("Announcement Cancelled", ephemeral=True)
            await channel.send(content)
            await message.delete()
            return await ctx.respond("Announcement Created", ephemeral=True)
        except asyncio.TimeoutError:
            await ctx.respond("Announcement cancelled!\nYou took too long to respond")


def setup(bot: discord.Bot):
    bot.add_cog(Event(bot))
