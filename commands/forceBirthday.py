from commands import _birthdayMessage, _mongoFunctions, _checkrole, _embedMessage


async def force_birthdays(ctx, client):
    if not (_checkrole.author_has_role(ctx, "admin") or _checkrole.author_has_role(ctx, "admins()")):
        replyEmbed = _embedMessage.create("SetBediBotChannel Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    await _birthdayMessage.send_birthday_message(client, ctx.guild.id, _mongoFunctions.get_bedi_bot_channel_id(ctx.guild.id))
    await ctx.channel.send(embed = _embedMessage.create("ForceBirthdays Reply", "Birthdays have been Forced", "blue"))
    return
