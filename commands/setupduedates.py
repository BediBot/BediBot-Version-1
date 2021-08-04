import asyncio

import discord

from commands import _mongoFunctions, _embedMessage, _util

# How long to wait for user response before timeout
wait_timeout = 60.0


async def setup_due_dates(ctx: discord.Message, client: discord.Client):
    stop_embed = _embedMessage.create("SetupDueDates Reply", "Setup Stopped", "green")

    # Checks if user is admin or bot owner
    if not (ctx.author.guild_permissions.administrator or _util.author_is_bot_owner(ctx)):
        await ctx.channel.send(embed = _embedMessage.create("Setup Reply", "Invalid Permissions", "red"))
        return

    try:
        _mongoFunctions.get_guilds_information()[str(ctx.guild.id)]
    except KeyError:
        _mongoFunctions.generate_default_settings(ctx.guild.id)

    # Checking function to determine if responses are sent by initial user in initial channel
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    response_message = await ctx.channel.send(embed = _embedMessage.create("Setup Reply", "Should Due Dates be Enabled (y/n)?", "blue"))

    await set_settings(ctx, client, response_message, stop_embed, check)

    await ctx.channel.send(embed = _embedMessage.create("Setup Reply", "DueDate Setup has been Completed", "blue"))


async def set_settings(ctx: discord.Message, client: discord.Client, response_message: discord.Message, stop_embed: discord.embeds, check):
    while True:
        await response_message.edit(embed = _embedMessage.create("Setup Reply", "Should Due Dates be Enabled (y/n)?", "blue"))
        try:
            due_dates_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
            return
        else:
            due_dates_string = due_dates_message.content.lower()
            if due_dates_string == 'next':
                break
            if due_dates_string == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            if due_dates_string in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
                _mongoFunctions.update_setting(ctx.guild.id, "due_dates_enabled", True)

            else:
                _mongoFunctions.update_setting(ctx.guild.id, "due_dates_enabled", False)
            break

    await asyncio.sleep(0.5)

    if _mongoFunctions.get_settings(ctx.guild.id)["due_dates_enabled"]:
        while True:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "Which streams require due dates? (Must be integers separated by spaces."
                                                                                    "E.g. 4 8)", "blue"))
            try:
                streams_message = await client.wait_for('message', timeout = wait_timeout, check = check)
            except asyncio.TimeoutError:
                await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
                return
            else:
                streams_string = streams_message.content
                if streams_string.lower() == 'next':
                    break
                if streams_string.lower() == 'stop':
                    await ctx.channel.send(embed = stop_embed)
                    return
                streams = streams_string.split(' ')
                _mongoFunctions.update_setting(ctx.guild.id, "streams", streams)
                break

        while True:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "What are the term's courses. (Or other deadline categories). "
                                                                                    "(Must be strings separated by spaces. "
                                                                                    "Use quotes around courses made of multiple words) "
                                                                                    "E.g. \"MATH 115\" Physics)", "blue"))
            try:
                courses_message = await client.wait_for('message', timeout = wait_timeout, check = check)
            except asyncio.TimeoutError:
                await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
                return
            else:
                courses_string = courses_message.content
                if courses_string.lower() == 'next':
                    break
                if courses_string.lower() == 'stop':
                    await ctx.channel.send(embed = stop_embed)
                    return
                courses = _util.parse_message(courses_string)
                _mongoFunctions.update_setting(ctx.guild.id, "courses", courses)
                break

        while True:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "What are the due date types. "
                                                                                    "(Must be strings separated by spaces. "
                                                                                    "E.g. Assignment Test Quiz Exam Project Other)", "blue"))
            try:
                due_date_types_message = await client.wait_for('message', timeout = wait_timeout, check = check)
            except asyncio.TimeoutError:
                await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
                return
            else:
                due_date_types_string = due_date_types_message.content
                if due_date_types_string.lower() == 'next':
                    break
                if due_date_types_string.lower() == 'stop':
                    await ctx.channel.send(embed = stop_embed)
                    return
                due_date_types = due_date_types_string.split(' ')
                _mongoFunctions.update_setting(ctx.guild.id, "due_date_types", due_date_types)
                break
