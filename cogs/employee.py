import os
import discord
from discord import ApplicationContext, EmbedProvider, Option, asyncio
from discord.ext import commands


class Employee(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.meetings = list()

    @commands.slash_command(name='apply_leave', description='Apply for a leave')
    @commands.has_role(int(os.getenv('EMPLOYEE_ROLE_ID') or 0))
    async def apply_leave(
        self,
        ctx: ApplicationContext,
        reason: Option(str, description="What is the reason for leave?", required=True),
        duration: Option(int, description="Duration of leave in days", required=True),
        documentation: Option(bool, description="Are there any documents supporting the reason?", required=False)
    ):
        await ctx.defer(ephemeral=True)
        if documentation is True:
            await ctx.respond("Please upload any supporting documents", ephemeral=ctx.guild is not None)

            def check(message):
                return (
                    message.author == ctx.author and
                    message.channel == ctx.channel and
                    len(message.attachments) > 0
                )

            try:
                message = await self.bot.wait_for('message', timeout=60.0, check=check)
                for attachment in message.attachments:
                    await ctx.followup.send(f"Received File: {attachment.filename}\nFile URL: {attachment.url}", ephemeral=ctx.guild is not None)
                await message.delete()
            except asyncio.TimeoutError:
                await ctx.followup.send("You took too long to upload a file!", ephemeral=ctx.guild is not None)

        return await ctx.followup.send(f"## Leave Applied\n**Reason:** {reason}\n**Duration (In Days):** {duration}", ephemeral=ctx.guild is not None)
    
    @commands.slash_command(name='meeting', description='Schedule a meeting')
    @commands.has_any_role(int(os.getenv('EMPLOYEE_ROLE_ID') or 0), int(os.getenv('ADMIN_ROLE_ID') or 0))
    async def meeting(
        self,
        ctx: ApplicationContext,
        date: Option(str, description="Date of meeting. Format: YYYY-MM-DD. Example: 2025-04-08", required=True),
        time: Option(str, description="Time of meeting. Format: HH:MM. Example: 14:30", required=True),
        meeting_channel: Option(discord.VoiceChannel, description="Voice channel for meeting", required=False),
        meeting_notification_channel: Option(discord.TextChannel, description="Text channel for notifying about meeting", required=False),
        title: Option(str, description="Title of meeting", required=False),
        description: Option(str, description="Description of meeting", required=False),
        members: Option(str, description="Members to invite. Format: @member1, @member2", required=False),
    ):
        await ctx.defer(ephemeral=True)
        embed = discord.Embed(title="Meeting Scheduled", description=f"**Date:** {date}\n**Time:** {time}", color=discord.Color.green())
        if title:
            embed.add_field(name="Title", value=title, inline=False)
        if description:
            embed.add_field(name="Description", value=description, inline=False)
        if meeting_channel:
            embed.add_field(name="Meeting Channel", value=meeting_channel.mention, inline=False)
        if members:
            members_list = [member.strip() for member in members.split(",")]
            embed.add_field(name="Members", value=", ".join(members_list), inline=False)

        if meeting_notification_channel:
            message = await meeting_notification_channel.send(embed=embed)
        
        discord_members = []
        if members:
            members_list = [member.strip() for member in members.split(",")]
            for member in members_list:
                member_id = int(member.strip()[2:-1])
                member_obj = ctx.guild.get_member(member_id)
                discord_members.append(member_obj)
                if member_obj:
                    try:
                        await member_obj.send(embed=embed)
                    except discord.HTTPException:
                        pass
        
        self.meetings.append({
            "title": title,
            "scheduled_by": ctx.author.id,
            "message": message.id if meeting_notification_channel else None,
        })

        await ctx.respond("Meeting scheduled successfully!", ephemeral=ctx.guild is not None)


    @commands.slash_command(name='meeting_list', description='List all scheduled meetings for you')
    @commands.has_any_role(int(os.getenv('EMPLOYEE_ROLE_ID') or 0), int(os.getenv('ADMIN_ROLE_ID') or 0))
    async def meeting_list(
        self,
        ctx: ApplicationContext,
        private: Option(bool, description="Show publicly in the channel", required=False, default=True),
    ):
        await ctx.defer(ephemeral=private)
        if not self.meetings:
            return await ctx.respond("No meetings scheduled.", ephemeral=private)

        embed = discord.Embed(title="Scheduled Meetings", color=discord.Color.blue())
        for meeting in self.meetings:
            if meeting["scheduled_by"] == ctx.author.id:
                embed.add_field(name="Meeting", value=f"Title: {meeting['title']}\nScheduled By: <@{meeting['scheduled_by']}>\nMessage ID: {meeting['message']}", inline=False)

        await ctx.respond(embed=embed, ephemeral=private)



def setup(bot: discord.Bot):
    bot.add_cog(Employee(bot))
