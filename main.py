import os
import discord
from dotenv import load_dotenv
from commands import *
from commands import _setBotStatus, _scheduling, _mongoFunctions

commands = {
    "verify": verify,
    "confirm": confirm,
    "unverify": unverify,
    "setbirthday": set_birthday,
    "addduedate": add_due_date,
    "help": help_command,
    "setduedatechannel": set_due_date_channel,
    "ping": ping,
    "parse": parse_command,
    "addquote": add_quote,
    "getquotes": get_quotes,
    "removequote": remove_quote,
    "adminverify": admin_verify,
    "removeduedate": remove_due_date,
    "forcebirthdays": force_birthdays,
    "say": say,
    "lockdown": lockdown,
    "unlock": unlock,
    "settings": settings,
    "getbirthdays": get_birthdays,
    "setup": setup,
    "forceannouncement": force_announcement,
    "setupannouncement": setup_announcement,
    "setupbirthdays": setup_birthdays,
    "setupduedates": setup_due_dates,
    "setupquotes": setup_quotes,
    "setupverification": setup_verification,
    "getrandomquote": get_random_quote,
    "kavirgoat": kavir_goat
}

reaction_handler_prefix = "|"

reactionHandlers = {
    reaction_handler_prefix: quotes_reaction_handler,
}

intents = discord.Intents.all()
client = discord.Client(intents = intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await _mongoFunctions.init(client)
    await _setBotStatus.set_random_bot_status(client)
    await _scheduling.schedule_jobs(client)


@client.event
async def on_message(ctx):
    if ctx.author == client.user:
        return

    prefix = _mongoFunctions.get_settings(ctx.guild.id)['prefix']

    if ctx.content.startswith(prefix):
        # Checks if the first word of the message's content (with the prefix removed) is in the dict of commands
        command_string = ctx.content.split(" ")[0][len(prefix):].lower()

        if command_string in commands:
            await commands[command_string](ctx, client)


@client.event
async def on_raw_reaction_add(reaction_payload: discord.RawReactionActionEvent):
    if reaction_payload.member.bot:
        return

    message = await client.get_channel(reaction_payload.channel_id).fetch_message(reaction_payload.message_id)

    if message.author == client.user:
        if message.embeds[0].description.split(" ")[0] in reactionHandlers:
            await reactionHandlers[message.embeds[0].description.split(" ")[0]](reaction_payload, message)


@client.event
async def on_reaction_add(reaction, user):
    ctx = reaction.message
    #if not _mongoFunctions.get_settings(ctx.guild.id)['pin_enabled']:
    #  replyEmbed = _embedMessage.create("Verify Reply", "Verification is not enabled on this server!", "red")
    # await ctx.channel.send(embed = replyEmbed)
    #return

    if str(reaction.emoji) == "📌":
        await reaction.message.pin()


@client.event
async def on_reaction_remove(reaction, user):
    #if not _mongoFunctions.get_settings(ctx.guild.id)['pin_enabled']:
    #    replyEmbed = _embedMessage.create("Verify Reply", "Verification is not enabled on this server!", "red")
    #await ctx.channel.send(embed = replyEmbed)
    #return

    if reaction.emoji == "📌":
        if not ":pushpin:" in [reaction.emoji for reaction in reaction.message.reactions]:
            await reaction.message.unpin()


if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")
    client.run(TOKEN)
