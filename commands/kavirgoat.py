import random

import discord

from commands import _embedMessage, _util

kavir_image_list = [
    "https://cdn.discordapp.com/attachments/753361850501955584/798554192012771358/Still_single.PNG",
    "https://cdn.discordapp.com/attachments/753361850501955584/798554196055818270/You.PNG",
    "https://cdn.discordapp.com/attachments/753361850501955584/798554202661584896/The_guy.PNG",
    "https://cdn.discordapp.com/attachments/753361850501955584/798554205937074206/too_cool.PNG",
    "https://cdn.discordapp.com/attachments/753361850501955584/798555482125893702/1.PNG",
    "https://cdn.discordapp.com/attachments/753361850501955584/798555485182623744/image.png",
    "https://cdn.discordapp.com/attachments/753361850501955584/798555485242392626/4.PNG",
    "https://cdn.discordapp.com/attachments/753361850501955584/798555484587819018/That_Damned_Smile_24112020214203.jpg",
    "https://cdn.discordapp.com/attachments/753361850501955584/798555486852087828/5.PNG",
    "https://cdn.discordapp.com/attachments/753361850501955584/798555488404242462/6.PNG",
    "https://cdn.discordapp.com/attachments/753361850501955584/798555488509624391/unknown_1.png",
    "https://cdn.discordapp.com/attachments/753361850501955584/798555488480395325/2.PNG",
    "https://cdn.discordapp.com/attachments/753361850501955584/798555489020936232/3.PNG",
    "https://cdn.discordapp.com/attachments/753361850501955584/798555489934770176/Capture.PNG"
]


async def kavir_goat(ctx: discord.Message, client: discord.Client):
    message_embed = _embedMessage.create("KavirGoat Reply", "Here is your Kavir pic.", "blue")
    message_embed.set_image(url = random.choice(kavir_image_list))
    await ctx.channel.send(embed = message_embed)
