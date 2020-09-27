import re

from commands import _email


async def verify(ctx):
    email_address = ctx.content.split(" ")[1]

    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email_address) and \
            email_address.endswith('@uwaterloo.ca')

    if not match:
        await ctx.channel.send("Invalid email!")
        return

    _email.send_confirmation_email(email_address)
    await ctx.channel.send("Verification Email sent!")
