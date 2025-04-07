import os
import discord
import asyncio
from discord.ext import commands


class Voice(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.temporary_channels = list()
        self.temporary_category_id = os.getenv('TEMP_CATEGORY_ID')
    
    @commands.slash_command(name='create_temporary_voice', description='Creates a temporary voice channel')
    async def create_temporary_voice(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        category = discord.utils.get(ctx.guild.categories, id=int(self.temporary_category_id))
        if category is None:
            await ctx.send("Temporary category not found.", ephemeral=True)
            return
        
        voice_channel = await ctx.guild.create_voice_channel(name=f"Temp Voice {len(self.temporary_channels) + 1}", category=category)

        self.temporary_channels.append(VoiceChannel(voice_channel))
        await ctx.respond(f"Temporary voice channel created: {voice_channel.mention}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.channel and before.channel.id in [vc.channel.id for vc in self.temporary_channels]:
            vc_obj = next(vc for vc in self.temporary_channels if vc.channel.id == before.channel.id)
            if vc_obj.is_empty():
                await vc_obj.start_timer()
        if after.channel and after.channel.id in [vc.channel.id for vc in self.temporary_channels]:
            vc_obj = next(vc for vc in self.temporary_channels if vc.channel.id == after.channel.id)
            await vc_obj.cancel_timer()


class VoiceChannel:
    def __init__(self, channel: discord.VoiceChannel):
        self.channel = channel
        self.timer: asyncio.Task | None = asyncio.create_task(self._deletion_countdown())

    def is_empty(self):
        return len(self.channel.members) == 0
    
    async def cancel_timer(self):
        if self.timer and not self.timer.done():
            self.timer.cancel()
            try:
                await self.timer
            except asyncio.CancelledError:
                pass
            self.timer = None
    
    async def start_timer(self):
        await self.cancel_timer()
        self.timer = asyncio.create_task(self._deletion_countdown())

    async def _deletion_countdown(self):
        try:
            await asyncio.sleep(120)
            if self.is_empty():
                await self.channel.delete(reason="Temporary channel empty for too long")
        except asyncio.CancelledError:
            pass



def setup(bot: discord.Bot):
    bot.add_cog(Voice(bot))