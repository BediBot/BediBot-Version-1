import discord
from discord.utils import get

from commands import _embedMessage, _checkrole, _util, _mongoFunctions
from ._util import parse_message


async def lockdown(ctx: discord.Message, client: discord.Client):
    # Checks if user is admin or bot owner
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("Lockdown Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    args = parse_message(ctx.content)

    if len(args) == 1:
        for role in ctx.guild.roles:
            try:
                perms = ctx.channel.overwrites_for(role)  # Use a permissions overwrite object
                perms.send_messages = False
                await ctx.channel.set_permissions(role, overwrite = perms)
            except:
                print("Unable to change permissions for {0}".format(role.name))
        replyEmbed = _embedMessage.create("Lockdown Reply", "Channel Locked for all possible roles", "green")
        await ctx.channel.send(embed = replyEmbed)

    elif len(args) == 2:
        role = get(ctx.guild.roles, name = args[1])
        if role is None:
            replyEmbed = _embedMessage.create("Lockdown Reply", "Invalid Role", "red")
            await ctx.channel.send(embed = replyEmbed)
            return
        else:
            replyEmbed = _embedMessage.create("Lockdown Reply", "Channel Locked for {}".format(args[1]), "green")
            await ctx.channel.send(embed = replyEmbed)

            # await ctx.channel.set_permissions(role, send_messages = False, read_messages = True)
            perms = ctx.channel.overwrites_for(role)  # Use a permissions overwrite object
            perms.send_messages = False
            await ctx.channel.set_permissions(role, overwrite = perms)

    else:
        replyEmbed = _embedMessage.create("Lockdown Reply", "This command needs can only take one argument.", "red")
        await ctx.channel.send(embed = replyEmbed)


async def unlock(ctx: discord.Message, client: discord.Client):
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("Unlock Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    args = parse_message(ctx.content)

    if len(args) == 1:
        for role in ctx.guild.roles:
            try:
                perms = ctx.channel.overwrites_for(role)  # Use a permissions overwrite object
                perms.send_messages = True
                await ctx.channel.set_permissions(role, overwrite = perms)
            except:
                print("Unable to change permissions for {0}".format(role.name))
        replyEmbed = _embedMessage.create("Unlock Reply", "Channel unlocked for all possible roles", "green")
        await ctx.channel.send(embed = replyEmbed)

    elif len(args) == 2:
        role = get(ctx.guild.roles, name = args[1])
        if role is None:
            replyEmbed = _embedMessage.create("Unlock reply", "Invalid Role", "red")
            await ctx.channel.send(embed = replyEmbed)
            return
        else:
            replyEmbed = _embedMessage.create("Unlock Reply", "Channel Unlocked for {}".format(args[1]), "green")
            await ctx.channel.send(embed = replyEmbed)
            # await ctx.channel.set_permissions(role, send_messages = True, read_messages = True)
            perms = ctx.channel.overwrites_for(role)  # Use a permissions overwrite object
            perms.send_messages = True
            await ctx.channel.set_permissions(role, overwrite = perms)

    else:
        replyEmbed = _embedMessage.create("Unlock Reply", "This command needs can only take one argument.", "red")
        await ctx.channel.send(embed = replyEmbed)
