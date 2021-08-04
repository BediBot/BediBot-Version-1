import discord

from commands import _embedMessage, _checkrole, _mongoFunctions, _util


async def settings(ctx: discord.Message, client: discord.Client):
    # Checks if user is admin or bot owner
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("Settings Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    settings_embed = _embedMessage.create("Settings Reply", "Here are the settings for **" + ctx.guild.name + "**", "blue")

    _embedMessage.add_field(settings_embed, "Prefix", _mongoFunctions.get_settings(ctx.guild.id)['prefix'], False)

    _embedMessage.add_field(settings_embed, "Timezone", _mongoFunctions.get_settings(ctx.guild.id)['timezone'], False)

    _embedMessage.add_field(settings_embed, "Admin Role", _mongoFunctions.get_settings(ctx.guild.id)['admin_role'], False)

    _embedMessage.add_field(settings_embed, "Pins Enabled", _mongoFunctions.get_settings(ctx.guild.id)['pins_enabled'], False)

    await ctx.channel.send(embed = settings_embed)

    verification_embed = _embedMessage.create("Verification Settings", "Here are the verification settings.", "blue")
    _embedMessage.add_field(verification_embed, "Verification Enabled?", _mongoFunctions.get_settings(ctx.guild.id)['verification_enabled'], False)
    if _mongoFunctions.get_settings(ctx.guild.id)['verification_enabled']:
        _embedMessage.add_field(verification_embed, "Verified Role", _mongoFunctions.get_settings(ctx.guild.id)['verified_role'], False)
        _embedMessage.add_field(verification_embed, "Verification Email Domain", _mongoFunctions.get_settings(ctx.guild.id)['email_domain'], False)
    await ctx.channel.send(embed = verification_embed)

    announcement_embed = _embedMessage.create("Morning Announcement Settings", "Here are the morning announcement settings.", "blue")
    _embedMessage.add_field(announcement_embed, "Morning Announcements Enabled?", _mongoFunctions.get_settings(ctx.guild.id)['morning_announcements_enabled'], False)
    if _mongoFunctions.get_settings(ctx.guild.id)['morning_announcements_enabled']:
        try:
            channel_name = ctx.guild.get_channel(int(_mongoFunctions.get_settings(ctx.guild.id)['announcement_channel_id'])).mention
        except:
            channel_name = "Not set. Run {0}setup to set.".format(_mongoFunctions.get_settings(ctx.guild.id)['prefix'])

        _embedMessage.add_field(announcement_embed, "Morning Announcements Channel", channel_name, False)
        _embedMessage.add_field(announcement_embed, "Daily Announcement Time", _mongoFunctions.get_settings(ctx.guild.id)['announcement_time'], False)
        _embedMessage.add_field(announcement_embed, "Random Quote?", _mongoFunctions.get_settings(ctx.guild.id)['random_quote'], False)
        _embedMessage.add_field(announcement_embed, "Daily Announcement Quote Author", _mongoFunctions.get_settings(ctx.guild.id)['announcement_quoted_person'], False)
    await ctx.channel.send(embed = announcement_embed)

    birthday_embed = _embedMessage.create("Birthday Announcement Settings", "Here are the birthday settings.", "blue")
    _embedMessage.add_field(birthday_embed, "Birthday Announcements Enabled?", _mongoFunctions.get_settings(ctx.guild.id)['birthday_announcements_enabled'], False)
    if _mongoFunctions.get_settings(ctx.guild.id)['birthday_announcements_enabled']:
        try:
            channel_name = ctx.guild.get_channel(int(_mongoFunctions.get_settings(ctx.guild.id)['birthday_channel_id'])).mention
        except:
            channel_name = "Not set. Run {0}setup to set.".format(_mongoFunctions.get_settings(ctx.guild.id)['prefix'])

        _embedMessage.add_field(birthday_embed, "Birthday Announcements Channel", channel_name, False)
        _embedMessage.add_field(birthday_embed, "Birthday Announcement Time", _mongoFunctions.get_settings(ctx.guild.id)['birthday_time'], False)
        _embedMessage.add_field(birthday_embed, "Birthday Role", _mongoFunctions.get_settings(ctx.guild.id)['birthday_role'], False)
    await ctx.channel.send(embed = birthday_embed)

    due_date_embed = _embedMessage.create("Due Date Settings", "Here are the due date settings.", "blue")
    _embedMessage.add_field(due_date_embed, "Due Dates Enabled?", _mongoFunctions.get_settings(ctx.guild.id)['due_dates_enabled'], False)
    if _mongoFunctions.get_settings(ctx.guild.id)['due_dates_enabled']:
        try:
            channel_name = ctx.guild.get_channel(int(_mongoFunctions.get_settings(ctx.guild.id)['due_date_channel_id'])).mention
        except:
            channel_name = "Not set. Run {0}setduedatechannel in a channel to set.".format(_mongoFunctions.get_settings(ctx.guild.id)['prefix'])

        _embedMessage.add_field(due_date_embed, "Due Date Channel", channel_name, False)
        _embedMessage.add_field(due_date_embed, "Streams", ', '.join(_mongoFunctions.get_settings(ctx.guild.id)['streams']), False)
        _embedMessage.add_field(due_date_embed, "Courses", ', '.join(_mongoFunctions.get_settings(ctx.guild.id)['courses']), False)
        _embedMessage.add_field(due_date_embed, "Due Date Types", ', '.join(_mongoFunctions.get_settings(ctx.guild.id)['due_date_types']), False)
    await ctx.channel.send(embed = due_date_embed)

    quote_embed = _embedMessage.create("Quote Settings", "Here are the quote settings.", "blue")
    _embedMessage.add_field(quote_embed, "Quotes Enabled?", _mongoFunctions.get_settings(ctx.guild.id)['quotes_enabled'], False)

    if _mongoFunctions.get_settings(ctx.guild.id)['quotes_enabled']:
        _embedMessage.add_field(quote_embed, "Quote Reaction Emoji Name", _mongoFunctions.get_settings(ctx.guild.id)['reaction_emoji'], False)
        _embedMessage.add_field(quote_embed, "Required Quote Reactions for Approval", _mongoFunctions.get_settings(ctx.guild.id)['required_quote_reactions'], False)
    await ctx.channel.send(embed = quote_embed)
