import discord

from commands import _mongoFunctions, _embedMessage


async def unverify(ctx: discord.Message, client: discord.Client):
    if not _mongoFunctions.get_settings(ctx.guild.id)['verification_enabled']:
        replyEmbed = _embedMessage.create("Confirm Reply", "Verification is not enabled on this server!", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    if not _mongoFunctions.is_user_id_linked_to_verified_user_in_guild(ctx.guild.id, ctx.author.id):
        replyEmbed = _embedMessage.create("Unverify Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return
    else:
        user_id = ctx.author.id
        _mongoFunctions.remove_verified_user(ctx.guild.id, user_id)
        await ctx.channel.send(embed = _embedMessage.create("Unverify Reply", "You have been unverified", "blue"))
        try:
            await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, name = _mongoFunctions.get_settings(ctx.guild.id)['verified_role']))
        except:
            print("this didnt work LOL")
