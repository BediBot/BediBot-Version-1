from commands import _embedMessage, _mongoFunctions


async def edit_due_date_message(client):
    guild_list = _mongoFunctions.get_guilds_information()

    for guild in guild_list:
        for key, value in guild.items():
            if key == 'guild_id':
                guild_id = value
            if key == 'channel_id':
                channel_id = value

        guild = client.get_guild(guild_id)

        courses = _mongoFunctions.get_list_of_courses(guild_id)

        await edit_schedule_embed(4, courses, guild_id, guild, channel_id)

        await edit_schedule_embed(8, courses, guild_id, guild, channel_id)


async def edit_schedule_embed(stream, courses, guild_id, guild, channel_id):
    channel = guild.get_channel(channel_id)
    message_id = _mongoFunctions.get_due_date_channel_id(guild_id, stream)
    msg = await channel.fetch_message(message_id)

    messageEmbed = _embedMessage.create("Upcoming Due Dates for Stream " + str(stream), "​", "blue")

    for course in courses:

        duedates = _mongoFunctions.get_all_upcoming_due_dates(guild_id, stream, course)

        for duedate in duedates:
            if duedate['time_included']:
                current_due_date = " **Type:** " + duedate['type'].rjust(10) + " **Date:** " + duedate['date'].strftime("%m/%d/%Y, %H:%M:%S").rjust(10) + '\n​'
            else:
                current_due_date = " **Type:** " + duedate['type'].rjust(10) + " **Date:** " + duedate['date'].strftime("%m/%d/%Y").rjust(10) + '\n​'

            if duedate == duedates[0]:
                title = "**" + course + "**\n" + duedate['title']
            else:
                title = duedate['title']

            messageEmbed.add_field(name = title, value = current_due_date, inline = False)
    await msg.edit(embed = messageEmbed)


def update_due_dates(guild_id):
    _mongoFunctions.remove_due_dates_passed(guild_id)
