import asyncio

import discord

from commands import _mongoFunctions, _embedMessage, _util


async def setup_announcement(ctx: discord.Message, client: discord.Client):
    # How long to wait for user response before timeout
    wait_timeout = 60.0

    stop_embed = _embedMessage.create("SetupAnnouncement Reply", "Setup Stopped", "green")

    # Checks if user is admin or bot owner
    if not (ctx.author.guild_permissions.administrator or _util.author_is_bot_owner(ctx)):
        await ctx.channel.send(embed = _embedMessage.create("SetupAnnouncement Reply", "Invalid Permissions", "red"))
        return

    try:
        _mongoFunctions.get_guilds_information()[str(ctx.guild.id)]
    except KeyError:
        _mongoFunctions.generate_default_settings(ctx.guild.id)

    # Checking function to determine if responses are sent by initial user in initial channel
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    response_message = await ctx.channel.send(embed = _embedMessage.create("SetupAnnouncement Reply", "Should Morning Announcements be Enabled (y/n)?", "blue"))

    while True:
        await response_message.edit(embed = _embedMessage.create("SetupAnnouncement Reply", "Should Morning Announcements be Enabled (y/n)?", "blue"))
        try:
            morning_announcements_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("SetupAnnouncement Reply", "You took too long to respond.", "red"))
            return
        else:
            morning_announcements_string = morning_announcements_message.content.lower()
            if morning_announcements_string == 'next':
                break
            if morning_announcements_string == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            if morning_announcements_string in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
                _mongoFunctions.update_setting(ctx.guild.id, "morning_announcements_enabled", True)
            else:
                _mongoFunctions.update_setting(ctx.guild.id, "morning_announcements_enabled", False)

            break

    while True:
        await response_message.edit(embed = _embedMessage.create("SetupAnnouncement Reply", "What is the morning announcement channel?", "blue"))
        try:
            announcement_channel_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("SetupAnnouncement Reply", "You took too long to respond.", "red"))
            return
        else:
            announcement_channel_string = announcement_channel_message.content
            if announcement_channel_string.lower() == 'next':
                break
            if announcement_channel_string.lower() == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            announcement_channel_id = discord.utils.get(ctx.guild.channels, mention = announcement_channel_string).id
            _mongoFunctions.update_setting(ctx.guild.id, "announcement_channel_id", announcement_channel_id)
            break

    while True:
        await response_message.edit(embed = _embedMessage.create("SetupAnnouncement Reply", "What is the morning announcement time (HH:MM)?", "blue"))
        try:
            announcement_time_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("SetupAnnouncement Reply", "You took too long to respond.", "red"))
            return
        else:
            announcement_time_string = announcement_time_message.content
            if announcement_time_string.lower() == 'next':
                break
            if announcement_time_string.lower() == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            _mongoFunctions.update_setting(ctx.guild.id, "announcement_time", announcement_time_string)
            break

    while True:
        await response_message.edit(embed = _embedMessage.create("SetupAnnouncement Reply", "Who should be quoted in the morning announcement?", "blue"))
        try:
            announcement_quoted_person_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("SetupAnnouncement Reply", "You took too long to respond.", "red"))
            return
        else:
            announcement_quoted_person = announcement_quoted_person_message.content
            if announcement_quoted_person.lower() == 'next':
                break
            if announcement_quoted_person.lower() == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            _mongoFunctions.update_setting(ctx.guild.id, "announcement_quoted_person", announcement_quoted_person)
            break

    await ctx.channel.send(embed = _embedMessage.create("SetupAnnouncement Reply", "Announcement Setup has been Completed", "blue"))
