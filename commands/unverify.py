import discord
from commands import _mongoFunctions, _embedMessage, _checkrole


async def unverify(ctx, client):
    if _mongoFunctions.get_verification_enabled(ctx.guild_id):
        replyEmbed = _embedMessage.create("Confirm Reply", "Verification is not enabled on this server!\nIf this is a mistake, contact a dev", "red")
        await ctx.channel.send(embed = replyEmbed)
        return
    
    if not _mongoFunctions.is_user_id_linked_to_verified_user(ctx.guild.id, ctx.author.id):
        replyEmbed = _embedMessage.create("Unverify Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    user_id = ctx.author.id

    if _mongoFunctions.is_user_id_linked_to_verified_user(ctx.guild.id, user_id):
        _mongoFunctions.remove_verified_user(ctx.guild.id, user_id)
        await ctx.channel.send(embed = _embedMessage.create("Unverify Reply", "You have been unverified", "blue"))
        for role in ctx.author.roles:
            try:
                await ctx.author.remove_roles(role)
            except:
                print("this didnt work LOL")
    return
