import discord
from discord.ext import commands

class Hello(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.slash_command()
  async def hello(self, ctx):
    await ctx.respond("Hey!\nI'm Neo")
  
  @commands.Cog.listener()
  async def on_member_join(self, member):
    await member.send('Welcome to NeoFlux')

def setup(bot):
  bot.add_cog(Hello(bot))