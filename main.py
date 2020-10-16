import os
from dotenv import load_dotenv
from commands import *
import discord

command_prefix = "$"
emote_prefix = "!"
reaction_handler_prefix = "|"

prefixes = [command_prefix, emote_prefix]

commands = {
    command_prefix + "ping"     : ping,
    command_prefix + "parse"    : parseCommand,
    command_prefix + "addQuote" : addQuote,
    command_prefix + "getQuotes" : getQuotes,
}

reactionHandlers = {
    reaction_handler_prefix + "addQuote" : quotesReactionHandler,
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
           await commands[message.content.split(" ")[0]](message, client)

@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if reaction.message.author == client.user:
        if reaction.message.content.split(" ")[0] in reactionHandlers:
           await reactionHandlers[reaction.message.content.split(" ")[0]](reaction, user) 


#------------------------------main-----------------------------
load_dotenv()

TOKEN = os.getenv("TOKEN")
#print(TOKEN)
#commands["$ping"]()
init()
print("starting now....")
client.run(TOKEN)