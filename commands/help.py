from commands import _embedMessage

commandPrefix2 = "$"


async def help_command(ctx, client):
    helpMessage = _embedMessage.create("Help Command", "Commands that can be run with BediBot. Each word represents an argument", "green")
    _embedMessage.add_field(helpMessage, commandPrefix2 + "addquote \"quote with spaces\" Name",
                            "Adds a quote from the individual of your choice\nEx: " + commandPrefix2 + "addQuote \"Life is Good\", Bedi", False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "confirm code",
                            "Allows you to enter in your 2FA verification code after you run the verify command\nEx: " + commandPrefix2 + "confirm 123456789", False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "getQuotes person pagenumber",
                            "Gets a persons quotes with a page number, with each page in 5 days\nEx: " + commandPrefix2 + "getQuote Bedi 2", False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "help", "Allows you to view commands!", False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "ping", "Returns Pong", False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "setbirthday YYYY MM DD",
                            "Allows you to set your birthday and let the server know when to embarrass you :D\nEx: " + commandPrefix2 + "setbirthday 2001 01 01", False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "unverify",
                            "Unverifies you from the server. Note that this does NOT remove the associated email address from your discord user ID", False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "verify userID@uwaterloo.ca",
                            "Allows you to verify yourself as a UWaterloo Student and access the server\nEx: " + commandPrefix2 + "$verify g0ose@uwaterloo.ca", False)
    _embedMessage.add_field(helpMessage, "Admin Commands", "Admin Commands are listed below. They cannot be used without the admin or bot dev role\n/**********************/",
                            False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "addduedate", "Add's an assignment's due date to be counted down to\nEx: " + commandPrefix2 + "addduedate", False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "adminverify @Mention",
                            "Manually verifies a user. Note that this does NOT add in a role and simply adds them to the database\nEx: " + commandPrefix2 + "adminverify " + client.user.mention,
                            False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "lockdown role", "Sets send message permissions to false for specified role\nEx: " + commandPrefix2 + "lockdown " + "Tron", False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "removeduedate", "Remove's a due date\nEx: " + commandPrefix2 + "removeduedate", False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "removequote \"quote with spaces\" Name",
                            "Removes a quote from the individual of your choice\nEx: " + commandPrefix2 + "addQuote \"Life is Good\", Bedi", False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "say title content channel",
                            "Sends a message inside an embed to the specified channel\nEx: " + commandPrefix2 + "say Hello world " + ctx.channel.mention, False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "setbedibotchannel",
                            "Sets the channel which will be used for announcements\nWARNING: This clears the channel's history. Use with caution.", False)
    _embedMessage.add_field(helpMessage, commandPrefix2 + "unlock role", "Sets send message permissions to True for specified role\nEx: " + commandPrefix2 + "unlock " + "Tron", False)

    await ctx.channel.send(embed = helpMessage)
