import asyncio

from commands import _embedMessage, _mongoFunctions, _dueDateMessage


async def setbedibotchannel(ctx, client):
    replyEmbed = _embedMessage.create("SetBediBotChannel Reply", "The channel has been set!", "blue")
    message = await ctx.channel.send(embed = replyEmbed)

    dueDatesStream4Embed = _embedMessage.create("Stream 4 Due Dates Message", "Temporary Message", "blue")
    dueDatesStream8Embed = _embedMessage.create("Stream 4 Due Dates Message", "Temporary Message", "blue")

    dueDatesStream4Message = await ctx.channel.send(embed = dueDatesStream4Embed)
    dueDatesStream8Message = await ctx.channel.send(embed = dueDatesStream8Embed)

    _mongoFunctions.set_bedi_bot_channel_id(ctx.guild.id, ctx.channel.id)
    _mongoFunctions.set_due_date_message_id(ctx.guild.id, 4, dueDatesStream4Message.id)
    _mongoFunctions.set_due_date_message_id(ctx.guild.id, 8, dueDatesStream8Message.id)

    await _dueDateMessage.edit_due_date_message(client)

    await asyncio.sleep(10)

    await message.delete()
    await ctx.delete()
