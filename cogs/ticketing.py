from datetime import datetime
import discord
from discord import Option, ApplicationContext
from discord.ext import commands
from discord.ui import InputText, Modal

from models.Ticket import Ticket


class Ticketing(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.slash_command(name='create_ticket', description='Create a support ticket')
    async def create_ticket(self, ctx: ApplicationContext):
        modal = TicketModal()
        return await ctx.interaction.response.send_modal(modal)

    @commands.slash_command(name='get_tickets', description='Get Tickets')
    async def get_tickets(self, ctx: ApplicationContext):
        await ctx.defer(ephemeral=ctx.guild is not None)

        user_id = ctx.author.id

        embed = discord.Embed(title=f"List of Tickets :tickets:", timestamp=datetime.now(), color=discord.Color.fuchsia())

        tickets = Ticket.select().where(Ticket.user_id == user_id)

        for ticket in tickets:
            if len(embed.fields) > 25:
                break

            if len(embed) > 5900:
                embed.add_field(name='Too many tickets to list', value='')
                continue

            embed.add_field(name="Ticket", value=f"ID: {ticket.id}\nSubject: {ticket.subject}\nDescription: {ticket.description}\nResolution: {'Resolved' if ticket.resolution is True else 'Open'}\nTicket Date: {ticket.created_at}", inline=True)
        return await ctx.respond(embed=embed, ephemeral=ctx.guild is not None)


class TicketModal(Modal):
    def __init__(self) -> None:
        super().__init__(title="Create Ticket")
        self.add_item(InputText(label="Subject", placeholder="What is the ticket about?"))
        self.add_item(InputText(label="Description", placeholder="Explain the query", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        Ticket.create(
            subject=self.children[0].value,
            description=self.children[1].value,
            user_id=interaction.user.id
        )
        await interaction.response.send_message("Ticket Submitted :white_check_mark:", ephemeral=interaction.guild is not None)


def setup(bot: discord.Bot):
    bot.add_cog(Ticketing(bot))

