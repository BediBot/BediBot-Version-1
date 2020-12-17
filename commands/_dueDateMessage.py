from commands import _embedMessage, _mongoFunctions


async def edit_due_date_message(client):
    guild_list = _mongoFunctions.get_guilds_information()

    for guild in guild_list:
        global guild_id, channel_id
        for key, value in guild.items():
            if key == 'guild_id':
                guild_id = value
            if key == 'channel_id':
                channel_id = value

        update_due_dates(guild_id)
        guild = client.get_guild(guild_id)

        courses = _mongoFunctions.get_list_of_courses(guild_id)

        for stream in _mongoFunctions.get_list_of_streams(guild_id):
            await edit_schedule_embed(stream, courses, guild_id, guild, channel_id)


async def edit_schedule_embed(stream, courses, guild_id, guild, channel_id):
    channel = guild.get_channel(channel_id)
    message_id = _mongoFunctions.get_due_date_channel_id(guild_id, stream)
    msg = await channel.fetch_message(message_id)

    message_embed = _embedMessage.create("Upcoming Due Dates for Stream " + str(stream), "​", "blue")

    for course in courses:
        due_dates = _mongoFunctions.get_all_upcoming_due_dates(guild_id, stream, course)

        for due_date in due_dates:
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

            if due_date['time_included']:
                current_due_date = " **Type:** " + due_date['type'].rjust(10) + " **Date:** " + due_date['date'].strftime("%m/%d/%Y, %H:%M:%S").rjust(10) + '\n​'
            else:
                current_due_date = " **Type:** " + due_date['type'].rjust(10) + " **Date:** " + due_date['date'].strftime("%m/%d/%Y").rjust(10) + '\n​'

            if due_date == due_dates[0]:
                title = "**" + course + "**\n" + emoji + "   " + due_date['title']
            else:
                title = emoji + "   " + due_date['title']

            message_embed.add_field(name = title, value = current_due_date, inline = False)
    await msg.edit(embed = message_embed)


def update_due_dates(guild_id):
    _mongoFunctions.remove_due_dates_passed(guild_id)
