import os
import string
from commands import _mongoFunctions

import discord
from dotenv import load_dotenv
from commands import _email

load_dotenv()
os.environ['UW_API_KEY'] = os.getenv('UW_API_KEY')
from uwaterloodriver import UW_Driver

uw_driver = UW_Driver()


async def confirm(ctx):
    unique_key = ctx.content.split(" ")[1]

    email_address = _mongoFunctions.get_email_from_pending_user_id(ctx.author.id)

    if unique_key == _email.verificationCodes.get(email_address):
        await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name="Verified"))

        _mongoFunctions.add_user_to_verified_users(ctx.author.id, email_address)
        _mongoFunctions.remove_user_from_pending_verification_users(ctx.author.id)
        await ctx.channel.send("You have been verified")
        return

    await ctx.channel.send("Invalid code!")