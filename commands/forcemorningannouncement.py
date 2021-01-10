import discord

from commands import _birthdayMessage, _mongoFunctions, _checkrole, _embedMessage, _util, _morningAnnouncement


async def force_announcement(ctx: discord.Message, client: discord.Client):
    # Checks if user is admin or bot owner
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("ForceAnnouncement Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    await _morningAnnouncement.send_morning_announcement(client, ctx.guild.id, _mongoFunctions.get_settings(ctx.guild.id)['announcement_channel_id'])
    await ctx.channel.send(embed = _embedMessage.create("ForceAnnouncement Reply", "Announcement has been **FORCED**", "blue"))
    return
