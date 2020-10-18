import discord

def checkIfAuthorHasRole(ctx, roleString:str):
    role = discord.utils.get(ctx.guild.roles, name = roleString)
    if role in ctx.author.roles:
        return True
    else:
        return False
