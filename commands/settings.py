from commands import _embedMessage, _checkrole, _mongoFunctions, _util


async def settings(ctx, client):
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("SetBediBotChannel Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return
    message = _embedMessage.create("Settings Reply", "Here are the settings for **" + ctx.guild.name + "**", "blue")

    _embedMessage.add_field(message, "Timezone", _mongoFunctions.get_settings(ctx.guild.id)['timezone'], False)
    _embedMessage.add_field(message, "Verification Enabled?", _mongoFunctions.get_settings(ctx.guild.id)['verification_enabled'], False)
    _embedMessage.add_field(message, "Bedi Bot Channel", ctx.guild.get_channel(int(_mongoFunctions.get_settings(ctx.guild.id)['channel_id'])).mention, False)
    _embedMessage.add_field(message, "Admin Role", _mongoFunctions.get_settings(ctx.guild.id)['admin_role'], False)
    _embedMessage.add_field(message, "Daily Announcement Time", _mongoFunctions.get_settings(ctx.guild.id)['announcement_time'], False)
    _embedMessage.add_field(message, "Daily Announcement Quote Author", _mongoFunctions.get_settings(ctx.guild.id)['announcement_quoted_person'], False)
    _embedMessage.add_field(message, "Announcement Role", _mongoFunctions.get_settings(ctx.guild.id)['announcement_role'], False)
    _embedMessage.add_field(message, "Birthday Announcement Time", _mongoFunctions.get_settings(ctx.guild.id)['birthday_time'], False)
    _embedMessage.add_field(message, "Birthday Role", _mongoFunctions.get_settings(ctx.guild.id)['birthday_role'], False)
    _embedMessage.add_field(message, "Quote Reaction Emoji Name", _mongoFunctions.get_settings(ctx.guild.id)['reaction_emoji'], False)
    _embedMessage.add_field(message, "Streams", ', '.join(_mongoFunctions.get_settings(ctx.guild.id)['streams']), False)
    _embedMessage.add_field(message, "Courses", ', '.join(_mongoFunctions.get_settings(ctx.guild.id)['courses']), False)
    _embedMessage.add_field(message, "Due Date Types", ', '.join(_mongoFunctions.get_settings(ctx.guild.id)['due_date_types']), False)

    await ctx.channel.send(embed = message)

    return
