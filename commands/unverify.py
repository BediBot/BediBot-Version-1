import discord

from commands import _mongoFunctions


async def unverify(ctx):
    user_id = ctx.author.id

    if _mongoFunctions.is_user_id_linked_to_verified_user(user_id):
        _mongoFunctions.remove_verified_user(user_id)
        await ctx.channel.send("You have been unverified")
        await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, name="Verified"))
        return

    await ctx.channel.send("You are not verified")