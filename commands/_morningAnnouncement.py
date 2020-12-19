import discord
from datetime import date, datetime
from commands import _birthdayMessage, _mongoFunctions, _setBotStatus, _dueDateMessage, _embedMessage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


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
    scheduler.add_job(send_morning_announcement, 'cron', hour = 8, minute = 30, second = 0, args = [client])
    scheduler.add_job(_dueDateMessage.edit_due_date_message, 'interval', minutes = 1, args = [client])
    scheduler.start()
