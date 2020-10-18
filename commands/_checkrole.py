import discord

def checkIfAuthorHasRole(ctx, role:str):
    role = discord.utils.get(ctx.guild.roles, name = role)
    if role in ctx.author.roles:
        return True
    else:
        return False
