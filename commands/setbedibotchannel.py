from commands import _embedMessage, _mongoFunctions, _dueDateMessage, _checkrole, _util


async def set_bedi_bot_channel(ctx, client):
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("SetBediBotChannel Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    await ctx.channel.purge(limit = None)
    await ctx.channel.send(embed = _embedMessage.create("SetBediBotChannel Reply", "The channel has been set!", "blue"))

    dueDateEmbeds = {}
    dueDateMessages = {}

    for stream in _mongoFunctions.get_settings(ctx.guild.id)['streams']:
        dueDateEmbeds[stream] = _embedMessage.create("Stream {0} Due Dates Message".format(stream), "Temporary Message", "green")
        dueDateMessages[stream] = await ctx.channel.send(embed = dueDateEmbeds[stream])
        await dueDateMessages[stream].pin()
        _mongoFunctions.set_due_date_message_id(ctx.guild.id, stream, dueDateMessages[stream].id)

    _mongoFunctions.set_bedi_bot_channel_id(ctx.guild.id, ctx.channel.id)

    await _dueDateMessage.edit_due_date_message(client)

    await ctx.channel.purge(limit = None, check = lambda msg: not msg.pinned)
