import asyncio
import datetime
import re

from commands import _embedMessage, _mongoFunctions, _dateFunctions, _dueDateMessage, _checkrole, _util


async def add_due_date(ctx, client):
    global course, due_date_type, stream, time, title, year, month, day
    wait_timeout = 60.0
    sleep_time = 2
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "Invalid Permissions", "red"))
        return

    if not _mongoFunctions.get_settings(ctx.guild.id)['due_dates_enabled']:
        await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "Due Dates are not enabled on this server.", "red"))
        return

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    response_message = await ctx.channel.send(
        embed = _embedMessage.create("AddDueDate Reply", "What course is this due date for?\nOptions: " + ', '.join(_mongoFunctions.get_settings(ctx.guild.id)['courses']), "blue"))

    while True:
        await response_message.edit(
            embed = _embedMessage.create("AddDueDate Reply", "What course is this due date for?\nOptions: " + ', '.join(_mongoFunctions.get_settings(ctx.guild.id)['courses']),
                                         "blue"))
        try:
            course_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "You took too long to respond.", "red"))
            return
        else:
            course = course_message.content
            if course not in _mongoFunctions.get_settings(ctx.guild.id)['courses']:
                await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "The course name is invalid!", "red"))
                await asyncio.sleep(sleep_time)
            else:
                break

    while True:
        await response_message.edit(
            embed = _embedMessage.create("AddDueDate Reply", "What is the due date type?\nOptions: " + ', '.join(_mongoFunctions.get_settings(ctx.guild.id)['due_date_types']),
                                         "blue"))
        try:
            due_date_type_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "You took too long to respond.", "red"))
            return
        else:
            due_date_type = due_date_type_message.content
            if due_date_type not in _mongoFunctions.get_settings(ctx.guild.id)['due_date_types']:
                await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "The due date type is invalid!", "red"))
                await asyncio.sleep(sleep_time)
            else:
                break

    if len(_mongoFunctions.get_settings(ctx.guild.id)['streams']) == 1:
        stream = _mongoFunctions.get_settings(ctx.guild.id)['streams'][0]
    else:
        while True:
            await response_message.edit(
                embed = _embedMessage.create("AddDueDate Reply", "Which stream is this for?\nOptions: " + ', '.join(_mongoFunctions.get_settings(ctx.guild.id)['streams']), "blue"))
            try:
                stream_message = await client.wait_for('message', timeout = wait_timeout, check = check)
            except asyncio.TimeoutError:
                await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "You took too long to respond.", "red"))
                return
            else:
                stream = stream_message.content
                if stream not in _mongoFunctions.get_settings(ctx.guild.id)['streams']:
                    await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "The stream is invalid!", "red"))
                    await asyncio.sleep(sleep_time)
                else:
                    break

    while True:
        await response_message.edit(
            embed = _embedMessage.create("AddDueDate Reply", "What is the title?", "blue"))
        try:
            title_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "You took too long to respond.", "red"))
            return
        else:
            title = title_message.content
            break

    while True:
        await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "What is the date? (YYYY MM DD)", "blue"))
        try:
            date_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "You took too long to respond.", "red"))
            return
        else:
            global error_check
            date = date_message.content.split(" ")
            if len(date) == 3:
                year = date[0]
                month = date[1]
                day = date[2]
                error_check = _dateFunctions.check_for_errors_in_date(year, month, day)
            else:
                error_check = 1
            if error_check == 1:
                await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "Invalid syntax. Make sure it is in the format YYYY MM DD", "red"))
                await asyncio.sleep(sleep_time)
            elif error_check == 2:
                await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "The date is invalid, please ensure that this is a valid date.", "red"))
                await asyncio.sleep(sleep_time)
            else:
                date_object = datetime.date(int(year), int(month), int(day))
                if date_object < datetime.date.today():
                    await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "That due date has already passed.", "red"))
                    await asyncio.sleep(sleep_time)
                else:
                    break

    while True:
        await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "What time is the due date? (HH:MM)\nEnter 'None' if there is no time.", "blue"))
        try:
            time_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "You took too long to respond.", "red"))
            return
        else:
            time = time_message.content
            match = re.match('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', time)  # Using regex to check if time format is valid

            if time == "None":
                break
            elif not match:
                await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "Invalid syntax. Make sure it is in the format HH:MM or 'None'", "red"))
                await asyncio.sleep(sleep_time)
            else:
                time = time.split(':')
                time_object = datetime.datetime(int(year), int(month), int(day), int(time[0]), int(time[1]))
                if time_object < datetime.datetime.now():
                    await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "That due date has already passed.", "red"))
                    await asyncio.sleep(sleep_time)
                else:
                    break

    if time == "None":
        if _mongoFunctions.does_assignment_exist_already(ctx.guild.id, course, due_date_type, title, stream, datetime.datetime(int(year), int(month), int(day)), False):
            await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "Your due date already exists!", "red"))
            return

        _mongoFunctions.add_due_date_to_upcoming_due_dates(ctx.guild.id, course, due_date_type, title, stream, datetime.datetime(int(year), int(month), int(day)), False)
        await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "Your due date has been added!", "blue"))

    else:
        if type(time) is str:
            time = time.split(':')

        if _mongoFunctions.does_assignment_exist_already(ctx.guild.id, course, due_date_type, title, stream,
                                                         datetime.datetime(int(year), int(month), int(day), int(time[0]), int(time[1])), True):
            await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "Your due date already exists!", "red"))
            return

        _mongoFunctions.add_due_date_to_upcoming_due_dates(ctx.guild.id, course, due_date_type, title, stream,
                                                           datetime.datetime(int(year), int(month), int(day), int(time[0]), int(time[1])), True)
        await response_message.edit(embed = _embedMessage.create("AddDueDate Reply", "Your due date has been added!", "blue"))

    await _dueDateMessage.edit_due_date_message(client)
    return
