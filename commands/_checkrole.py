import discord


def author_has_role(ctx: discord.Message, role_string: str):
    role = discord.utils.get(ctx.guild.roles, name = role_string)
    if role in ctx.author.roles:
        return True
    else:
        return False
