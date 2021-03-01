from datetime import datetime, timedelta

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from commands import _birthdayMessage, _mongoFunctions, _dueDateMessage, _morningAnnouncement, _util, _setBotStatus

scheduler = AsyncIOScheduler()
scheduler.start()


async def schedule_jobs(client: discord.Client):
    guild_list = _mongoFunctions.get_guilds_information()

    for guild_dict in guild_list:
        guild_id = guild_list[guild_dict]['guild_id']
        guild_timezone = guild_list[guild_dict]['timezone']

        # Checks if channel actually exists in guild
        if guild_list[guild_dict]['due_dates_enabled']:
            try:
                due_date_channel_id = client.get_guild(guild_id).get_channel(int(_mongoFunctions.get_settings(guild_id)['due_date_channel_id'])).id

                # Purges (unpinned) messages in due date channel at end of day
                scheduler.add_job(_util.purge_messages_in_channel, 'cron', hour = 23, minute = 59, second = 0, timezone = guild_timezone,
                                  args = [client, guild_id, due_date_channel_id])
            except:
                print("Error scheduling due dates for guild ID: {0}".format(str(client.get_guild(guild_id))))

        if guild_list[guild_dict]['birthday_announcements_enabled']:
            try:
                birthday_channel_id = client.get_guild(guild_id).get_channel(int(_mongoFunctions.get_settings(guild_id)['birthday_channel_id'])).id
                birthday_time = guild_list[guild_dict]['birthday_time'].split(':')

                scheduler.add_job(_birthdayMessage.send_birthday_message, 'cron', hour = int(birthday_time[0]), minute = int(birthday_time[1]), second = 1,
                                  timezone = guild_timezone, args = [client, guild_id, birthday_channel_id])
            except:
                print("Error scheduling birthdays for guild ID: {0}".format(guild_id))

        if guild_list[guild_dict]['morning_announcements_enabled']:
            try:
                announcement_channel_id = client.get_guild(guild_id).get_channel(int(_mongoFunctions.get_settings(guild_id)['announcement_channel_id'])).id
                announcement_time = guild_list[guild_dict]['announcement_time'].split(':')

                announcement_time_object = datetime.today()
                announcement_time_object = announcement_time_object.replace(hour = int(announcement_time[0]), minute = int(announcement_time[1]))

                scheduler.add_job(_morningAnnouncement.send_morning_announcement, 'cron', hour = announcement_time_object.hour, minute = announcement_time_object.minute,
                                  second = 1,
                                  timezone = guild_timezone, args = [client, guild_id, announcement_channel_id])

                # Does announcement check five minutes after announcement time (To handle edge case where bot goes offline during announcement time
                announcement_time_object += timedelta(minutes = 5)
                scheduler.add_job(_morningAnnouncement.check_if_morning_announcement_occurred_today, 'cron', hour = announcement_time_object.hour,
                                  minute = announcement_time_object.minute,
                                  second = 1, timezone = guild_timezone, args = [client, guild_id, announcement_channel_id])
            except:
                print("Error scheduling morning announcements for guild ID: {0}".format(guild_id))

    due_date_edit_interval = 10
    scheduler.add_job(_dueDateMessage.edit_due_date_message, 'interval', minutes = due_date_edit_interval, args = [client])
    scheduler.add_job(_setBotStatus.set_random_bot_status, 'interval', hours = 1, args = [client])


# Removes all jobs and reschedules them
async def reschedule_jobs(client: discord.Client):
    for job in scheduler.get_jobs():
        job.remove()

    await schedule_jobs(client)
