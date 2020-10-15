import datetime
import enum
import re

import discord

from commands import _embedMessage, _mongoFunctions, _dateFunctions, _dueDateMessage


async def addduedate(ctx, client):
    if discord.utils.get(ctx.guild.roles, name = "admin") not in ctx.author.roles:
        await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "You are not an admin", "blue"))
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

    if error_check == 1:
        await ctx.channel.send(
            embed = _embedMessage.create("AddDueDate Reply", "The syntax is invalid! Make sure it is in the format $addduedate course type title stream YYYY MM DD HH:MM"
                                                             "\n If there is no related time, enter none instead of HH:MM. Time in 24 hour format", "blue"))
        return
    if error_check == 2:
        await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "The date is invalid, please ensure that this is a valid date.", "blue"))
        return

    await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "Your due date has been added!", "blue"))

    match = re.match('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', time)

    if not match:
        time = None

    if time == None:
        _mongoFunctions.add_due_date_to_upcoming_due_dates(ctx.guild.id, course, due_date_type, title, stream,
                                                           datetime.datetime(int(year), int(month), int(day)), False)

    else:
        time = time.split(':')

        _mongoFunctions.add_due_date_to_upcoming_due_dates(ctx.guild.id, course, due_date_type, title, stream,
                                                           datetime.datetime(int(year), int(month), int(day), int(time[0]), int(time[1])), True)

    await _dueDateMessage.edit_due_date_message(client)

    return
