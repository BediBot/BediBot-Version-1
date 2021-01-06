import discord

from commands import _embedMessage


async def ping(ctx: discord.Message, client: discord.Client):
    member_count = 0
    for member in client.get_all_members():
        member_count += 1

    message = _embedMessage.create("Ping Reply", "Pong! **{0}ms**\n Users: **{1}**".format(int(client.latency * 1000), member_count), "blue")
    await ctx.channel.send(embed = message)
