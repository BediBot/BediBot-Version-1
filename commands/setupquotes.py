import asyncio

import discord

from commands import _mongoFunctions, _embedMessage, _util

# How long to wait for user response before timeout
wait_timeout = 60.0


async def setup_quotes(ctx: discord.Message, client: discord.Client):
    stop_embed = _embedMessage.create("SetupQuotes Reply", "Setup Stopped", "green")

    # Checks if user is admin or bot owner
    if not (ctx.author.guild_permissions.administrator or _util.author_is_bot_owner(ctx)):
        await ctx.channel.send(embed = _embedMessage.create("SetupQuotes Reply", "Invalid Permissions", "red"))
        return

    try:
        _mongoFunctions.get_guilds_information()[str(ctx.guild.id)]
    except KeyError:
        _mongoFunctions.generate_default_settings(ctx.guild.id)

    # Checking function to determine if responses are sent by initial user in initial channel
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    response_message = await ctx.channel.send(embed = _embedMessage.create("SetupQuotes Reply", "Should Quotes be Enabled (y/n)?", "blue"))

    await set_settings(ctx, client, response_message, stop_embed, check)

    await ctx.channel.send(embed = _embedMessage.create("SetupQuotes Reply", "Quotes Setup has been Completed", "blue"))


async def set_settings(ctx: discord.Message, client: discord.Client, response_message: discord.Message, stop_embed: discord.embeds, check):
    while True:
        await response_message.edit(embed = _embedMessage.create("Setup Reply", "Should Quotes be Enabled (y/n)?", "blue"))
        try:
            quotes_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
            return
        else:
            quotes_string = quotes_message.content.lower()
            if quotes_string == 'next':
                break
            if quotes_string == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            if quotes_string in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
                _mongoFunctions.update_setting(ctx.guild.id, "quotes_enabled", True)

            else:
                _mongoFunctions.update_setting(ctx.guild.id, "quotes_enabled", False)
            break

    await asyncio.sleep(0.5)

    while True:
        await response_message.edit(embed = _embedMessage.create("Setup Reply", "What is the quote reaction emoji name? "
                                                                                "(Must be a custom emoji, enter the name without the : characters)", "blue"))
        try:
            reaction_emoji_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
            return
        else:
            reaction_emoji_string = reaction_emoji_message.content
            if reaction_emoji_string.lower() == 'next':
                break
            if reaction_emoji_string.lower() == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            _mongoFunctions.update_setting(ctx.guild.id, "reaction_emoji", reaction_emoji_string)
            break

    while True:
        await response_message.edit(embed = _embedMessage.create("Setup Reply", "How many approvals should be required to approve a quote. (Minimum of 2)", "blue"))
        try:
            reaction_number_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
            return
        else:
            reaction_number_string = reaction_number_message.content
            if reaction_number_string.lower() == 'next':
                break
            if reaction_number_string.lower() == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            _mongoFunctions.update_setting(ctx.guild.id, "required_quote_reactions", int(reaction_number_string))
            break
