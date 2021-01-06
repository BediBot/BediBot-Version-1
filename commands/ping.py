import discord

from commands import _embedMessage


async def ping(ctx: discord.Message, client: discord.Client):
    member_count = 0

    for user in client.users:
        if not user.bot:
            member_count += 1

    guild_count = len(client.guilds)

    message = _embedMessage.create("Ping Reply", "Pong! **{0}ms**\n Guilds: **{1}**\n Users: **{2}**".format(int(client.latency * 1000), guild_count, member_count), "blue")
    await ctx.channel.send(embed = message)
