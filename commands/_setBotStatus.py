import random

import discord

from commands import _util


async def reset_status_list(client: discord.Client):
    global botStatusList
    botStatusList = [
        discord.Activity(type = discord.ActivityType.listening, name = "Martingales | $help"),
        discord.Activity(type = discord.ActivityType.watching, name = "Geese Honk | $help"),
        discord.Activity(type = discord.ActivityType.streaming, name = "EGAD videos | $help"),
        discord.Activity(type = discord.ActivityType.listening, name = "115 ASMR | $help"),
        discord.Activity(type = discord.ActivityType.playing, name = "Solidworks | $help"),
        discord.Activity(type = discord.ActivityType.playing, name = "Among Us | $help"),
        discord.Activity(type = discord.ActivityType.watching, name = "Crowdmark | $help"),
        discord.Activity(type = discord.ActivityType.watching, name = "{0} Users, {1} Guilds".format(_util.get_member_count(client), _util.get_guild_count(client)))
    ]


async def set_random_bot_status(client):
    await reset_status_list(client)
    await client.change_presence(activity = (random.choice(botStatusList)))


async def set_bot_status_from_command(ctx, client):
    await set_random_bot_status(client)
