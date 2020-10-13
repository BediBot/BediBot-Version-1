import os
from commands import _mongoFunctions, _embedMessage, _email
import discord
from dotenv import load_dotenv

load_dotenv()
os.environ['UW_API_KEY'] = os.getenv('UW_API_KEY')
from uwaterloodriver import UW_Driver

uw_driver = UW_Driver()


async def confirm(ctx):
    message_contents = ctx.content.split(" ")

    if len(message_contents) != 2:
        await ctx.channel.send(embed = _embedMessage.create("Confirm Reply", "The syntax is invalid! Make sure it is in the format $confirm <confirmcode>", "blue"))
        return

    unique_key = message_contents[1]

    email_address = _mongoFunctions.get_email_from_pending_user_id(ctx.author.id)

    if unique_key == _email.verificationCodes.get(ctx.author.id):
        await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name = "Verified"))

        _mongoFunctions.add_user_to_verified_users(ctx.author.id, email_address)
        _mongoFunctions.remove_user_from_pending_verification_users(ctx.author.id)
        await ctx.channel.send(embed = _embedMessage.create("Confirm reply", "You have been verified", "blue"))
        return

    await ctx.channel.send(embed = _embedMessage.create("Confirm reply", "Invalid Code!", "blue"))

    return
