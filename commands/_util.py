import os
import shlex

import discord
from dotenv import load_dotenv

load_dotenv()
BOT_OWNERS = os.getenv("BOT_OWNERS")
BOT_OWNERS = BOT_OWNERS.split(' ')


def parse_message(msg):
    msg = msg.replace('“', '"')
    msg = msg.replace('”', '"')
    return shlex.split(msg)


def author_is_bot_owner(ctx: discord.Message) -> bool:
    if str(ctx.author.id) in BOT_OWNERS:
        return True
    else:
        return False


async def purge_messages_in_channel(client: discord.Client, guild_id: int, channel_id: int):
    await client.get_guild(guild_id).get_channel(channel_id).purge(limit = None, check = lambda msg: not msg.pinned)


def get_guild_count(client: discord.Client):
    return len(client.guilds)


def get_member_count(client: discord.Client):
    member_count = 0

    for user in client.get_all_members():
        if not user.bot:
            member_count += 1

    return member_count
