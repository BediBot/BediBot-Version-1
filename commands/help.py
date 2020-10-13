from commands import _embedMessage

async def helpCommand(ctx):
    helpMessage = _embedMessage.create("Help Command", "Commands that can be run with BediBot. Each <> represents an arguement", "green")
    _embedMessage.addField(helpMessage, "$addduedate <type> <title> <YYYY> <MM> <DD>", "Add's an assignment's due date to be counted down to", False)
    _embedMessage.addField(helpMessage, "$addQuote <quote with spaces>", "Add's a quote from Professor Bedi", False)
    _embedMessage.addField(helpMessage, "$confirm <code>", "Allows you to enter in your 2FA verification code after you run the verify command", False)
    _embedMessage.addField(helpMessage, "$help", "Allows you to view commands!", False)
    _embedMessage.addField(helpMessage, "$ping", "Returns Pong", False)
    _embedMessage.addField(helpMessage, "$setbirthday <YYYY> <MM> <DD>", "Allows you to set your birthday and let the server know when to embarass you :D", False)
    _embedMessage.addField(helpMessage, "$unverify", "Unverifies you from the server. Note that this does NOT remove the associated email address from your discord user ID", False)
    _embedMessage.addField(helpMessage, "$verify <userID@uwaterloo.ca>", "Allows you to verify yourself as a UWaterloo Student and access the server", False)
    _embedMessage.setFooter(helpMessage, "For any concerns, contact a BediBot dev")

    #780 233 2993
    await ctx.channel.send(embed=helpMessage)