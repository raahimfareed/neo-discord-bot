import os

from database import db
from models.Ticket import Ticket

import discord
from discord.ext.commands import MissingPermissions
from discord.types import activity
from dotenv import load_dotenv

cogs_list = [
    'hello',
    'moderation',
    'meeting',
    'ticketing',
    'voice'
]


def init() -> discord.Bot:
    load_dotenv()

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
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

    @bot.event
    async def on_member_join(member):
        await member.send('Welcome to NeoFlux')

    @bot.event
    async def on_application_command_error(ctx: discord.ApplicationContext, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("You don't have permissions to run this command! :no_entry:")
        raise error

    for cog in cogs_list:
        bot.load_extension(f"cogs.{cog}")

    bot.run(token)


if __name__ == "__main__":
    main()
