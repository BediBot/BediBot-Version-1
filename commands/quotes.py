from ._mongoFunctions import *
from ._util import parseMessage
import discord

sweat_smile = "😅"
trigger_emoji = 764716218392772638
amount_emoji_needed = 2

async def addQuote(ctx: discord.message, client:discord.client):
    print("add quote command called")
    args = parseMessage(ctx.content)
    
    if len(args) != 3:
        await ctx.channel.send("you need 2 arguments for this function")
    message = await ctx.channel.send("|addQuote quote: \"" +args[1] + "\" by: " + args[2] + " submitted by: " + ctx.author.mention + " \n Approved by: ")
    await message.add_reaction(client.get_emoji(trigger_emoji))

    # await ctx.channel.send("Quote Recorded!")


async def getQuotes(ctx):
    args = parseMessage(ctx.content)
    if len(args) != 3:
        await ctx.channel.send("you need 2 arguments for this function")
    try:
        perPage = int(args[1])
        page = int(args[2])
    except:
        await ctx.channel.send("input error: you need integers")

async def quotesReactionHandler(reaction: discord.reaction, user:discord.User):

    print("reaction handler")

    if isinstance(reaction.emoji,str):
        # i think this means its a discord emoji
        await reaction.message.channel.send("string")

    
    elif isinstance(reaction.emoji, discord.Emoji):
        # await reaction.message.channel.send("emoji")
        # print(reaction.emoji.name)
        # emojis from this server
        if reaction.emoji.id == trigger_emoji:
            await reaction.message.edit(content=reaction.message.content+user.mention)
            if reaction.count >= amount_emoji_needed:
                args = parseMessage(reaction.message.content)
                quote = args[2]
                quotedPerson = args[4]
                res = insertQuote(guildId=reaction.message.guild.id, quotedPerson=quotedPerson, quote=quote)

                contentArr = reaction.message.content.split(" ")
                newContent = " ".join(contentArr[1:])
                if res:
                    await reaction.message.edit(content="approved "+newContent)
                else:
                    await reaction.message.edit(content="failed to connect to db: " + newContent)


    else:
        await reaction.message.channel.send("i dont fucking know what this is")
        #emojis from other servers
        #partial emojis?
    

# print(type(reaction.emoji),"reee",reaction.emoji)
# await reaction.message.channel.send(reaction.emoji)
# if reaction.emoji == sweat_smile:
# await reaction.message.channel.send("reeeeeeeeeeee")