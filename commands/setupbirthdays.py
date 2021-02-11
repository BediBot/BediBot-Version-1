import asyncio

import discord

from commands import _mongoFunctions, _embedMessage, _util

# How long to wait for user response before timeout
wait_timeout = 60.0


async def setup_birthdays(ctx: discord.Message, client: discord.Client):
    stop_embed = _embedMessage.create("SetupBirthdays Reply", "Setup Stopped", "green")

    # Checks if user is admin or bot owner
    if not (ctx.author.guild_permissions.administrator or _util.author_is_bot_owner(ctx)):
        await ctx.channel.send(embed = _embedMessage.create("SetupBirthdays Reply", "Invalid Permissions", "red"))
        return

    try:
        _mongoFunctions.get_guilds_information()[str(ctx.guild.id)]
    except KeyError:
        _mongoFunctions.generate_default_settings(ctx.guild.id)

    # Checking function to determine if responses are sent by initial user in initial channel
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    response_message = await ctx.channel.send(embed = _embedMessage.create("SetupBirthdays Reply", "Should Birthday Announcements be Enabled (y/n)?", "blue"))

    await set_settings(ctx, client, response_message, stop_embed, check)

    await ctx.channel.send(embed = _embedMessage.create("SetupBirthdays Reply", "Birthdays Setup has been Completed", "blue"))


async def set_settings(ctx: discord.Message, client: discord.Client, response_message: discord.Message, stop_embed: discord.embeds, check):
    while True:
        await response_message.edit(embed = _embedMessage.create("Setup Reply", "Should Birthday Announcements be Enabled (y/n)?", "blue"))
        try:
            birthday_announcements_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
            return
        else:
            birthday_announcements_string = birthday_announcements_message.content.lower()
            if birthday_announcements_string == 'next':
                break
            if birthday_announcements_string == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            if birthday_announcements_string in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
                _mongoFunctions.update_setting(ctx.guild.id, "birthday_announcements_enabled", True)
            else:
                _mongoFunctions.update_setting(ctx.guild.id, "birthday_announcements_enabled", False)
            break

    await asyncio.sleep(0.5)

    if _mongoFunctions.get_settings(ctx.guild.id)["birthday_announcements_enabled"]:
        while True:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "What is the birthday announcement channel?", "blue"))
            try:
                birthday_channel_message = await client.wait_for('message', timeout = wait_timeout, check = check)
            except asyncio.TimeoutError:
                await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
                return
            else:
                birthday_channel_string = birthday_channel_message.content
                if birthday_channel_string.lower() == 'next':
                    break
                if birthday_channel_string.lower() == 'stop':
                    await ctx.channel.send(embed = stop_embed)
                    return
                birthday_channel_id = discord.utils.get(ctx.guild.channels, mention = birthday_channel_string).id
                _mongoFunctions.update_setting(ctx.guild.id, "birthday_channel_id", birthday_channel_id)
                break

        while True:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "What is the birthday announcement time (HH:MM)? Most would do 00:00 here.", "blue"))
            try:
                birthday_time_message = await client.wait_for('message', timeout = wait_timeout, check = check)
            except asyncio.TimeoutError:
                await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
                return
            else:
                birthday_time_string = birthday_time_message.content
                if birthday_time_string.lower() == 'next':
                    break
                if birthday_time_string.lower() == 'stop':
                    await ctx.channel.send(embed = stop_embed)
                    return
                _mongoFunctions.update_setting(ctx.guild.id, "birthday_time", birthday_time_string)
                break

        while True:
            await response_message.edit(embed = _embedMessage.create("Setup Reply",
                                                                     "What is the birthday announcement role? (This role must be below BediBot's highest role. "
                                                                     "You may want to display this role separately from online members.)",
                                                                     "blue"))
            try:
                birthday_role_message = await client.wait_for('message', timeout = wait_timeout, check = check)
            except asyncio.TimeoutError:
                await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
                return
            else:
                birthday_role_string = birthday_role_message.content
                if birthday_role_string.lower() == 'next':
                    break
                if birthday_role_string.lower() == 'stop':
                    await ctx.channel.send(embed = stop_embed)
                    return
                _mongoFunctions.update_setting(ctx.guild.id, "birthday_role", birthday_role_string)
                break
