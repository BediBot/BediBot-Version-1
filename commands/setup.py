import asyncio

import discord

from commands import _mongoFunctions, _embedMessage, _util
from commands.settings import settings


async def setup(ctx: discord.Message, client: discord.Client):
    # How long to wait for user response before timeout
    wait_timeout = 60.0

    stop_embed = _embedMessage.create("Setup Reply", "Setup Stopped", "green")

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

    response_message = await ctx.channel.send(
        embed = _embedMessage.create("Setup Reply", "What should the prefix be (Default: $)? For any of these settings, if you wish to keep the current setting, type 'next'. "
                                                    "If you wish to stop the command at any time, type 'stop'.",
                                     "blue"))

    while True:
        await response_message.edit(embed = _embedMessage.create("Setup Reply", "What should the prefix be (Default: $)? For any of these settings, "
                                                                                "if you wish to keep the current setting, type 'next'.", "blue"))
        try:
            prefix_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
            return
        else:
            prefix = prefix_message.content
            if prefix.lower() == 'next':
                break
            if prefix.lower() == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            _mongoFunctions.update_setting(ctx.guild.id, "prefix", prefix)
            break

    while True:
        await response_message.edit(embed = _embedMessage.create("Setup Reply", "What is the admin role?", "blue"))
        try:
            admin_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
            return
        else:
            admin_role_string = admin_message.content
            if admin_role_string.lower() == 'next':
                break
            if admin_role_string.lower() == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            _mongoFunctions.update_setting(ctx.guild.id, "admin_role", admin_role_string)
            break

    while True:
        await response_message.edit(embed = _embedMessage.create("Setup Reply", "Should Verification be Enabled (y/n)?", "blue"))
        try:
            verification_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
            return
        else:
            verification_string = verification_message.content.lower()
            if verification_string == 'next':
                break
            if verification_string == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            if verification_string in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
                _mongoFunctions.update_setting(ctx.guild.id, "verification_enabled", True)

            else:
                _mongoFunctions.update_setting(ctx.guild.id, "verification_enabled", False)
            break

    if _mongoFunctions.get_settings(ctx.guild.id)["verification_enabled"]:
        while True:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "What is the verified role?", "blue"))
            try:
                verified_role_message = await client.wait_for('message', timeout = wait_timeout, check = check)
            except asyncio.TimeoutError:
                await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
                return
            else:
                verified_role_string = verified_role_message.content
                if verified_role_string.lower() == 'next':
                    break
                if verified_role_string.lower() == 'stop':
                    await ctx.channel.send(embed = stop_embed)
                    return
                _mongoFunctions.update_setting(ctx.guild.id, "verified_role", verified_role_string)
                break

        while True:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "What is the verification email domain? (E.g. @uwaterloo.ca)", "blue"))
            try:
                email_domain_message = await client.wait_for('message', timeout = wait_timeout, check = check)
            except asyncio.TimeoutError:
                await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
                return
            else:
                email_domain = email_domain_message.content
                if email_domain.lower() == 'next':
                    break
                if email_domain.lower() == 'stop':
                    await ctx.channel.send(embed = stop_embed)
                    return
                _mongoFunctions.update_setting(ctx.guild.id, "email_domain", email_domain)
                break

    while True:
        await response_message.edit(embed = _embedMessage.create("Setup Reply", "Should Morning Announcements be Enabled (y/n)?", "blue"))
        try:
            morning_announcements_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
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

    if _mongoFunctions.get_settings(ctx.guild.id)["morning_announcements_enabled"]:
        while True:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "What is the morning announcement channel?", "blue"))
            try:
                announcement_channel_message = await client.wait_for('message', timeout = wait_timeout, check = check)
            except asyncio.TimeoutError:
                await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
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
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "What is the morning announcement time (HH:MM)?", "blue"))
            try:
                announcement_time_message = await client.wait_for('message', timeout = wait_timeout, check = check)
            except asyncio.TimeoutError:
                await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
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
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "Who should be quoted in the morning announcement?", "blue"))
            try:
                announcement_quoted_person_message = await client.wait_for('message', timeout = wait_timeout, check = check)
            except asyncio.TimeoutError:
                await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
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

    while True:
        await response_message.edit(embed = _embedMessage.create("Setup Reply", "What is the quote reaction emoji name? "
                                                                                "(Must be a custom emoji, enter the name without the : characters)", "blue"))
        try:
            reaction_emoji_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
            return
        else:
            reaction_emoji_string = reaction_emoji_message.content
            if reaction_emoji_string.lower() == 'next':
                break
            if reaction_emoji_string.lower() == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            _mongoFunctions.update_setting(ctx.guild.id, "reaction_emoji", reaction_emoji_string)
            break

    while True:
        await response_message.edit(embed = _embedMessage.create("Setup Reply", "How many approvals should be required to approve a quote. (Minimum of 2)", "blue"))
        try:
            reaction_number_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
            return
        else:
            reaction_number_string = reaction_number_message.content
            if reaction_number_string.lower() == 'next':
                break
            if reaction_number_string.lower() == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            _mongoFunctions.update_setting(ctx.guild.id, "required_quote_reactions", int(reaction_number_string))
            break

    await ctx.channel.send(embed = _embedMessage.create("Setup Reply", "Guild has been setup. Make sure to run {0}setduedatechannel in a view-only channel if needed.".format(
        _mongoFunctions.get_settings(ctx.guild.id)['prefix']), "blue"))
    await settings(ctx, client)
