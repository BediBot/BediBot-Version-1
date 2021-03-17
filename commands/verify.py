import os
import re

import discord
from dotenv import load_dotenv

from commands import _mongoFunctions, _embedMessage, _email



async def verify(ctx: discord.Message, client: discord.Client):
    await ctx.delete()

    if not _mongoFunctions.get_settings(ctx.guild.id)['verification_enabled']:
        replyEmbed = _embedMessage.create("Verify Reply", "Verification is not enabled on this server!", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    # This checks if the user is verified in the current guild
    if _mongoFunctions.is_user_id_linked_to_verified_user_in_guild(ctx.guild.id, ctx.author.id):
        replyEmbed = _embedMessage.create("Verify Reply",
                                          "Invalid Permissions - you are already verified! Run $unverify if you need to reverify yourself here.",
                                          "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    # Checks if the user is verified in ANY guild with the same verification email domain
    if _mongoFunctions.is_user_id_linked_to_verified_user_anywhere(ctx.guild.id, ctx.author.id):
        user_doc = _mongoFunctions.get_user_doc_from_verified_user_id(ctx.guild.id, ctx.author.id)
        _mongoFunctions.add_user_to_verified_users(ctx.guild.id, ctx.author.id, user_doc['uw_id'])
        await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name = _mongoFunctions.get_settings(ctx.guild.id)['verified_role']))
        replyEmbed = _embedMessage.create("Verify Reply", "You are already verified on another server, so you've been automatically verified.", "blue")
        await ctx.channel.send(embed = replyEmbed)
        await ctx.author.send(embed = replyEmbed)
        return

    message_contents = ctx.content.split(" ")

    if len(message_contents) != 2:
        await ctx.channel.send(embed = _embedMessage.create("Verify Reply", "The syntax is invalid! Make sure it is in the format $verify <emailaddress>", "red"))
        return

    email_address = message_contents[1]

    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email_address) and email_address.endswith(
        _mongoFunctions.get_settings(ctx.guild.id)['email_domain'])
    uw_id = email_address[:email_address.rfind('@')]

    if not match:
        await ctx.channel.send(embed = _embedMessage.create("Verify Reply", "Invalid email!", "red"))
        return

    # Commenting these lines since the V2 API will be deprecated
    # if uw_driver.directory_people_search(uw_id) == {}:
    #     await ctx.channel.send(embed = _embedMessage.create("Verify Reply", "That's not a valid uWaterloo email!", "red"))
    #     return

    # uw_id = uw_driver.directory_people_search(uw_id)['user_id']

    if _mongoFunctions.is_uw_id_linked_to_verified_user(ctx.guild.id, uw_id):
        await ctx.channel.send(embed = _embedMessage.create("Verify Reply", "That email is already linked to a user!", "red"))
        return

    if _mongoFunctions.is_uw_id_linked_to_pending_verification_user(ctx.guild.id, uw_id):
        await ctx.channel.send(embed = _embedMessage.create("Verify Reply", "Someone is already using that email to verify! If this is an error, contact an admin", "red"))
        return

    _email.send_confirmation_email(email_address, ctx.author.id)
    _mongoFunctions.add_user_to_pending_verification_users(ctx.guild.id, ctx.author.id, uw_id)
    await ctx.channel.send(embed = _embedMessage.create("Verify Reply", "Verification Email sent!", "blue"))
