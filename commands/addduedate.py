import datetime

import discord

from commands import _embedMessage, _mongoFunctions, _dateFunctions


async def addduedate(ctx):
	if discord.utils.get(ctx.guild.roles, name = "admin") not in ctx.author.roles:
		await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "You are not an admin", "blue"))
		return

	message_contents = ctx.content.split(" ", 1)
	message_contents.pop(0)

	message_contents = message_contents[0].split(' ')

	description = message_contents[0:2]

	description.append(' '.join(message_contents[2:-3]))

	date = message_contents[-3:]

	if len(description) == 3 and len(date) == 3:
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
		await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "The syntax is invalid! Make sure it is in the format $addduedate type title YYYY MM DD", "blue"))
		return
	if error_check == 2:
		await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "The date is invalid, please ensure that this is a valid date.", "blue"))
		return

	due_date_string = '-'.join(date)

	await ctx.channel.send(embed = _embedMessage.create("AddDueDate Reply", "Your due date has been added!", "blue"))

	_mongoFunctions.add_due_date_to_upcoming_due_dates(course, due_date_type, title, datetime.datetime.strptime(due_date_string, "%Y-%m-%d"))

	return
