import asyncio

import discord

from commands import _checkrole, _mongoFunctions, _embedMessage, _util


async def setup(ctx: discord.Message, client: discord.Client):
    # How long to wait for user response before timeout
    wait_timeout = 60.0

    # Checks if user is admin or bot owner
    if not (ctx.author.guild_permissions.administrator or _util.author_is_bot_owner(ctx)):
        await ctx.channel.send(embed = _embedMessage.create("Setup Reply", "Invalid Permissions", "red"))
        return

    # Checking function to determine if responses are sent by initial user in initial channel
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    response_message = await ctx.channel.send(embed = _embedMessage.create("Setup Reply", "What is the admin role?", "blue"))

    while True:
        await response_message.edit(embed = _embedMessage.create("Setup Reply", "What is the admin role?", "blue"))
        try:
            admin_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
            return
        else:
            admin_role_string = admin_message.content
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
            if verification_string in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
                _mongoFunctions.update_setting(ctx.guild.id, "verification_enabled", True)

                while True:
                    await response_message.edit(embed = _embedMessage.create("Setup Reply", "What is the verified role?", "blue"))
                    try:
                        verified_role_message = await client.wait_for('message', timeout = wait_timeout, check = check)
                    except asyncio.TimeoutError:
                        await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
                        return
                    else:
                        verified_role_string = verified_role_message.content
                        _mongoFunctions.update_setting(ctx.guild.id, "verified_role", verified_role_string)
                        break

            else:
                _mongoFunctions.update_setting(ctx.guild.id, "verification_enabled", False)
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
            if morning_announcements_string in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
                _mongoFunctions.update_setting(ctx.guild.id, "morning_announcements_enabled", True)

                while True:
                    await response_message.edit(embed = _embedMessage.create("Setup Reply", "What is the morning announcement time (HH:MM)?", "blue"))
                    try:
                        announcement_time_message = await client.wait_for('message', timeout = wait_timeout, check = check)
                    except asyncio.TimeoutError:
                        await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
                        return
                    else:
                        announcement_time_string = announcement_time_message.content
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
                        _mongoFunctions.update_setting(ctx.guild.id, "announcement_quoted_person", announcement_quoted_person)
                        break

                while True:
                    await response_message.edit(embed = _embedMessage.create("Setup Reply",
                                                                             "What is the morning announcement role? (This role will be tagged in every announcement. "
                                                                             "Think of it as a subscription role.)",
                                                                             "blue"))
                    try:
                        announcement_role_message = await client.wait_for('message', timeout = wait_timeout, check = check)
                    except asyncio.TimeoutError:
                        await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
                        return
                    else:
                        announcement_role_string = announcement_role_message.content
                        _mongoFunctions.update_setting(ctx.guild.id, "announcement_role", announcement_role_string)
                        break
            else:
                _mongoFunctions.update_setting(ctx.guild.id, "morning_announcements_enabled", False)

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
            if birthday_announcements_string in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
                _mongoFunctions.update_setting(ctx.guild.id, "birthday_announcements_enabled", True)

                while True:
                    await response_message.edit(embed = _embedMessage.create("Setup Reply", "What is the birthday announcement time (HH:MM)? Most would do 00:00 here.", "blue"))
                    try:
                        birthday_time_message = await client.wait_for('message', timeout = wait_timeout, check = check)
                    except asyncio.TimeoutError:
                        await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
                        return
                    else:
                        birthday_time_string = birthday_time_message.content
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
                        _mongoFunctions.update_setting(ctx.guild.id, "birthday_role", birthday_role_string)
                        break
            else:
                _mongoFunctions.update_setting(ctx.guild.id, "birthday_announcements_enabled", False)
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
            if due_dates_string in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
                _mongoFunctions.update_setting(ctx.guild.id, "due_dates_enabled", True)

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
                        due_date_types = due_date_types_string.split(' ')
                        _mongoFunctions.update_setting(ctx.guild.id, "due_date_types", due_date_types)
                        break
            else:
                _mongoFunctions.update_setting(ctx.guild.id, "due_dates_enabled", False)
            break

    await response_message.edit(embed = _embedMessage.create("Setup Reply", "Guild has been setup. Make sure to run $setbedibotchannel if needed.", "blue"))
