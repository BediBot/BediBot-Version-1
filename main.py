import os
import discord
from dotenv import load_dotenv
from commands import *
from commands import _morningAnnouncement, _mongoFunctions, _setBotStatus, _dueDateMessage

command_prefix = "$"
emote_prefix = "!"

prefixes = [command_prefix]

commands = {
    command_prefix + "ping": ping,
    command_prefix + "verify": verify,
    command_prefix + "confirm": confirm,
    command_prefix + "unverify": unverify,
    command_prefix + "setbirthday": setbirthday,
    command_prefix + "addduedate": addduedate,
    command_prefix + "help": helpCommand,
    command_prefix + "setbedibotchannel": setbedibotchannel
}

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    _mongoFunctions.init()
    # await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="115 ASMR | $help"))
    await _setBotStatus.setBotStatusRandomly(client)
    await _morningAnnouncement.schedule_announcement(client)


@client.event
async def on_message(ctx):
    if ctx.author == client.user:
        return

    if ctx.content[0] in prefixes:
        if ctx.content.split(" ")[0] in commands:
            await commands[ctx.content.split(" ")[0]](ctx, client)


# ------------------------------main-----------------------------


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
client.run(TOKEN)
