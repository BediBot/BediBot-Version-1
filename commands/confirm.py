import os
from commands import _mongoFunctions, _embedMessage, _email, _hashingFunctions
import discord
from dotenv import load_dotenv

load_dotenv()
os.environ['UW_API_KEY'] = os.getenv('UW_API_KEY')
from uwaterloodriver import UW_Driver

uw_driver = UW_Driver()


async def confirm(ctx, client):
    if _mongoFunctions.get_verification_enabled(ctx.guild_id):
        replyEmbed = _embedMessage.create("Confirm Reply", "Verification is not enabled on this server!\nIf this is a mistake, contact a dev", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    if _mongoFunctions.is_user_id_linked_to_verified_user(ctx.guild.id, ctx.author.id):
        replyEmbed = _embedMessage.create("Confirm Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    message_contents = ctx.content.split(" ")

    if len(message_contents) != 2:
        await ctx.channel.send(embed = _embedMessage.create("Confirm Reply", "The syntax is invalid! Make sure it is in the format $confirm <confirmcode>", "red"))
        return
    uw_id = _mongoFunctions.get_uw_id_from_pending_user_id(ctx.guild.id, ctx.author.id)

    unique_key = message_contents[1]
    if unique_key == _email.verificationCodes.get(ctx.author.id):
        department = uw_driver.directory_people_search(uw_id)['department']

        if department == "ENG/Mechanical & Mechatronics":
            await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name = "Tron"))
        else:
            await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name = "Not Tron"))

        _mongoFunctions.add_user_to_verified_users(ctx.guild.id, ctx.author.id, _hashingFunctions.hash_user_id(uw_id))
        _mongoFunctions.remove_user_from_pending_verification_users(ctx.guild.id, ctx.author.id)
        await ctx.channel.send(embed = _embedMessage.create("Confirm reply", "You have been verified", "blue"))

        return

    await ctx.channel.send(embed = _embedMessage.create("Confirm reply", "Invalid Code!", "red"))

    return
