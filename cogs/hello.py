from datetime import datetime
import discord
from discord.ext import commands

class Hello(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.slash_command()
  async def hello(self, ctx):
    await ctx.respond("Hey!\nI'm Neo")
  
  @commands.slash_command()
  async def status(self, ctx):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await ctx.respond(f"My name is Neo, as of {current_time}")
  
  @commands.slash_command()
  async def ping(self, ctx):
    await ctx.respond(f"Pong 🏓\nLatency: {self.bot.latency*1000}ms")

def setup(bot):
  bot.add_cog(Hello(bot))