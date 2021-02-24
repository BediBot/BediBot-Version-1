import discord

async def kick_user(member: discord.Member, reason: str): 
    await member.kick(reason=reason)

async def ban_user(member: discord.Member, reason: str):
    await member.ban(reason=reason)