import os

from discord.errors import HTTPException, NotFound
from discord.ext.commands.errors import MissingAnyRole, MissingRole

from database import db
from models.Ticket import Ticket

import discord
from discord.ext.commands import MissingPermissions, NoPrivateMessage
from dotenv import load_dotenv

cogs_list = [
    'setup',
    'hello',
    'moderation',
    'meeting',
    'ticketing',
    'event',
    'employee',
    'poll',
    'voice',
    'error_handler'
]


def init() -> discord.Bot:
    load_dotenv()

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    intents.presences = True
    intents.guilds = True
    intents.voice_states = True
    intents.members = True
    bot = discord.Bot(intents=intents)

    db.connect()
    db.create_tables([Ticket], safe=True)
    db.close()

    return bot

def main():
    bot = init()
    token = str(os.getenv("TOKEN"))


    @bot.event
    async def on_ready():
        game = discord.Game('with the API')
        await bot.change_presence(activity=game)
        print(f"{bot.user} is ready and online")

    for cog in cogs_list:
        bot.load_extension(f"cogs.{cog}")

    bot.run(token)


if __name__ == "__main__":
    main()
