from commands import _embedMessage

commandPrefix2 = "$"

async def helpCommand(ctx, client):
    helpMessage = _embedMessage.create("Help Command", "Commands that can be run with BediBot. Each <> represents an arguement", "green")
    _embedMessage.addField(helpMessage, commandPrefix2 + "addduedate <course> <type> <title> <YYYY> <MM> <DD> <HH:DD>", "Add's an assignment's due date to be counted down to", False)
    _embedMessage.addField(helpMessage, commandPrefix2 + "addQuote <\"quote with spaces\"> <Name of person who said it>", "Add's a quote from Professor Bedi", False)
    _embedMessage.addField(helpMessage, commandPrefix2 + "confirm <code>", "Allows you to enter in your 2FA verification code after you run the verify command", False)
    _embedMessage.addField(helpMessage, commandPrefix2 + "getQuotes <Person> <PageNumber>", "Gets a person's quotes with a page number, with each page in 5 days", False)
    _embedMessage.addField(helpMessage, commandPrefix2 + "help", "Allows you to view commands!", False)
    _embedMessage.addField(helpMessage, commandPrefix2 + "ping", "Returns Pong", False)
    _embedMessage.addField(helpMessage, commandPrefix2 + "setbirthday <YYYY> <MM> <DD>", "Allows you to set your birthday and let the server know when to embarass you :D", False)
    _embedMessage.addField(helpMessage, commandPrefix2 + "unverify", "Unverifies you from the server. Note that this does NOT remove the associated email address from your discord user ID", False)
    _embedMessage.addField(helpMessage, commandPrefix2 + "verify <userID@uwaterloo.ca>", "Allows you to verify yourself as a UWaterloo Student and access the server", False)
    _embedMessage.addField(helpMessage, "Admin Commands", "Admin Commands are listed below. They cannot be used without the admin or bot dev role\n/**********************/", False)
    _embedMessage.addField(helpMessage, commandPrefix2 + "setbedibotchannel", "Sets the channel which will be used for announcements\nWARNING: This clears the channel's history. Use with caution.", False)


    await ctx.channel.send(embed = helpMessage)
