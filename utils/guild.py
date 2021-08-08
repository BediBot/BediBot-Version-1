import discord
from discord.ext import commands


def get_guild_count(client: discord.Client):
    return len(client.guilds)


def get_member_count(client: discord.Client):
    member_count = 0

    for user in client.get_all_members():
        if not user.bot:
            member_count += 1

    return member_count


def get_prefix(bot: discord.ext.commands.Bot, ctx: discord.Message):
    prefixes = ['$', '.', '#']

    if not ctx.guild:
        return '$'

    return commands.when_mentioned_or(*prefixes)(bot, ctx)
