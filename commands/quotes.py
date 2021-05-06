import discord

from commands import _mongoFunctions, _util, _embedMessage, _checkrole

sweat_smile = "😅"
embed_field_max_char = 1024


async def add_quote(ctx: discord.Message, client: discord.Client):
    if not _mongoFunctions.is_user_id_linked_to_verified_user_in_guild(ctx.guild.id, ctx.author.id) and _mongoFunctions.get_settings(ctx.guild.id)['verification_enabled']:
        replyEmbed = _embedMessage.create("AddQuote Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    args = _util.parse_message(ctx.content)

    if len(args) != 3:
        await ctx.channel.send(
            embed = _embedMessage.create("AddQuote Reply", "Invalid Syntax! You need two arguments for this function!\nEx: $addquote \"Life is Good\" Bedi", "red"))
        return

    if len(args[1]) > embed_field_max_char:
        await ctx.channel.send(embed = _embedMessage.create("AddQuote Reply", "Quote is too long! Please submit a quote that is 1024 characters or fewer", "red"))
        return

    embed = _embedMessage.create("AddQuote Reply", "| \"" + args[1] + "\" by: " + args[2] + " submitted by: " + ctx.author.mention + " \nReact to Approve\nApproved by: ", "blue")
    message = await ctx.channel.send(embed = embed)
    await message.add_reaction(discord.utils.get(ctx.guild.emojis, name = _mongoFunctions.get_settings(ctx.guild.id)['reaction_emoji']))


async def get_quotes(ctx: discord.Message, client: discord.Client):
    args = _util.parse_message(ctx.content)
    if len(args) != 3 and len(args) != 2:
        await ctx.channel.send(embed = _embedMessage.create("getQuote Reply", "Invalid Syntax! You need two arguments for this function!\nEx: $getQuotes Bedi 2", "red"))
        return
    try:
        person = str(args[1])
        if len(args) == 2:
            page = 1
        else:
            page = int(args[2])
        quotes = _mongoFunctions.find_quotes(ctx.guild.id, person, page)
        try:
            embed = _embedMessage.create("Quotes from: " + person, "Page: " + str(page), "green")
            for quote in quotes:
                value = (quote["quote"][:(embed_field_max_char - 3)] + '...') if len(quote["quote"]) > 1024 else quote["quote"]
                _embedMessage.add_field(embed_msg = embed, title_string = quote["name"], value_string = value, is_inline = False)
            await ctx.channel.send(embed = embed)
        except Exception as e:
            print(e)
            await ctx.channel.send(embed = _embedMessage.create("GetQuotes Reply", "Error sending response", "red"))
    except:
        await ctx.channel.send(embed = _embedMessage.create("GetQuotes Reply", "Invalid Syntax! You need integers", "red"))


async def get_random_quote(ctx: discord.Message, client: discord.Client):
    args = _util.parse_message(ctx.content)

    quote = _mongoFunctions.random_quote_from_person(ctx.guild.id, args[1]) \
        if len(args) == 2 \
        else _mongoFunctions.random_quote(ctx.guild.id)

    await ctx.channel.send(embed = _embedMessage.create("GetRandomQuote Reply", quote, "blue"))


async def remove_quote(ctx: discord.Message, client: discord.Client):
    # Checks if user is admin or bot owner
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("RemoveQuote Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    args = _util.parse_message(ctx.content)

    if len(args) != 3:
        await ctx.channel.send(embed = _embedMessage.create("RemoveQuote Reply", "Invalid Syntax! You need two arguments for this function!", "red"))
        return

    if len(args[1]) > embed_field_max_char:
        await ctx.channel.send(embed = _embedMessage.create("RemoveQuote Reply", "Quote is too long! Please submit a quote that is 1024 characters or fewer", "red"))
        return
    
    embed = None
    del_res = _mongoFunctions.delete_quote(ctx.guild.id, args[1], args[2])
    if del_res.deleted_count == 1:
        embed = _embedMessage.create("RemoveQuote Reply", "\"" + args[1] + "\" by: " + args[2] + " \n Removed by: " + ctx.author.mention, "blue")
    else:
        embed = _embedMessage.create("RemoveQuote Reply", '"' + args[1] + '" by: ' + args[2] + ' Does not exist \n Remove attempted by: ' + ctx.author.mention, "red")
    await ctx.channel.send(embed = embed)


async def quotes_reaction_handler(reaction_payload: discord.RawReactionActionEvent, message: discord.Message):
    # if isinstance(reaction.emoji, str):
    # i think this means its a discord emoji
    # await reaction.message.channel.send("string")

    if reaction_payload.emoji.is_custom_emoji:
        # await reaction.message.channel.send("emoji")
        # print(reaction.emoji.name)
        # emojis from this server

        if reaction_payload.emoji.id == discord.utils.get(message.guild.emojis, name = _mongoFunctions.get_settings(message.guild.id)['reaction_emoji']).id:
            if reaction_payload.member.mention not in message.embeds[0].description:
                embed = _embedMessage.create("AddQuote Reply", message.embeds[0].description + " " + reaction_payload.member.mention, "blue")
                await message.edit(embed = embed)

            reaction_object = None

            for reaction in message.reactions:
                if reaction.emoji.id == reaction.emoji.id:
                    reaction_object = reaction
                    break

            if reaction_object.count >= _mongoFunctions.get_settings(message.guild.id)['required_quote_reactions']:
                args = _util.parse_message(message.embeds[0].description)
                quote = args[1]
                quotedPerson = args[3]
                res = _mongoFunctions.insert_quote(guild_id = message.guild.id, quoted_person = quotedPerson, quote = quote)

                contentArr = message.embeds[0].description.split(" ")
                newContent = " ".join(contentArr[1:])

                if res:
                    embed = _embedMessage.create("Quote Reply", "Approved: " + newContent, "blue")
                    await message.edit(embed = embed)
                else:
                    embed = _embedMessage.create("Quote Reply", "Failed to Connect to DB: " + newContent, "blue")
                    await message.edit(embed = embed)
