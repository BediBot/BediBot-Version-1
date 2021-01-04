import discord

from commands import _embedMessage, _mongoFunctions


# Edit's due date message(s) for all guilds
async def edit_due_date_message(client: discord.Client):
    guild_list = _mongoFunctions.get_guilds_information()

    for guild_dict in guild_list:
        guild_id = guild_list[guild_dict]['guild_id']

        # Updates due dates if due dates are enabled
        if guild_list[guild_dict]['due_dates_enabled']:
            update_due_dates(guild_id)

            guild_object = client.get_guild(guild_id)

            courses = guild_list[guild_dict]['courses']
            channel_id = guild_list[guild_dict]['channel_id']

            for stream in guild_list[guild_dict]['streams']:
                try:
                    await edit_due_date_embed(stream, courses, guild_id, guild_object, channel_id)
                except:
                    print("Error in edit_schedule_embed")
                    print("server id: " + str(guild_dict))


async def edit_due_date_embed(stream: int, courses: list[str], guild_id: int, guild: discord.Guild, channel_id: int):
    channel = guild.get_channel(channel_id)

    message_id = _mongoFunctions.get_settings(guild_id)['stream_' + str(stream) + '_message_id']

    due_date_message = await channel.fetch_message(message_id)

    # Zero Width Space is used as embed body as field cannot be empty
    message_embed = _embedMessage.create("Upcoming Due Dates for Stream " + str(stream), "​", "blue")

    for course in courses:
        due_dates = _mongoFunctions.get_all_upcoming_due_dates(guild_id, stream, course)

        for due_date in due_dates:
            # Sets emojis for some generic due date types or uses :placard: by default
            if due_date['type'] == "Assignment":
                emoji = ":pushpin:"
            elif due_date['type'] == "Test":
                emoji = ":bulb:"
            elif due_date['type'] == "Exam":
                emoji = ":pen_ballpoint:"
            elif due_date['type'] == "Project":
                emoji = ":books:"
            elif due_date['type'] == "Quiz":
                emoji = ":pencil:"
            else:
                emoji = ":placard:"

            # Creates string to represent due date information
            if due_date['time_included']:
                current_due_date = " **Type:** " + due_date['type'].rjust(10) + " **Date:** " + due_date['date'].strftime("%m/%d/%Y, %H:%M:%S").rjust(10) + '\n​'
            else:
                current_due_date = " **Type:** " + due_date['type'].rjust(10) + " **Date:** " + due_date['date'].strftime("%m/%d/%Y").rjust(10) + '\n​'

            # Creates string to represent due date title, including course name if its the first due date for that course
            if due_date == due_dates[0]:
                title = "**" + course + "**\n" + emoji + "   " + due_date['title']
            else:
                title = emoji + "   " + due_date['title']

            message_embed.add_field(name = title, value = current_due_date, inline = False)
    await due_date_message.edit(embed = message_embed)


def update_due_dates(guild_id: int):
    _mongoFunctions.remove_due_dates_passed(guild_id)
