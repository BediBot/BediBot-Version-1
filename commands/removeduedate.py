import asyncio
import datetime
import re

from commands import _embedMessage, _mongoFunctions, _dateFunctions, _dueDateMessage, _checkrole


async def remove_due_date(ctx, client):
    global course, due_date_type, stream, time, title, year, month, day
    wait_timeout = 60.0
    if not (_checkrole.author_has_role(ctx, "admin") or _checkrole.author_has_role(ctx, "admins()")):
        await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "Invalid Permissions", "red"))
        return

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    while True:
        await ctx.channel.send(
            embed = _embedMessage.create("RemoveDueDate Reply", "What course is this due date for?\nOptions: " + ', '.join(_mongoFunctions.get_list_of_courses(ctx.guild.id)),
                                         "blue"))
        try:
            course_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "You took too long to respond.", "red"))
            return
        else:
            course = course_message.content
            if course not in _mongoFunctions.get_list_of_courses(ctx.guild.id):
                await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "The course name is invalid!", "red"))
            else:
                break

    while True:
        await ctx.channel.send(
            embed = _embedMessage.create("RemoveDueDate Reply", "What is the due date type?\nOptions: " + ', '.join(_mongoFunctions.get_list_of_due_date_types(ctx.guild.id)),
                                         "blue"))
        try:
            due_date_type_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "You took too long to respond.", "red"))
            return
        else:
            due_date_type = due_date_type_message.content
            if due_date_type not in _mongoFunctions.get_list_of_due_date_types(ctx.guild.id):
                await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "The due date type is invalid!", "red"))
            else:
                break

    if len(_mongoFunctions.get_list_of_streams(ctx.guild.id)) == 1:
        stream = _mongoFunctions.get_list_of_streams(ctx.guild.id)[0]
    else:
        while True:
            await ctx.channel.send(
                embed = _embedMessage.create("RemoveDueDate Reply", "Which stream is this for?\nOptions: " + ', '.join(_mongoFunctions.get_list_of_streams(ctx.guild.id)), "blue"))
            try:
                stream_message = await client.wait_for('message', timeout = wait_timeout, check = check)
            except asyncio.TimeoutError:
                await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "You took too long to respond.", "red"))
                return
            else:
                stream = stream_message.content
                if stream not in _mongoFunctions.get_list_of_streams(ctx.guild.id):
                    await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "The stream is invalid!", "red"))
                else:
                    break

    while True:
        await ctx.channel.send(
            embed = _embedMessage.create("RemoveDueDate Reply", "What is the title?", "blue"))
        try:
            title_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "You took too long to respond.", "red"))
            return
        else:
            title = title_message.content
            break

    while True:
        await ctx.channel.send(
            embed = _embedMessage.create("RemoveDueDate Reply", "What is the date? (YYYY MM DD)", "blue"))
        try:
            date_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "You took too long to respond.", "red"))
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
                await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "Invalid syntax. Make sure it is in the format YYYY MM DD", "red"))
            elif error_check == 2:
                await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "The date is invalid, please ensure that this is a valid date.", "red"))
            else:
                date_object = datetime.date(int(year), int(month), int(day))
                if date_object < datetime.date.today():
                    await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "That due date has already passed.", "red"))
                else:
                    break

    while True:
        await ctx.channel.send(
            embed = _embedMessage.create("RemoveDueDate Reply", "What time is the due date? (HH:MM)\nEnter 'None' if there is no time.", "blue"))
        try:
            time_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "You took too long to respond.", "red"))
            return
        else:
            time = time_message.content
            match = re.match('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', time)

            if time == "None":
                break
            elif not match:
                await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "Invalid syntax. Make sure it is in the format HH:MM or 'None'", "red"))
            else:
                time = time.split(':')
                time_object = datetime.datetime(int(year), int(month), int(day), int(time[0]), int(time[1]))

                if time_object < datetime.datetime.now():
                    await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "That due date has already passed.", "red"))

                else:
                    break

    if time == "None":
        if not _mongoFunctions.does_assignment_exist_already(ctx.guild.id, course, due_date_type, title, stream, datetime.datetime(int(year), int(month), int(day)), False):
            await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "Your due date does not exist!", "red"))
            return

        _mongoFunctions.remove_due_date_from_upcoming_due_dates(ctx.guild.id, course, due_date_type, title, stream, datetime.datetime(int(year), int(month), int(day)), False)
        await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "Your due date has been removed!", "blue"))

    else:
        if type(time) is str:
            time = time.split(':')

        if not _mongoFunctions.does_assignment_exist_already(ctx.guild.id, course, due_date_type, title, stream,
                                                             datetime.datetime(int(year), int(month), int(day), int(time[0]), int(time[1])), True):
            await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "Your due date does not exist!", "red"))
            return

        _mongoFunctions.remove_due_date_from_upcoming_due_dates(ctx.guild.id, course, due_date_type, title, stream,
                                                                datetime.datetime(int(year), int(month), int(day), int(time[0]), int(time[1])), True)
        await ctx.channel.send(embed = _embedMessage.create("RemoveDueDate Reply", "Your due date has been removed!", "blue"))

    await _dueDateMessage.edit_due_date_message(client)
    return
