import os
import discord
from discord import Option
from datetime import timedelta
from discord.ext import commands
from discord.ext.commands import MissingPermissions

from utils.embed import send_log


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        print(message,message.content)

  
    @commands.slash_command(name='mute', description='Mutes/timeouts a member')
    @commands.has_permissions(moderate_members=True)
    async def mute(
        self, 
        ctx, 
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


    @mute.error
    async def muteerror(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return await ctx.respond("You can't do this! You need to have moderate member permissions")

        raise error

    @commands.slash_command(name='unmute', description='Umutes member')
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: Option(discord.Member, required=True), reason: Option(str, required=False), log: Option(bool, required=False)):
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

    @unmute.error
    async def unmuteerror(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return await ctx.respond("You can't do this! You need to have moderate member permissions")

        raise error

    @commands.slash_command(name='kick', description='Kicks a member')
    @commands.has_permissions(kick_members=True)
    async def kick(
        self, 
        ctx,
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

    @kick.error
    async def kickerror(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return await ctx.respond("You don't have permissions to kick members! :no_entry:")

        raise error

    @commands.slash_command(name='ban', description='Bans members')
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        ctx,
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

    @ban.error
    async def banerror(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return await ctx.respond("You don't have permissions to ban members! :no_entry:")

        raise error


def setup(bot):
  bot.add_cog(Moderation(bot))
