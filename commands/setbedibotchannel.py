import asyncio

from commands import _embedMessage, _mongoFunctions, _dueDateMessage, _checkrole


async def set_bedi_bot_channel(ctx, client):
    if not (_checkrole.author_has_role(ctx, "admin") or _checkrole.author_has_role(ctx, "admins()")):
        replyEmbed = _embedMessage.create("SetBediBotChannel Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    await ctx.channel.purge(limit = None)
    replyEmbed = _embedMessage.create("SetBediBotChannel Reply", "The channel has been set!", "blue")
    await ctx.channel.send(embed = replyEmbed)

    dueDatesStream4Embed = _embedMessage.create("Stream 4 Due Dates Message", "Temporary Message", "green")
    dueDatesStream8Embed = _embedMessage.create("Stream 4 Due Dates Message", "Temporary Message", "green")

    dueDatesStream4Message = await ctx.channel.send(embed = dueDatesStream4Embed)
    dueDatesStream8Message = await ctx.channel.send(embed = dueDatesStream8Embed)

    await dueDatesStream4Message.pin()
    await dueDatesStream8Message.pin()

    _mongoFunctions.set_bedi_bot_channel_id(ctx.guild.id, ctx.channel.id)
    _mongoFunctions.set_due_date_message_id(ctx.guild.id, 4, dueDatesStream4Message.id)
    _mongoFunctions.set_due_date_message_id(ctx.guild.id, 8, dueDatesStream8Message.id)

    await _dueDateMessage.edit_due_date_message(client)

    await asyncio.sleep(5)

    await ctx.channel.purge(limit = None, check = lambda msg: not msg.pinned)
