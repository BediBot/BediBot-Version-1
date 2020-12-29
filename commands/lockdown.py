from commands import _embedMessage, _checkrole, _util, _mongoFunctions
from discord.utils import get
from ._util import parse_message
import discord


async def lockdown(ctx: discord.message, client: discord.client):
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("Lockdown Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    args = parse_message(ctx.content)

    if len(args) == 2:
        try:
            role = get(ctx.guild.roles, name = args[1])
        except:
            replyEmbed = _embedMessage.create("Lockdown reply", "Invalid Role", "red")
            await ctx.channel.send(embed = replyEmbed)
            return
        replyEmbed = _embedMessage.create("Lockdown Reply", "Channel Locked for {}".format(args[1]), "green")
        await ctx.channel.send(embed = replyEmbed)

        await ctx.channel.set_permissions(role, send_messages = False, read_messages = True)

    else:
        replyEmbed = _embedMessage.create("Lockdown reply", "Error 404: Something went wrong", "red")
        await ctx.channel.send(embed = replyEmbed)


async def unlock(ctx: discord.message, client: discord.client):
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("Unlock Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    args = parse_message(ctx.content)
    try:
        role = get(ctx.guild.roles, name = args[1])
    except:
        replyEmbed = _embedMessage.create("Unlock reply", "Invalid Role", "red")
        await ctx.channel.send(embed = replyEmbed)

    replyEmbed = _embedMessage.create("Unlock Reply", "Channel Unlocked for {}".format(args[1]), "green")
    await ctx.channel.send(embed = replyEmbed)
    await ctx.channel.set_permissions(role, send_messages = True, read_messages = True)
