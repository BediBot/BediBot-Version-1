import asyncio

import discord

from commands import _mongoFunctions, _embedMessage, _util, setupannouncement, setupbirthdays, setupduedates, setupquotes, setupverification
from commands.settings import settings


async def setup(ctx: discord.Message, client: discord.Client):
    # How long to wait for user response before timeout
    wait_timeout = 60.0

    stop_embed = _embedMessage.create("Setup Reply", "Setup Stopped", "green")

    # Checks if user is admin or bot owner
    if not (ctx.author.guild_permissions.administrator or _util.author_is_bot_owner(ctx)):
        await ctx.channel.send(embed = _embedMessage.create("Setup Reply", "Invalid Permissions", "red"))
        return

    try:
        _mongoFunctions.get_guilds_information()[str(ctx.guild.id)]
    except KeyError:
        _mongoFunctions.generate_default_settings(ctx.guild.id)

    # Checking function to determine if responses are sent by initial user in initial channel
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    response_message = await ctx.channel.send(
        embed = _embedMessage.create("Setup Reply", "What should the prefix be (Default: $)? For any of these settings, if you wish to keep the current setting, type 'next'. "
                                                    "If you wish to stop the command at any time, type 'stop'.",
                                     "blue"))

    while True:
        await response_message.edit(embed = _embedMessage.create("Setup Reply", "What should the prefix be (Default: $)? For any of these settings, "
                                                                                "if you wish to keep the current setting, type 'next'.", "blue"))
        try:
            prefix_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
            return
        else:
            prefix = prefix_message.content
            if prefix.lower() == 'next':
                break
            if prefix.lower() == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            _mongoFunctions.update_setting(ctx.guild.id, "prefix", prefix)
            break

    while True:
        await response_message.edit(embed = _embedMessage.create("Setup Reply", "What is the admin role?", "blue"))
        try:
            admin_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
            return
        else:
            admin_role_string = admin_message.content
            if admin_role_string.lower() == 'next':
                break
            if admin_role_string.lower() == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            _mongoFunctions.update_setting(ctx.guild.id, "admin_role", admin_role_string)
            break

    while True:
        await response_message.edit(embed = _embedMessage.create("Setup Reply", "Should reaction pinning be enabled (y/n)?", "blue"))
        try:
            pinning_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
            return
        else:
            pinning_string = pinning_message.content.lower()
            if pinning_string == 'next':
                break
            if pinning_string == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            if pinning_string in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
                _mongoFunctions.update_setting(ctx.guild.id, "pins_enabled", True)
            else:
                _mongoFunctions.update_setting(ctx.guild.id, "pins_enabled", False)

            break

    await setupverification.set_settings(ctx, client, response_message, stop_embed, check)

    await setupannouncement.set_settings(ctx, client, response_message, stop_embed, check)

    await setupbirthdays.set_settings(ctx, client, response_message, stop_embed, check)

    await setupduedates.set_settings(ctx, client, response_message, stop_embed, check)

    await setupquotes.set_settings(ctx, client, response_message, stop_embed, check)

    await ctx.channel.send(embed = _embedMessage.create("Setup Reply", "Guild has been setup. Make sure to run {0}setduedatechannel in a view-only channel if needed.".format(
        _mongoFunctions.get_settings(ctx.guild.id)['prefix']), "blue"))
    await settings(ctx, client)
