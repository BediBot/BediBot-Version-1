import os
from commands import _mongoFunctions, _embedMessage, _email, _hashingFunctions, _checkrole
import discord
from dotenv import load_dotenv

load_dotenv()
os.environ['UW_API_KEY'] = os.getenv('UW_API_KEY')
from uwaterloodriver import UW_Driver

uw_driver = UW_Driver()


async def adminverify(ctx, client):
    if not (_checkrole.checkIfAuthorHasRole(ctx, "admin") or _checkrole.checkIfAuthorHasRole(ctx, "admins()")):
        replyEmbed = _embedMessage.create("SetBediBotChannel Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    message_contents = ctx.content.split(" ")

    if len(message_contents) != 2:
        await ctx.channel.send(embed = _embedMessage.create("Admin Verify Reply", "The syntax is invalid! Make sure it is in the format $adminverify <User (Mention)>\nNote that this command does NOT assign a role, it only verifies them inside the database!", "red"))
        return

    mention = message_contents[1]
    user_id = mention.replace("<", "")
    user_id = user_id.replace(">", "")
    user_id = user_id.replace("@", "")
    user_id = user_id.replace("!", "")

    _mongoFunctions.admin_add_user_to_verified_users(ctx.guild.id, user_id)
    await ctx.channel.send(embed = _embedMessage.create("Admin Verify reply", mention + "has been verified", "blue"))

    return
