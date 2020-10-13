import asyncio
import threading
import time
import schedule
from commands import _birthdayMessage, _mongoFunctions

GUILD_ID = 760615522130984980
CHANNEL_ID = 760615523145875494

schedule_stop = threading.Event()


def timer():
    while not schedule_stop.is_set():
        schedule.run_pending()
        time.sleep(1)


schedule_thread = threading.Thread(target = timer)
schedule_thread.start()


async def send_morning_announcement(client):
    guild_list = _mongoFunctions.get_guilds_information()

    for guild in guild_list:
        for key, value in guild.items():
            if key == 'guild_id':
                guild_id = value
            if key == 'channel_id':
                channel_id = value
        await _birthdayMessage.send_birthday_message(client, guild_id, channel_id)


async def schedule_announcement(client):
    schedule.every().day.at("13:57").do(
        asyncio.run_coroutine_threadsafe, send_morning_announcement(client), client.loop)
