import discord
from discord import Option
from datetime import timedelta
from discord.ext import commands
from discord.ext.commands import MissingPermissions


class Moderation(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.slash_command(name='timeout', description='mutes/timeouts a member')
  @commands.has_permissions(moderate_members=True)
  async def timeout(
      self, 
      ctx, 
      member: Option(discord.Member, required=True), 
      reason: Option(str, required=False),
      days: Option(int, max_value=28, required=False),
      hours: Option(int, required=False),
      minutes: Option(int, required=False),
      seconds: Option(int, required=False)
    ):
      if member.id == ctx.author.id:
        await ctx.respond("You can't timeout yourself")
        return
      
      if member.guild_permissions.moderate_members:
        await ctx.respond("You can't do that! This person is a moderator")
        return
      
      if days is None:
        days = 0
      
      if hours is None:
        hours = 0
      
      if minutes is None:
        minutes = 0

      if seconds is None:
        seconds = 0

      duration = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

      await member.timeout_for(duration, reason=reason)
      timeout_response = f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
      if reason is not None:
        timeout_response += f" for `{reason}`"
      await ctx.respond(timeout_response)
  
  @timeout.error
  async def timeouterror(self, ctx, error):
    if isinstance(error, MissingPermissions):
      return await ctx.respond("You can't do this! You need to have moderate member permissions")

    raise error

def setup(bot):
  bot.add_cog(Moderation(bot))