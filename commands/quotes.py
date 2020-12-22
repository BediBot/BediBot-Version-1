from ._mongoFunctions import *
from ._util import *
from ._embedMessage import *
from ._checkrole import *
import discord

sweat_smile = "😅"
amount_emoji_needed = 4


async def add_quote(ctx: discord.message, client: discord.client):
    if not is_user_id_linked_to_verified_user(ctx.guild.id, ctx.author.id):
        replyEmbed = create("AddQuote Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    args = parse_message(ctx.content)

    if len(args) != 3:
        await ctx.channel.send(embed = create("AddQuote Reply", "Invalid Syntax! You need two arguments for this function!", "red"))
        return

    if len(args[1]) > 1024:
        await ctx.channel.send(embed = create("AddQuote Reply", "Quote is too long! Please submit a quote that is 1024 characters or fewer", "red"))
        return

    embed = create("AddQuote Reply", "| \"" + args[1] + "\" by: " + args[2] + " submitted by: " + ctx.author.mention + " \n Approved by: ", "blue")
    message = await ctx.channel.send(embed = embed)
    await message.add_reaction(discord.utils.get(ctx.guild.emojis, name = "bedi"))

    # await ctx.channel.send("Quote Recorded!")


async def get_quotes(ctx: discord.message, client: discord.client):
    args = parse_message(ctx.content)
    if len(args) != 3 and len(args) != 2:
        await ctx.channel.send(embed = create("getQuote Reply", "Invalid Syntax! You need two arguments for this function!\nEx: $getQuotes Bedi 2", "red"))
        return
    try:
        person = str(args[1])
        if len(args) == 2:
            page = 1
        else:
            page = int(args[2])
        quotes = find_quotes(ctx.guild.id, person, page)
        try:
            # print(quotes)
            embed = create("Quotes from: " + person, "Page: " + str(page), "green")
            for quote in quotes:
                value = (quote["quote"][:1021] + '...') if len(quote["quote"]) > 1024 else quote["quote"]
                add_field(embed_msg = embed, title_string = quote["name"], value_string = value, is_inline = False)
            await ctx.channel.send(embed = embed)
        except Exception as e:
            print(e)
            await ctx.channel.send(embed = create("GetQuotes Reply", "Error sending response", "red"))
    except:
        await ctx.channel.send(embed = create("GetQuotes Reply", "Invalid Syntax! You need integers", "red"))


async def remove_quote(ctx: discord.message, client: discord.client):
    if not (author_has_role(ctx, get_admin_role(ctx.guild.id)) or author_is_bot_owner(ctx)):
        replyEmbed = create("RemoveQuote Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    args = parse_message(ctx.content)

    if len(args) != 3:
        await ctx.channel.send(embed = create("RemoveQuote Reply", "Invalid Syntax! You need two arguments for this function!", "red"))
        return

    if len(args[1]) > 1024:
        await ctx.channel.send(embed = create("RemoveQuote Reply", "Quote is too long! Please submit a quote that is 1024 characters or fewer", "red"))
        return

    embed = create("RemoveQuote Reply", "\"" + args[1] + "\" by: " + args[2] + " \n Removed by: " + ctx.author.mention, "blue")
    await ctx.channel.send(embed = embed)
    delete_quote(ctx.guild.id, args[1], args[2])


async def quotes_reaction_handler(reaction: discord.reaction, user: discord.User):
    print("reaction handler")
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
                embed = create("AddQuote Reply", reaction.message.embeds[0].description + " " + user.mention, "blue")
                await reaction.message.edit(embed = embed)
                print("this is acc happening")
            if reaction.count >= amount_emoji_needed:
                args = parse_message(reaction.message.embeds[0].description)
                quote = args[1]
                quotedPerson = args[3]
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
