import discord


async def giveRole(ctx, client, role):
    user = ctx.author
    role = discord.utils.get(ctx.guild.roles, name="role")
    await user.add_roles(role)
    await ctx.channel.send("Added role")