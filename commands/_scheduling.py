from datetime import datetime, timedelta

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from commands import _birthdayMessage, _mongoFunctions, _dueDateMessage, _morningAnnouncement, _util

scheduler = AsyncIOScheduler()
scheduler.start()


async def schedule_jobs(client: discord.Client):
    guild_list = _mongoFunctions.get_guilds_information()

    for guild_dict in guild_list:
        guild_id = guild_list[guild_dict]['guild_id']

        # Checks if channel actually exists in guild
        try:
            channel_id = client.get_guild(guild_id).get_channel(int(_mongoFunctions.get_settings(guild_id)['channel_id'])).id
        except:
            continue

        guild_timezone = guild_list[guild_dict]['timezone']

        # Purges (unpinned) messages in channel at end of day
        scheduler.add_job(_util.purge_messages_in_channel, 'cron', hour = 23, minute = 59, second = 0, timezone = guild_timezone, args = [client, guild_id, channel_id])

        if guild_list[guild_dict]['birthday_announcements_enabled']:
            birthday_time = guild_list[guild_dict]['birthday_time'].split(':')

            scheduler.add_job(_birthdayMessage.send_birthday_message, 'cron', hour = int(birthday_time[0]), minute = int(birthday_time[1]), second = 1, timezone = guild_timezone,
                              args = [client, guild_id, channel_id])

        if guild_list[guild_dict]['morning_announcements_enabled']:
            announcement_time = guild_list[guild_dict]['announcement_time'].split(':')

            announcement_time_object = datetime.today()
            announcement_time_object = announcement_time_object.replace(hour = int(announcement_time[0]), minute = int(announcement_time[1]))

            scheduler.add_job(_morningAnnouncement.send_morning_announcement, 'cron', hour = announcement_time_object.hour, minute = announcement_time_object.minute, second = 1,
                              timezone = guild_timezone, args = [client, guild_id, channel_id])

            # Does announcement check five minutes after announcement time (To handle edge case where bot goes offline during announcement time
            announcement_time_object += timedelta(minutes = 5)
            scheduler.add_job(_morningAnnouncement.check_if_morning_announcement_occurred_today, 'cron', hour = announcement_time_object.hour,
                              minute = announcement_time_object.minute,
                              second = 1, timezone = guild_timezone, args = [client, guild_id, channel_id])

    due_date_edit_interval = 10
    scheduler.add_job(_dueDateMessage.edit_due_date_message, 'interval', minutes = due_date_edit_interval, args = [client])


# Removes all jobs and reschedules them
async def reschedule_jobs(client: discord.Client):
    for job in scheduler.get_jobs():
        job.remove()

    await schedule_jobs(client)
