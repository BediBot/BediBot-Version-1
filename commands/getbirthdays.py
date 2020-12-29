import calendar

import discord

from commands import _embedMessage, _util, _mongoFunctions


async def get_birthdays(ctx, client):
    args = _util.parse_message(ctx.content)

    if len(args) != 2:
        await ctx.channel.send(embed = _embedMessage.create("GetBirthdays Reply", "Invalid Syntax! You need one arguments for this function!", "red"))
        return

    if int(args[1]) > 12 or int(args[1]) < 1:
        await ctx.channel.send(embed = _embedMessage.create("GetBirthdays Reply", "Pick a month from 1 to 12", "red"))
        return

    message_embed = _embedMessage.create("GetBirthdays Reply", "Here are the Birthdays for " + calendar.month_name[int(args[1])], "blue")

    user_documents = _mongoFunctions.get_birthdays_from_month(args[1])

    for document in user_documents:
        member = discord.utils.get(ctx.guild.members, id = document['user_id'])
        if member is None:
            continue

        _embedMessage.add_field(message_embed, document['birth_date'].strftime("%d %B, %Y"), member.mention, False)

    await ctx.channel.send(embed = message_embed)

    return
