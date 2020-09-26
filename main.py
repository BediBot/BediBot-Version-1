import os
from commands import *
import discord

command_prefix = "$"
emote_prefix = "!"

prefixes = [command_prefix]

commands = {
    command_prefix + "ping": ping
}

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0] in prefixes:
        if message.content.split(" ")[0] in commands:
           await commands[message.content.split(" ")[0]](message)



#------------------------------main-----------------------------

TOKEN = os.getenv("BOT_TOKEN")
print("starting now....")
client.run(TOKEN)