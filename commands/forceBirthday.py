from commands import _birthdayMessage, _mongoFunctions, _checkrole, _embedMessage, _util


async def force_birthdays(ctx, client):
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("ForceBirthdays Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    await _birthdayMessage.send_birthday_message(client, ctx.guild.id, _mongoFunctions.get_settings(ctx.guild.id)['channel_id'])
    await ctx.channel.send(embed = _embedMessage.create("ForceBirthdays Reply", "Birthdays have been Forced", "blue"))
    return
