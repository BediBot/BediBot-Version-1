from ._mongoFunctions import *
from ._util import parse_message
from ._embedMessage import *
from ._checkrole import *
import discord

sweat_smile = "😅"
amount_emoji_needed = 4


async def addQuote(ctx: discord.message, client: discord.client):
    if not is_user_id_linked_to_verified_user(ctx.guild.id, ctx.author.id):
        replyEmbed = create("AddQuote Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    args = parse_message(ctx.content)

    if len(args) != 3:
        await ctx.channel.send(embed = create("AddQuote Reply", "Invalid Syntax! You need two arguments for this function!", "red"))
        return
    embed = create("AddQuote Reply", "|addQuote quote: \"" + args[1] + "\" by: " + args[2] + " submitted by: " + ctx.author.mention + " \n Approved by: ", "blue")
    message = await ctx.channel.send(embed = embed)
    await message.add_reaction(discord.utils.get(ctx.guild.emojis, name = "bedi"))

    # await ctx.channel.send("Quote Recorded!")


async def getQuotes(ctx: discord.message, client: discord.client):
    args = parse_message(ctx.content)
    if len(args) != 3:
        await ctx.channel.send(embed = create("getQuote Reply", "Invalid Syntax! You need two arguments for this function!\nEx: $getQuote Bedi 2", "red"))
        return
    try:
        person = str(args[1])
        page = int(args[2])
        quotes = find_quotes(ctx.guild.id, person, page)
        try:
            print(quotes)
            embed = create("Quotes from: " + person, "Page: " + str(page), "green")
            for quote in quotes:
                add_field(embed_msg = embed, title_string = quote["quote"], value_string = quote["name"], is_inline = False)
            await ctx.channel.send(embed = embed)
        except Exception as e:
            print(e)
            await ctx.channel.send(embed = create("GetQuotes Reply", "Error sending response", "red"))
    except:
        await ctx.channel.send(embed = create("GetQuotes Reply", "Invalid Syntax! You need integers", "red"))


async def quotesReactionHandler(reaction: discord.reaction, user: discord.User):
    # print("reaction handler")
    # print(reaction.message.embeds + "test")

    if isinstance(reaction.emoji, str):
        # i think this means its a discord emoji
        # await reaction.message.channel.send("string")
        print("reeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")

    elif isinstance(reaction.emoji, discord.Emoji):
        # await reaction.message.channel.send("emoji")
        # print(reaction.emoji.name)
        # emojis from this server

        if reaction.emoji.id == discord.utils.get(reaction.message.guild.emojis, name = "bedi").id:
            if not user.mention in reaction.message.embeds[0].description:
                embed = create("Quote Reply", reaction.message.embeds[0].description + user.mention, "blue")
                await reaction.message.edit(embed = embed)
            if reaction.count >= amount_emoji_needed:
                args = parse_message(reaction.message.embeds[0].description)
                quote = args[2]
                quotedPerson = args[4]
                res = insert_quote(guild_id = reaction.message.guild.id, quoted_person = quotedPerson, quote = quote)

                contentArr = reaction.message.embeds[0].description.split(" ")
                newContent = " ".join(contentArr[1:])
                print(newContent)
                if res:
                    embed = create("Quote Reply", "Approved: " + newContent, "blue")
                    await reaction.message.edit(embed = embed)
                else:
                    embed = create("Quote Reply", "Failed to Connect to DB: " + newContent, "blue")
                    await reaction.message.edit(embed = embed)

    else:
        await reaction.message.channel.send("i dont know what this is")
        # emojis from other servers
        # partial emojis?

# print(type(reaction.emoji),"reee",reaction.emoji)
# await reaction.message.channel.send(reaction.emoji)
# if reaction.emoji == sweat_smile:
# await reaction.message.channel.send("reeeeeeeeeeee")
