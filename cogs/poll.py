import discord
from discord import ApplicationContext, Option, asyncio
from discord.ext import commands


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='create_poll', description='Create a poll')
    async def create_poll(
        self,
        ctx: ApplicationContext,
        question: Option(str, description="What is the poll question?", required=True),
        channel: Option(discord.TextChannel, description="The channel where the poll will be created", required=False)
    ):
        await ctx.defer(ephemeral=True)
        await ctx.respond("Please enter the options in the following format\n\nEmoji: Option\nEmoji: Option\n\nFor Example\n:heart:: Go to the movies\n:handshake:: Go to the walk", ephemeral=True)

        def check(message):
            return message.author == ctx.author

        try:
            message = await self.bot.wait_for('message', timeout=300.0, check=check)
            options = message.content.strip().split('\n')
            options_list = [option.strip() for option in options]
            options = {}
            embed = discord.Embed(title=f"Poll: {question}", color=discord.Color.teal())
            options_text = ""
            for option in options_list:
                emoji, option = option.split(':')
                emoji = emoji.strip()
                option = option.strip()
                options[emoji] = option
                options_text += f"{emoji}: {option}\n"
            embed.add_field(name='Options', value=options_text)
            await message.delete()
            if channel is None:
                message = await ctx.followup.send(embed=embed)
            else:
                message = await channel.send(embed=embed)

            for emoji in options.keys():
                await message.add_reaction(emoji)

        except asyncio.TimeoutError:
            return await ctx.followup.send('Failed to create poll! You didn\'t provide options in time', ephemeral=True)


def setup(bot: discord.Bot):
    bot.add_cog(Poll(bot))
