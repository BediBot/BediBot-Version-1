# I totally stole that syntax validation thing from https://www.scottbrady91.com/Email-Verification/Python-Email-Verification-Script
import os
import re
from dotenv import load_dotenv
from commands import _mongoFunctions

from commands import _email

load_dotenv()
os.environ['UW_API_KEY'] = os.getenv('UW_API_KEY')
from uwaterloodriver import UW_Driver

uw_driver = UW_Driver()


async def verify(ctx):
    email_address = ctx.content.split(" ")[1]

    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email_address) and \
            email_address.endswith('@uwaterloo.ca')

    if not match:
        await ctx.channel.send("Invalid email!")
        return

    if uw_driver.directory_people_search(email_address[:email_address.rfind('@')]) == {}:
        await ctx.channel.send("That's not a valid uWaterloo email!")
        return

    if _mongoFunctions.is_email_linked_to_verified_user(email_address):
        await ctx.channel.send("That email is already linked to a user!")
        return

    _email.send_confirmation_email(email_address)
    _mongoFunctions.add_user_to_pending_verification_users(ctx.author.id, email_address)
    await ctx.channel.send("Verification Email sent!")
