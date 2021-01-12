import asyncio

import discord

from commands import _mongoFunctions, _embedMessage, _util

# How long to wait for user response before timeout
wait_timeout = 60.0


async def setup_verification(ctx: discord.Message, client: discord.Client):
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

    response_message = await ctx.channel.send(embed = _embedMessage.create("Setup Reply", "Should Verification be Enabled (y/n)?", "blue"))

    await set_settings(ctx, client, response_message, stop_embed, check)

    await ctx.channel.send(embed = _embedMessage.create("Setup Reply", "Verification Setup has been Completed", "blue"))


async def set_settings(ctx: discord.Message, client: discord.Client, response_message: discord.Message, stop_embed: discord.embeds, check):
    while True:
        await response_message.edit(embed = _embedMessage.create("Setup Reply", "Should Verification be Enabled (y/n)?", "blue"))
        try:
            verification_message = await client.wait_for('message', timeout = wait_timeout, check = check)
        except asyncio.TimeoutError:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
            return
        else:
            verification_string = verification_message.content.lower()
            if verification_string == 'next':
                break
            if verification_string == 'stop':
                await ctx.channel.send(embed = stop_embed)
                return
            if verification_string in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
                _mongoFunctions.update_setting(ctx.guild.id, "verification_enabled", True)

            else:
                _mongoFunctions.update_setting(ctx.guild.id, "verification_enabled", False)
            break

    await asyncio.sleep(0.5)

    if _mongoFunctions.get_settings(ctx.guild.id)["verification_enabled"]:
        while True:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "What is the verified role?", "blue"))
            try:
                verified_role_message = await client.wait_for('message', timeout = wait_timeout, check = check)
            except asyncio.TimeoutError:
                await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
                return
            else:
                verified_role_string = verified_role_message.content
                if verified_role_string.lower() == 'next':
                    break
                if verified_role_string.lower() == 'stop':
                    await ctx.channel.send(embed = stop_embed)
                    return
                _mongoFunctions.update_setting(ctx.guild.id, "verified_role", verified_role_string)
                break

        while True:
            await response_message.edit(embed = _embedMessage.create("Setup Reply", "What is the verification email domain? (E.g. @uwaterloo.ca)", "blue"))
            try:
                email_domain_message = await client.wait_for('message', timeout = wait_timeout, check = check)
            except asyncio.TimeoutError:
                await response_message.edit(embed = _embedMessage.create("Setup Reply", "You took too long to respond.", "red"))
                return
            else:
                email_domain = email_domain_message.content
                if email_domain.lower() == 'next':
                    break
                if email_domain.lower() == 'stop':
                    await ctx.channel.send(embed = stop_embed)
                    return
                _mongoFunctions.update_setting(ctx.guild.id, "email_domain", email_domain)
                break
