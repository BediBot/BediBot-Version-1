import datetime
import enum
import re

import discord

from commands import _embedMessage, _mongoFunctions, _dateFunctions, _dueDateMessage, _checkrole


async def addduedate(ctx, client):
    if not _checkrole.checkIfAuthorHasRole(ctx, "admin"):
        await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "Invalid Permissions", "red"))
        return

    message_contents = ctx.content.split(" ", 1)
    message_contents.pop(0)

    message_contents = message_contents[0].split(' ')

    if len(message_contents) > 8:

        description = [' '.join(message_contents[0:2]), message_contents[2], ' '.join(message_contents[3:-5])]

        stream = message_contents[-5]

        date = message_contents[-4:-1]

        time = message_contents[-1]

        course = description[0]
        due_date_type = description[1]
        title = description[2]
        year = date[0]
        month = date[1]
        day = date[2]

        error_check = _dateFunctions.check_for_errors_in_date(year, month, day)
    else:
        error_check = 1

    if course not in _mongoFunctions.get_list_of_courses(ctx.guild.id):
        error_check = 3

    if due_date_type not in _mongoFunctions.get_list_of_due_date_types(ctx.guild.id):
        error_check = 4

    if stream not in _mongoFunctions.get_list_of_streams(ctx.guild.id):
        error_check = 5

    if error_check == 1:
        await ctx.channel.send(
            embed = _embedMessage.create("AddDueDate Reply", "The syntax is invalid! Make sure it is in the format $addduedate course type title stream YYYY MM DD HH:MM"
                                                             "\n If there is no related time, enter none instead of HH:MM. Time in 24 hour format"
                                                             "\n Ensure there is a space in between the course name: eg. MTE 100", "red"))
        return
    if error_check == 2:
        await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "The date is invalid, please ensure that this is a valid date.", "red"))
        return
    if error_check == 3:
        await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "The course name is invalid!", "red"))
        return
    if error_check == 4:
        await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "The due date type is invalid!", "red"))
        return
    if error_check == 5:
        await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "The stream is invalid!", "red"))
        return

    match = re.match('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', time)

    if not match:
        time = None

    if time == None:
        if _mongoFunctions.does_assignment_exist_already(ctx.guild.id, course, due_date_type, title, stream, datetime.datetime(int(year), int(month), int(day)), False):
            await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "Your due date already exists!", "red"))
            return

        _mongoFunctions.add_due_date_to_upcoming_due_dates(ctx.guild.id, course, due_date_type, title, stream, datetime.datetime(int(year), int(month), int(day)), False)
        await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "Your due date has been added!", "blue"))

    else:
        time = time.split(':')

        if _mongoFunctions.does_assignment_exist_already(ctx.guild.id, course, due_date_type, title, stream,
                                                         datetime.datetime(int(year), int(month), int(day), int(time[0]), int(time[1])), True):
            await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "Your due date already exists!", "red"))
            return

        _mongoFunctions.add_due_date_to_upcoming_due_dates(ctx.guild.id, course, due_date_type, title, stream,
                                                           datetime.datetime(int(year), int(month), int(day), int(time[0]), int(time[1])), True)
        await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "Your due date has been added!", "blue"))

    await _dueDateMessage.edit_due_date_message(client)

    return
