import discord
from datetime import date, datetime
from commands import _mongoFunctions, _embedMessage


async def send_morning_announcement(client, guild_id, channel_id):
    role = discord.utils.get(client.get_guild(guild_id).roles, name = _mongoFunctions.get_settings(guild_id)['announcement_role'])
    await client.get_guild(guild_id).get_channel(channel_id).send(role.mention, embed = _embedMessage.create("Good Morning!",
                                                                                                             _mongoFunctions.random_quote(guild_id,
                                                                                                                                          _mongoFunctions.get_settings(guild_id)[
                                                                                                                                              'announcement_quoted_person']),
                                                                                                             "blue"))
    _mongoFunctions.set_last_announcement_time(guild_id, datetime.now())


async def check_if_morning_announcement_occurred_today(client, guild_id, channel_id):
    last_announcement_time = _mongoFunctions.get_settings(guild_id)['last_announcement_time']
    if last_announcement_time is None or (last_announcement_time.date() != date.today()):
        await send_morning_announcement(client, guild_id, channel_id)
