import os
import string

import discord
from dotenv import load_dotenv
from commands import _email

load_dotenv()
os.environ['UW_API_KEY'] = os.getenv('UW_API_KEY')
from uwaterloodriver import UW_Driver

uw_driver = UW_Driver()


async def confirm(ctx):
    email_address = ctx.content.split(" ")[1]
    unique_key = ctx.content.split(" ")[2]

    if unique_key == _email.verificationCodes.get(email_address):
        await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name="Verified"))

        user_id = email_address[:email_address.rfind('@')]

        department = uw_driver.directory_people_search(user_id).get('department').lower()

        if "mechatronics" in department:
            await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name="Tron"))
            await ctx.channel.send("You have been verified and given the Tron role")

        elif "mechanical" in department:
            await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name="Mechanical"))
            await ctx.channel.send("You have been verified and given the Mechanical role")
        else:
            await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name="Not Tron"))
            await ctx.channel.send("You have been verified and given the Not Tron role")
        return

    await ctx.channel.send("Invalid code!")
