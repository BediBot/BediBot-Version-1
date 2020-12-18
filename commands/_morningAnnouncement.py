import asyncio
import threading
import time
import discord
from datetime import date, datetime

import schedule
from commands import _birthdayMessage, _mongoFunctions, _setBotStatus, _dueDateMessage, _embedMessage

schedule_stop = threading.Event()


def timer():
    while not schedule_stop.is_set():
        schedule.run_pending()
        time.sleep(1)


schedule_thread = threading.Thread(target = timer)
schedule_thread.start()


async def send_morning_announcement(client):
    guild_list = _mongoFunctions.get_guilds_information()
    await _setBotStatus.set_random_bot_status(client)

    for guild in guild_list:
        global guild_id, channel_id
        for key, value in guild.items():
            if key == 'guild_id':
                guild_id = value
            if key == 'channel_id':
                channel_id = value
        await client.get_guild(guild_id).get_channel(channel_id).purge(limit = None, check = lambda msg: not msg.pinned)
        role = discord.utils.get(client.get_guild(guild_id).roles, name = _mongoFunctions.get_announcement_role_string(guild_id))
        await client.get_guild(guild_id).get_channel(channel_id).send(role.mention,
                                                                      embed = _embedMessage.create("Good Morning Trons!", _mongoFunctions.random_quote(guild_id, "bedi"), "blue"))
        await _birthdayMessage.send_birthday_message(client, guild_id, channel_id)
        _mongoFunctions.set_last_announcement_time(guild_id, datetime.now())


async def check_if_morning_announcement_occurred_today(client):
    guild_list = _mongoFunctions.get_guilds_information()

    for guild in guild_list:
        global guild_id
        for key, value in guild.items():
            if key == 'guild_id':
                guild_id = value

        last_announcement_time = _mongoFunctions.get_last_announcement_time(guild_id)
        if last_announcement_time is None or (last_announcement_time.date() != date.today()):
            await send_morning_announcement(client)


async def schedule_announcement(client):
    schedule.every().day.at("08:30").do(asyncio.run_coroutine_threadsafe, send_morning_announcement(client), client.loop)
    # schedule.every().day.at("08:35").do(asyncio.run_coroutine_threadsafe, check_if_morning_announcement_occurred_today(client), client.loop)
    schedule.every().minute.do(asyncio.run_coroutine_threadsafe, _dueDateMessage.edit_due_date_message(client), client.loop)
