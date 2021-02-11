import discord

from commands import _mongoFunctions, _util, _embedMessage, _checkrole


async def pins_reaction_handler(reaction: discord.Reaction, user: discord.Member, remove: bool):
    if not _mongoFunctions.get_settings(user.guild.id)['pins_enabled']:
        return

    if not remove:
        if str(reaction.emoji) == "📌":
            await reaction.message.pin()
    else:
        if reaction.emoji == "📌":
            if not ":pushpin:" in [reaction.emoji for reaction in reaction.message.reactions]:
                await reaction.message.unpin()
