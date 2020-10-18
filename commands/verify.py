import os
import re
from dotenv import load_dotenv
from commands import _mongoFunctions, _embedMessage, _email
from uwaterloodriver import UW_Driver

load_dotenv()
os.environ['UW_API_KEY'] = os.getenv('UW_API_KEY')
uw_driver = UW_Driver()


async def verify(ctx, client):
    message_contents = ctx.content.split(" ")

    if len(message_contents) != 2:
        await ctx.channel.send(embed = _embedMessage.create("Verify Reply", "The syntax is invalid! Make sure it is in the format $verify <emailaddress>", "red"))
        return

    email_address = message_contents[1]

    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email_address) and email_address.endswith('@uwaterloo.ca')

    if not match:
        await ctx.channel.send(embed = _embedMessage.create("Verify Reply", "Invalid email!", "red"))
        return

    if uw_driver.directory_people_search(email_address[:email_address.rfind('@')]) == {}:
        await ctx.channel.send(embed = _embedMessage.create("Verify Reply", "That's not a valid uWaterloo email!", "red"))
        return

    if _mongoFunctions.is_email_linked_to_verified_user(ctx.guild.id, email_address):
        await ctx.channel.send(embed = _embedMessage.create("Verify Reply", "That email is already linked to a user!", "red"))
        return

    _email.send_confirmation_email(email_address, ctx.author.id)
    _mongoFunctions.add_user_to_pending_verification_users(ctx.guild.id, ctx.author.id, email_address)
    await ctx.channel.send(embed = _embedMessage.create("Verify Reply", "Verification Email sent!", "blue"))

    return
