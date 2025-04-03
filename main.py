import os

import discord
from dotenv import load_dotenv

cogs_list = [
    'hello',
    'moderation'
]


def init() -> discord.Bot:
    load_dotenv()
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    intents.members = True
    bot = discord.Bot(intents=intents)

    return bot

def main():
    bot = init()
    token = str(os.getenv("TOKEN"))


    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready and online")

    @bot.event
    async def on_member_join(member):
        await member.send('Welcome to NeoFlux')


    for cog in cogs_list:
        bot.load_extension(f"cogs.{cog}")

    bot.run(token)


if __name__ == "__main__":
    main()
