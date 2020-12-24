import os
from threading import Thread

from dotenv import load_dotenv

load_dotenv()
BOT_OWNERS = os.getenv("BOT_OWNERS")
BOT_OWNERS = BOT_OWNERS.split(' ')


def parse_message(msg):
    ignoreSpace = False
    args = []
    start = 0
    for x in range(len(msg)):
        if msg[x] == ' ' and not ignoreSpace and not x == start:
            args.append(msg[start:x].strip())
            start = x + 1
        elif msg[x] == '"' and not ignoreSpace:
            start = x + 1
            ignoreSpace = True
        elif msg[x] == '"' and ignoreSpace:
            args.append(msg[start:x].strip())
            ignoreSpace = False
            start = x + 1
        elif x == len(msg) - 1:
            args.append(msg[start:len(msg)].strip())
    return args


def author_is_bot_owner(ctx):
    if str(ctx.author.id) in BOT_OWNERS:
        return True
    else:
        return False


async def purge_messages_in_channel(client, guild_id, channel_id):
    await client.get_guild(guild_id).get_channel(channel_id).purge(limit = None, check = lambda msg: not msg.pinned)


def run_threaded(func):
    thread = Thread(target = func)
    thread.start()
