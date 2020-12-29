import os
import shlex

from dotenv import load_dotenv

load_dotenv()
BOT_OWNERS = os.getenv("BOT_OWNERS")
BOT_OWNERS = BOT_OWNERS.split(' ')


def parse_message(msg):
    msg = msg.replace('“', '"')
    return shlex.split(msg)


def author_is_bot_owner(ctx):
    if str(ctx.author.id) in BOT_OWNERS:
        return True
    else:
        return False


async def purge_messages_in_channel(client, guild_id, channel_id):
    await client.get_guild(guild_id).get_channel(channel_id).purge(limit = None, check = lambda msg: not msg.pinned)
