import discord
from discord.ext import commands


class Meeting(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        self.recording = None

    @commands.slash_command(name='record', description='Records voice activity')
    async def record(self, ctx: discord.ApplicationContext):
        voice = ctx.author.voice
        if not voice:
            return await ctx.respond("You're not in a voice channel")

        vc = await voice.channel.connect()
        source = discord.FFmpegPCMAudio('assets/channel_recording_start.mp3')
        vc.play(source)
        self.recording = vc
        vc.start_recording(
            discord.sinks.WaveSink(),
            self.once_done,
            ctx.channel
        )

        await ctx.respond("Started recording!")

    async def once_done(self, sink: discord.sinks, channel: discord.TextChannel, *args):
        recorded_users = [
            f"<@{user_id}>"
            for user_id, audio in sink.audio_data.items()
        ]
        print(recorded_users)
        await sink.vc.disconnect()
        files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]
        await channel.send(f"Finished recording for: {', '.join(recorded_users)}.", files=files)

    @commands.slash_command(name='stop_recording', description='Stop recording voice')
    async def stop_recording(
        self,
        ctx: discord.ApplicationContext
    ):
        if not self.recording:
            return await ctx.respond("I'm not currently recording")

        vc = self.recording

        vc.stop_recording()
        self.recording = None

        await ctx.delete()


def setup(bot: discord.Bot):
    bot.add_cog(Meeting(bot))
