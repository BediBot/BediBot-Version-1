import discord

from commands import _embedMessage, _mongoFunctions

commandPrefix2 = "$"


async def help_command(ctx: discord.Message, client: discord.Client):
    helpMessage = _embedMessage.create("Help Command", "Commands that can be run with BediBot. Each word represents an argument.", "green")
    _embedMessage.add_field(helpMessage, commandPrefix2 + "help", "Allows you to view commands!", False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "ping", "Returns Pong", False)

    if _mongoFunctions.get_settings(ctx.guild.id)['verification_enabled']:
        _embedMessage.add_field(helpMessage, commandPrefix2 + "verify userID@uwaterloo.ca",
                                "Allows you to verify yourself as a UWaterloo Student and access the server\nEx: " + commandPrefix2 + "$verify g0ose@uwaterloo.ca", False)
        _embedMessage.add_field(helpMessage, commandPrefix2 + "unverify",
                                "Unverifies you from the server. Note that this does NOT remove the associated email address from your discord user ID", False)
        _embedMessage.add_field(helpMessage, commandPrefix2 + "confirm code",
                                "Allows you to enter in your 2FA verification code after you run the verify command\nEx: " + commandPrefix2 + "confirm 123456789", False)
        _embedMessage.add_field(helpMessage, commandPrefix2 + "adminverify @Mention",
                                "ADMIN ONLY - Manually verifies a user. Note that this does NOT add in a role and simply adds them to the database\nEx: " + commandPrefix2 + "adminverify " + client.user.mention,
                                False)

    if _mongoFunctions.get_settings(ctx.guild.id)['birthday_announcements_enabled']:
        _embedMessage.add_field(helpMessage, commandPrefix2 + "getbirthdays monthnumber",
                                "Gets all birthdays for the specified month\nEx: " + commandPrefix2 + "getbirthdays 5", False)
        _embedMessage.add_field(helpMessage, commandPrefix2 + "setbirthday YYYY MM DD",
                                "Allows you to set your birthday and let the server know when to embarrass you :D\nEx: " + commandPrefix2 + "setbirthday 2001 01 01", False)

    if _mongoFunctions.get_settings(ctx.guild.id)['due_dates_enabled']:
        _embedMessage.add_field(helpMessage, commandPrefix2 + "addduedate",
                                "ADMIN ONLY - Add's an assignment's due date to be counted down to\nEx: " + commandPrefix2 + "addduedate", False)
        _embedMessage.add_field(helpMessage, commandPrefix2 + "removeduedate", "ADMIN ONLY - Remove's a due date\nEx: " + commandPrefix2 + "removeduedate", False)

    _embedMessage.add_field(helpMessage, commandPrefix2 + "addquote \"quote with spaces\" Name",
                            "Adds a quote from the individual of your choice\nEx: " + commandPrefix2 + "addQuote \"Life is Good\", Bedi", False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "getQuotes person pagenumber",
                            "Gets a persons quotes with a page number, with each page in 5 days\nEx: " + commandPrefix2 + "getQuote Bedi 2", False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "removequote \"quote with spaces\" Name",
                            "ADMIN ONLY - Removes a quote from the individual of your choice\nEx: " + commandPrefix2 + "addQuote \"Life is Good\", Bedi", False)

    _embedMessage.add_field(helpMessage, commandPrefix2 + "lockdown role",
                            "ADMIN ONLY - Sets send message permissions to false for specified role\nEx: " + commandPrefix2 + "lockdown " + "Tron", False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "unlock role",
                            "ADMIN ONLY - Sets send message permissions to True for specified role\nEx: " + commandPrefix2 + "unlock " + "Tron",
                            False)

    _embedMessage.add_field(helpMessage, commandPrefix2 + "say title content channel",
                            "ADMIN ONLY - Sends a message inside an embed to the specified channel\nEx: " + commandPrefix2 + "say Hello world " + ctx.channel.mention, False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "setbedibotchannel",
                            "ADMIN ONLY - Sets the channel which will be used for announcements\nWARNING: This clears the channel's history. Use with caution.", False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "settings", "ADMIN ONLY - Displays the guild's settings", False)


    await ctx.channel.send(embed = helpMessage)
