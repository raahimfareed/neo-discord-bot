import os

import discord
from dotenv import load_dotenv

cogs_list = [
  'hello'
]


def init():
  load_dotenv()

def main():
  init()

  token = str(os.getenv("TOKEN"))
  bot = discord.Bot()


  @bot.event
  async def on_ready():
    print(f"{bot.user} is ready and online")

  
  for cog in cogs_list:
    bot.load_extension(f"cogs.{cog}")
  
  bot.run(token)


if __name__ == "__main__":
  main()