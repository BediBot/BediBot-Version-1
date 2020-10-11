from commands import _embedMessage
import discord

async def ping(ctx):
    print("pong")
    message = _embedMessage.create("Ping Reply", "Pong!", "blue")
    #_embedMessage.addField(message, "Imposter", "Red Sus", False)
    await ctx.channel.send(embed=message)