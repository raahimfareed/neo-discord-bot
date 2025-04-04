import os
import discord
from discord import ApplicationContext, EmbedProvider, Option, asyncio
from discord.ext import commands


class Employee(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='apply_leave', description='Apply for a leave')
    @commands.has_role(int(os.getenv('EMPLOYEE_ROLE_ID') or 0))
    async def apply_leave(
        self,
        ctx: ApplicationContext,
        reason: Option(str, description="What is the reason for leave?", required=True),
        duration: Option(int, description="Duration of leave in days", required=True),
        documentation: Option(bool, description="Are there any documents supporting the reason?", required=False)
    ):
        await ctx.defer(ephemeral=True)
        if documentation is True:
            await ctx.respond("Please upload any supporting documents", ephemeral=ctx.guild is not None)

            def check(message):
                return (
                    message.author == ctx.author and
                    message.channel == ctx.channel and
                    len(message.attachments) > 0
                )

            try:
                message = await self.bot.wait_for('message', timeout=60.0, check=check)
                for attachment in message.attachments:
                    await ctx.followup.send(f"Received File: {attachment.filename}\nFile URL: {attachment.url}", ephemeral=ctx.guild is not None)
                await message.delete()
            except asyncio.TimeoutError:
                await ctx.followup.send("You took too long to upload a file!", ephemeral=True)

        return await ctx.followup.send(f"## Leave Applied\n**Reason:** {reason}\n**Duration (In Days):** {duration}", ephemeral=ctx.guild is not None)


def setup(bot: discord.Bot):
    bot.add_cog(Employee(bot))
