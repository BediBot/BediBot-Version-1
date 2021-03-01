import discord

from commands import _embedMessage, _checkrole, _util, _mongoFunctions


async def say(ctx: discord.Message, client: discord.Client):
    # Checks if user is admin or bot owner
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("Say Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    global target_channel

    args = _util.parse_message(ctx.content)

    if len(args) != 4 and len(args) != 3:
        await ctx.channel.send(embed = _embedMessage.create("Say Reply", "Invalid Syntax! You need three arguments for this function!\nSyntax: say title content OPTIONAL:channel", "red"))
        return

    title = args[1]

    content = args[2]

    target_channel = ctx.channel
    if len(args) == 4:
        channel_mention = args[3]
        channels = client.get_all_channels()

        for channel in channels:
            if channel.mention == channel_mention:
                target_channel = channel
                break

        if target_channel is None:
            await ctx.channel.send(embed = _embedMessage.create("Say Reply", "Channel not Found!", "red"))
            return

    

    try:
        await ctx.delete()
    except:
        print("Missing Manage Messages permission in {0} on server ID: {1}".format(channel.mention, str(client.get_guild(ctx.guild.id))))

    if not _util.author_is_bot_owner(ctx):
        embed = _embedMessage.create(title, content + "\n\n This message was sent by {}".format(ctx.author.mention), "green")
    else:
        embed = _embedMessage.create(title, content, "green")

    await target_channel.send(embed = embed)
