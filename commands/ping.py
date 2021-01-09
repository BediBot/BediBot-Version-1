import discord

from commands import _embedMessage, _util


async def ping(ctx: discord.Message, client: discord.Client):
    message = _embedMessage.create("Ping Reply",
                                   "Pong! **{0}ms**\n Guilds: **{1}**\n Users: **{2}**".format(int(client.latency * 1000), _util.get_guild_count(client),
                                                                                               _util.get_member_count(client)), "blue")
    await ctx.channel.send(embed = message)
