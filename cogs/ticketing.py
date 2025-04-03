import discord
from discord import Option, ApplicationContext
from discord.ext import commands
from discord.ui import InputText, Modal


class Ticketing(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.slash_command(name='create_ticket', description='Create a support ticket')
    async def create_ticket(self, ctx: ApplicationContext):
        modal = TicketModal()
        await ctx.interaction.response.send_modal(modal)

class TicketModal(Modal):
    def __init__(self) -> None:
        super().__init__(title="Create Ticket")
        self.add_item(InputText(label="Subject", placeholder="What is the ticket about?"))
        self.add_item(InputText(label="Description", placeholder="Explain the query", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Ticket Submitted", color=discord.Color.blurple(), description="One of the representative will get back to you shortly!")
        await interaction.response.send_message(embed=embed)


def setup(bot: discord.Bot):
    bot.add_cog(Ticketing(bot))

