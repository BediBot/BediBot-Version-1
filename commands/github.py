import discord
from commands import _embedMessage

smiley_face = "😊"

async def show_github(ctx: discord.Message, client: discord.Client):
    embedmsg = _embedMessage.create("GitHub Reply", "Bedibot is an open source project managed by Tron 2025's. If you'd like to contribute (or star... it means a lot " + smiley_face + "), head over to this link here:\n[Github Link](https://github.com/sahil-kale/tron-discord-bot)", "blue")
    await ctx.channel.send(embed = embedmsg)

