import discord

from commands import _embedMessage


async def ping(ctx: discord.Message, client: discord.Client):
    message = _embedMessage.create("Ping Reply", "Pong! **{0}ms**".format(int(client.latency * 1000)), "blue")
    await ctx.channel.send(embed = message)
