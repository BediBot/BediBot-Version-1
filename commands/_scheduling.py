from datetime import datetime, timedelta
from commands import _birthdayMessage, _mongoFunctions, _setBotStatus, _dueDateMessage, _morningAnnouncement
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


async def schedule_jobs(client):
    guild_list = _mongoFunctions.get_guilds_information()

    for guild in guild_list:
        guild_id = guild['guild_id']
        channel_id = guild['channel_id']

        time = _mongoFunctions.get_announcement_time(guild_id).split(':')
        time_object = datetime.today()
        time_object = time_object.replace(hour = int(time[0]), minute = int(time[1]))

        scheduler.add_job(_birthdayMessage.send_birthday_message, 'cron', hour = 0, minute = 0, second = 1, args = [client, guild_id, channel_id])
        scheduler.add_job(_morningAnnouncement.send_morning_announcement, 'cron', hour = time_object.hour, minute = time_object.minute, second = 1,
                          args = [client, guild_id, channel_id])
        time_object += timedelta(minutes = 5)
        scheduler.add_job(_morningAnnouncement.check_if_morning_announcement_occurred_today, 'cron', hour = time_object.hour, minute = time_object.minute, second = 1,
                          args = [client, guild_id, channel_id])

    scheduler.add_job(_dueDateMessage.edit_due_date_message, 'interval', minutes = 1, args = [client])
    scheduler.start()
