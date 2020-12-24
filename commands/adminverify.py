import os
from commands import _mongoFunctions, _embedMessage, _checkrole, _util
from dotenv import load_dotenv

load_dotenv()
os.environ['UW_API_KEY'] = os.getenv('UW_API_KEY')
from uwaterloodriver import UW_Driver

uw_driver = UW_Driver()


async def admin_verify(ctx, client):
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("AdminVerify Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    message_contents = ctx.content.split(" ")

    if len(message_contents) != 2:
        await ctx.channel.send(embed = _embedMessage.create("Admin Verify Reply",
                                                            "The syntax is invalid! Make sure it is in the format $adminverify <User (Mention)>\nNote that this command does NOT assign a role, it only verifies them inside the database!",
                                                            "red"))
        return

    mention = message_contents[1]
    user_id = mention.replace("<", "").replace(">", "").replace("@", "").replace("!", "")

    _mongoFunctions.admin_add_user_to_verified_users(ctx.guild.id, user_id)
    await ctx.channel.send(embed = _embedMessage.create("Admin Verify reply", mention + "has been verified", "blue"))

    return
