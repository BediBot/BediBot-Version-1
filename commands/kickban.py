import discord
from commands import _embedMessage, _util, _kickban, _checkrole, _mongoFunctions
from discord.ext.commands import MemberConverter


async def kick_user_from_command(ctx: discord.Message, client: discord.Client):
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("Kick Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    args = _util.parse_message(ctx.content)

    if len(args) != 3:
        await ctx.channel.send(embed = _embedMessage.create("Kick Reply",
                                                            "The syntax is invalid! Make sure it is in the format $kick <User (Mention)> reason",
                                                            "red"))
        return

    
    mention = args[1]
    #ensure that the user ID is valid
    user_id = mention.replace("<", "").replace(">", "").replace("@", "").replace("!", "")
    try:
        memberToKick = ctx.guild.get_member(int(user_id))
    except:
        await ctx.channel.send(embed = _embedMessage.create("Kick Reply", "Error: Invalid Read", "red"))
        return


    reason = args[2]

    if memberToKick == ctx.author or memberToKick == None or memberToKick == client.user:
        await ctx.channel.send(embed = _embedMessage.create("Kick Reply","Error - you cannot kick yourself or the bot, or the member is not in the guild!", "red"))
        return
    

    replyEmbed = _embedMessage.create("Kick Reply", "Kicked " + mention + ", Reason: " + reason + "\nRequested by: " + ctx.author.mention, "green")
    
    #Attempt to send a PM to the user, try except is for if the user didn't enable messaging for some reason
    try:
        await memberToKick.send(embed = _embedMessage.create("Kicked from " + ctx.guild.name, "You have been kicked from the above listed server for: " + reason + "\nPlease direct any concerns to the admin team on the above listed server", "red"))
    except:
        _embedMessage.add_field(replyEmbed, "Bot Message", "Unable to send private message informing the user of the reason", False)
     
    #ban executes after message so the PM will go through
    await _kickban.kick_user(memberToKick, reason)

    await(ctx.channel.send(embed=replyEmbed))





async def ban_user_from_command(ctx: discord.Message, client: discord.Client):
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("Ban Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    args = _util.parse_message(ctx.content)

    if len(args) != 3:
        await ctx.channel.send(embed = _embedMessage.create("Ban Reply",
                                                            "The syntax is invalid! Make sure it is in the format $ban <User (Mention)> reason",
                                                            "red"))
        return

    
    mention = args[1]
    #ensure that the user ID is valid
    user_id = mention.replace("<", "").replace(">", "").replace("@", "").replace("!", "")
    try:
        memberToKick = ctx.guild.get_member(int(user_id))
    except:
        await ctx.channel.send(embed = _embedMessage.create("Ban Reply", "Error: Invalid Read", "red"))
        return


    reason = args[2]

    if memberToKick == ctx.author or memberToKick == None or memberToKick == client.user:
        await ctx.channel.send(embed = _embedMessage.create("Ban Reply","Error - you cannot ban yourself or the bot, or the member is not in the guild!", "red"))
        return
    

    replyEmbed = _embedMessage.create("Ban Reply", "Banned " + mention + ", Reason: " + reason + "\nRequested by: " + ctx.author.mention, "green")
    
    #Attempt to send a PM to the user, try except is for if the user didn't enable messaging for some reason
    try:
        await memberToKick.send(embed = _embedMessage.create("Banned from " + ctx.guild.name, "You have been banned from the above listed server for: " + reason + "\nPlease direct any concerns to the admin team on the above listed server", "red"))
    except:
        _embedMessage.add_field(replyEmbed, "Bot Message", "Unable to send private message informing the user of the reason", False)
     
    #ban executes after message so the PM will go through
    await _kickban.ban_user(memberToKick, reason)

    await(ctx.channel.send(embed=replyEmbed))

#TODO: Add in an unban command, the following below is an implementation, but does not work due to them not being in the guild. This is left as an issue for later
"""
async def unban_user_from_command(ctx: discord.Message, client: discord.Client):
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("Unban Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    args = _util.parse_message(ctx.content)

    if len(args) != 2:
        await ctx.channel.send(embed = _embedMessage.create("Unban Reply",
                                                            "The syntax is invalid! Make sure it is in the format $Unban <User (Mention)>",
                                                            "red"))
        return

    mention = args[1]
    #ensure that the user ID is valid
    user_id = mention.replace("<", "").replace(">", "").replace("@", "").replace("!", "")
    try:
        memberToUnban = ctx.guild.get_member(int(user_id))
    except:
        await ctx.channel.send(embed = _embedMessage.create("Unban Reply", "Error: Invalid Read", "red"))
        return

    await _kickban.unban_user(ctx, memberToUnban)
    replyEmbed = _embedMessage.create("Unban Reply", "Unbanned " + mention + "\nRequested by: " + ctx.author.mention, "green")
    await ctx.channel.send(embed = replyEmbed)

"""

