import discord
import enum
import random

botStatusList = [
    discord.Activity(type=discord.ActivityType.listening, name="Martingales | $help"),
    discord.Activity(type=discord.ActivityType.watching, name="Geese Honk | $help"),
    discord.Activity(type=discord.ActivityType.streaming, name="EGAD videos | $help"),
    discord.Activity(type=discord.ActivityType.listening, name="115 ASMR | $help"),
    discord.Activity(type=discord.ActivityType.playing, name="Solidworks | $help"),
    discord.Activity(type=discord.ActivityType.playing, name="Among Us | $help"),
    discord.Activity(type=discord.ActivityType.watching, name="Crowdmark | $help")
]


async def setBotStatusRandomly(client):
    await client.change_presence(activity=(random.choice(botStatusList)))

async def setBotStatusFromCommand(ctx, client):
    await setBotStatusRandomly