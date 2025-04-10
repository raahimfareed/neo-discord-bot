import discord
from discord.errors import HTTPException, NotFound
from discord.ext import commands
from discord.ext.commands.errors import MissingAnyRole, MissingPermissions, MissingRole, NoPrivateMessage


class ErrorHandler(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error):
        if isinstance(error, MissingPermissions):
            return await ctx.respond("You don't have permissions to run this command! :no_entry:", ephemeral=True)

        if isinstance(error, MissingRole) or isinstance(error, MissingAnyRole):
            return await ctx.respond("You don't have the role required for this command! :no_entry:", ephemeral=True)

        if isinstance(error, HTTPException):
            return await ctx.respond("An error with network occurred! Please try again :face_holding_back_tears:", ephemeral=True)

        if isinstance(error, NotFound):
            return await ctx.respond("An error with network occurred! Please try again :face_holding_back_tears:", ephemeral=True)
        
        if isinstance(error, NoPrivateMessage):
            return await ctx.respond("This command cannot be used in DMs! :no_entry:")

        raise error


def setup(bot: discord.Bot):
    bot.add_cog(ErrorHandler(bot))
