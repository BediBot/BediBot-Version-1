import discord

from commands import _embedMessage, _checkrole, _mongoFunctions, _util


async def settings(ctx: discord.Message, client: discord.Client):
    # Checks if user is admin or bot owner
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("Settings Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    message = _embedMessage.create("Settings Reply", "Here are the settings for **" + ctx.guild.name + "**", "blue")

    _embedMessage.add_field(message, "Prefix", _mongoFunctions.get_settings(ctx.guild.id)['prefix'], False)

    _embedMessage.add_field(message, "Timezone", _mongoFunctions.get_settings(ctx.guild.id)['timezone'], False)

    _embedMessage.add_field(message, "Admin Role", _mongoFunctions.get_settings(ctx.guild.id)['admin_role'], False)

    _embedMessage.add_field(message, "Verification Enabled?", _mongoFunctions.get_settings(ctx.guild.id)['verification_enabled'], False)
    if _mongoFunctions.get_settings(ctx.guild.id)['verification_enabled']:
        _embedMessage.add_field(message, "Verified Role", _mongoFunctions.get_settings(ctx.guild.id)['verified_role'], False)
        _embedMessage.add_field(message, "Verification Email Domain", _mongoFunctions.get_settings(ctx.guild.id)['email_domain'], False)

    _embedMessage.add_field(message, "Morning Announcements Enabled?", _mongoFunctions.get_settings(ctx.guild.id)['morning_announcements_enabled'], False)
    if _mongoFunctions.get_settings(ctx.guild.id)['morning_announcements_enabled']:
        try:
            channel_name = ctx.guild.get_channel(int(_mongoFunctions.get_settings(ctx.guild.id)['announcement_channel_id'])).mention
        except:
            channel_name = "Not set. Run {0}setup to set.".format(_mongoFunctions.get_settings(ctx.guild.id)['prefix'])

        _embedMessage.add_field(message, "Morning Announcements Channel", channel_name, False)
        _embedMessage.add_field(message, "Daily Announcement Time", _mongoFunctions.get_settings(ctx.guild.id)['announcement_time'], False)
        _embedMessage.add_field(message, "Daily Announcement Quote Author", _mongoFunctions.get_settings(ctx.guild.id)['announcement_quoted_person'], False)

    _embedMessage.add_field(message, "Birthday Announcements Enabled?", _mongoFunctions.get_settings(ctx.guild.id)['birthday_announcements_enabled'], False)
    if _mongoFunctions.get_settings(ctx.guild.id)['birthday_announcements_enabled']:
        try:
            channel_name = ctx.guild.get_channel(int(_mongoFunctions.get_settings(ctx.guild.id)['birthday_channel_id'])).mention
        except:
            channel_name = "Not set. Run {0}setup to set.".format(_mongoFunctions.get_settings(ctx.guild.id)['prefix'])

        _embedMessage.add_field(message, "Birthday Announcements Channel", channel_name, False)
        _embedMessage.add_field(message, "Birthday Announcement Time", _mongoFunctions.get_settings(ctx.guild.id)['birthday_time'], False)
        _embedMessage.add_field(message, "Birthday Role", _mongoFunctions.get_settings(ctx.guild.id)['birthday_role'], False)

    _embedMessage.add_field(message, "Due Dates Enabled?", _mongoFunctions.get_settings(ctx.guild.id)['due_dates_enabled'], False)
    if _mongoFunctions.get_settings(ctx.guild.id)['due_dates_enabled']:
        try:
            channel_name = ctx.guild.get_channel(int(_mongoFunctions.get_settings(ctx.guild.id)['due_date_channel_id'])).mention
        except:
            channel_name = "Not set. Run {0}setduedatechannel in a channel to set.".format(_mongoFunctions.get_settings(ctx.guild.id)['prefix'])

        _embedMessage.add_field(message, "Due Date Channel", channel_name, False)
        _embedMessage.add_field(message, "Streams", ', '.join(_mongoFunctions.get_settings(ctx.guild.id)['streams']), False)
        _embedMessage.add_field(message, "Courses", ', '.join(_mongoFunctions.get_settings(ctx.guild.id)['courses']), False)
        _embedMessage.add_field(message, "Due Date Types", ', '.join(_mongoFunctions.get_settings(ctx.guild.id)['due_date_types']), False)

    _embedMessage.add_field(message, "Quote Reaction Emoji Name", _mongoFunctions.get_settings(ctx.guild.id)['reaction_emoji'], False)
    _embedMessage.add_field(message, "Required Quote Reactions for Approval", _mongoFunctions.get_settings(ctx.guild.id)['required_quote_reactions'], False)

    await ctx.channel.send(embed = message)
