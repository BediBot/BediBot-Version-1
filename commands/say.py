from commands import _embedMessage, _checkrole, _util, _mongoFunctions


async def say(ctx, client):
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("Say Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    global target_channel

    args = _util.parse_message(ctx.content)

    if len(args) != 4:
        await ctx.channel.send(embed = _embedMessage.create("Say Reply", "Invalid Syntax! You need three arguments for this function!", "red"))
        return

    title = args[1]

    content = args[2]

    channel_mention = args[3]

    channels = client.get_all_channels()

    for channel in channels:
        if channel.mention == channel_mention:
            target_channel = channel
            break

    if target_channel is None:
        await ctx.channel.send(embed = _embedMessage.create("Say Reply", "Channel not Found!", "red"))
        return

    await ctx.delete()
    await target_channel.send(embed = _embedMessage.create(title, content, "green"))

    return
