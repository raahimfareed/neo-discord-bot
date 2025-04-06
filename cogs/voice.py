import discord
from discord.ext import commands


class Voice(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.guilds = {}
    
    @commands.slash_command(name='create_temporary_voice', description='Creates a temporary voice channel')
    async def create_temporary_voice(self, ctx: discord.ApplicationContext):
        if ctx.guild.id not in self.guilds:
            self.guilds[ctx.guild.id] = list()
        
        voice_channel = await ctx.guild.create_voice_channel(name=f"Temp Voice {len(self.guilds[ctx.guild.id]) + 1}")
        self.guilds[ctx.guild.id].append(VoiceChannel(voice_channel))


class VoiceChannel:
    def __init__(self, channel: discord.VoiceChannel):
        self.channel = channel
        self.timer = None

    def is_empty(self):
        return len(self.channel.members) == 0

    def cancel_timer(self):
        if self.timer and not self.timer.done():
            self.timer.cancel()
            self.timer = None
    
    def start_timer(self, bot: discord.Bot):
        self.cancel_timer()
        # self.timer = bot.loop.create_task(self.delete)



def setup(bot: discord.Bot):
    bot.add_cog(Voice(bot))