import os
import discord
from discord import Option, ApplicationContext
from datetime import datetime, timedelta
from discord.ext import commands

from utils.embed import send_log


class Moderation(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        pass

  
    @commands.slash_command(name='mute', description='Mutes/timeouts a member')
    @commands.has_permissions(moderate_members=True)
    async def mute(
        self, 
        ctx: ApplicationContext, 
        member: Option(discord.Member, required=True),
        reason: Option(str, required=False),
        days: Option(int, max_value=28, required=False),
        hours: Option(int, required=False),
        minutes: Option(int, required=False),
        seconds: Option(int, required=False),
        log: Option(bool, required=False)
    ):
        if member.id == ctx.author.id:
            return await ctx.respond("You can't mute yourself")

        if member.guild_permissions.moderate_members:
            return await ctx.respond("You can't do that! This person is a moderator")

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
        duration = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
        timeout_response = f"<@{member.id}> has been muted for {duration}"
        if reason is not None:
            timeout_response += f" for `{reason}`"
        await ctx.respond(timeout_response)

        if log is False:
            return

        await send_log(self.bot, 'Timeout', 'User timed out', discord.Colour.blurple(), [
            ('Member', f"<@{member.id}>", True),
            ('Muted By', f"<@{ctx.author.id}>", True),
            ('Reason', reason),
            ('Timeout Duration', duration),
        ])

    @commands.slash_command(name='unmute', description='Umutes member')
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx: ApplicationContext, member: Option(discord.Member, required=True), reason: Option(str, required=False), log: Option(bool, required=False)):
        await member.remove_timeout()
        timeout_response = f"<@{member.id}> unmuted"
        if reason is not None:
            timeout_response += f" for `{reason}`"
        await ctx.respond(timeout_response)

        if log is False:
            return

        await send_log(self.bot, 'Timeout', 'User unmuted', discord.Colour.green(), [
            ('Member', f"<@{member.id}>", True),
            ('Unmuted By', f"<@{ctx.author.id}>", True),
            ('Reason', reason),
        ])

    @commands.slash_command(name='kick', description='Kicks a member')
    @commands.has_permissions(kick_members=True)
    async def kick(
        self, 
        ctx: ApplicationContext,
        member: Option(discord.Member, description="Who do you want to kick?", required=True),
        reason: Option(str, required=False),
        log: Option(bool, description="Display in logs?", required=False)
    ):
        if member.id == ctx.author.id:
            return await ctx.respond("You can't kick yourself! :face_with_raised_eyebrow:")

        if member.guild_permissions.administrator:
            return await ctx.respond("You can't kick admins! :rolling_eyes:")

        response = f"<@{member.id}> has been kicked"
        if reason is not None:
            response += f"\nReason: `{reason}`"

        await member.kick(reason=reason)
        await ctx.respond(response)

        if log is False:
            return

        await send_log(self.bot, 'Kick', 'User kicked', discord.Colour.orange(), [
            ('Member', f"<@{member.id}>", True),
            ('Kicked By', f"<@{ctx.author.id}>", True),
            ('Reason', reason),
        ])

    @commands.slash_command(name='ban', description='Bans members')
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: ApplicationContext,
        member: Option(discord.Member, description="Who do you want to kick?", required=True),
        reason: Option(str, description="Why?", required=False),
        log: Option(bool, description="Display in logs?", required=False)
    ):
        if member.id == ctx.author.id:
            return await ctx.respond("You can't ban yourself! :face_with_raised_eyebrow:")

        if member.guild_permissions.administrator:
            return await ctx.respond("You can't ban admins! :rolling_eyes:")

        response = f"<@{member.id}> has been banned"
        if reason is not None:
            response += f"\nReason: `{reason}`"

        await member.ban(reason=reason)
        await ctx.respond(response)

        if log is False:
            return

        await send_log(self.bot, 'Ban', 'User banned', discord.Colour.red(), [
            ('Member', f"<@{member.id}>", True),
            ('Banned By', f"<@{ctx.author.id}>", True),
            ('Reason', reason),
        ])

    @commands.slash_command(name='bans', description='List of all bans')
    @commands.has_permissions(ban_members=True)
    async def bans(
        self,
        ctx: ApplicationContext
    ):
        await ctx.defer()
        bans = await ctx.guild.bans().flatten()

        embed = discord.Embed(title=f"List of Bans in {ctx.guild}", timestamp=datetime.now(), color=discord.Colour.red())

        for entry in bans:
            if len(embed.fields) > 25:
                break

            if len(embed) > 5900:
                embed.add_field(name='Too many bans to list', value='')
                continue

            embed.add_field(name="Ban", value=f"Username: {entry.user.name}\nReason: {entry.reason}\nUser ID: {entry.user.id}\nIs Bot: {entry.user.bot}", inline=True)

        await ctx.respond(embed=embed)

    @commands.slash_command(name='unban', description='Unbans members')
    @commands.has_permissions(ban_members=True)
    async def unban(
        self,
        ctx: ApplicationContext,
        member_id: Option(str, description="ID of the member you want to unban", required=True)
    ):
        await ctx.defer()
        member = await self.bot.get_or_fetch_user(member_id)
        if member is None:
            return await ctx.respond(f"Member with ID {member_id} doesn't exist in bans")

        await ctx.guild.unban(member)
        await ctx.respond(f"I've unbanned {member.mention}")


def setup(bot):
  bot.add_cog(Moderation(bot))
