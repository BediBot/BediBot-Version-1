import discord

from commands import _util, _checkrole, _mongoFunctions, _embedMessage

MAX_PURGE_LIMIT = 50

async def purge(ctx: discord.Message, client: discord.Client):
    #Check if user has admin permissions
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("Purge Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    args = _util.parse_message(ctx.content)
    try:
        numberOfMessages = int(args[1])
    except:
        await ctx.channel.send(embed = _embedMessage.create("Purge Reply", "Ensure that the argument is an int!", "red"))
        return

    if(len(args) != 2 or numberOfMessages < 1 or numberOfMessages > MAX_PURGE_LIMIT):
        await ctx.channel.send(embed = _embedMessage.create("Purge Reply", "Invalid Syntax! You need 1 argument for this function that is a positive integer less than " + str(MAX_PURGE_LIMIT) + "!\nSyntax: purge numberOfMessages", "red"))
        return

    

    await _util.purge_messages_with_limit(client, ctx.guild.id, ctx.channel.id, numberOfMessages)

    replyEmbed = _embedMessage.create("Purge Reply", "Purged " + str(numberOfMessages) + " message(s), requested by: " + ctx.author.mention, "green")
    await(ctx.channel.send(embed=replyEmbed))