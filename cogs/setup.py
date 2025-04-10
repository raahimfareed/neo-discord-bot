import discord
import asyncio
from discord import ApplicationContext, Interaction, Option, TextChannel, Role
from discord.ext import commands


class Setup(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.slash_command(name="setup", description="Setup for the bot")
    @commands.has_permissions(administrator=True)
    async def setup(
        self,
        ctx: ApplicationContext,
        log_channel: Option(TextChannel, required=True),
        announcement_channel_id: Option(str, required=True),
        employee_role: Option(Role, required=True),
        admin_role: Option(Role, required=True),
        temporary_category_id: Option(str, required=True)
    ):
        self_destruct_time = 10
        await ctx.respond("Setting up bot!")
        await asyncio.sleep(1)
        await ctx.edit(content=f"Setup complete! This message will self destruct in {self_destruct_time} seconds!")
        await ctx.delete(delay=self_destruct_time)


def setup(bot: discord.Bot):
    bot.add_cog(Setup(bot))
