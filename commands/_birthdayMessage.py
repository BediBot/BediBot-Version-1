import discord
from commands import _mongoFunctions, _embedMessage


async def send_birthday_message(client, guild_id, channel_id):
    guild_id = int(guild_id)
    channel_id = int(channel_id)
    guild = client.get_guild(guild_id)

    role = discord.utils.get(guild.roles, name = "Bedi's Favorite")

    for member in guild.members:
        if role in member.roles:
            await member.remove_roles(role)

    birthday_mentions = []

    user_documents = _mongoFunctions.get_all_birthdays_today(guild_id)
    print(user_documents)

    for document in user_documents:
        member = guild.get_member(document['user_id'])
        birthday_mentions.append(member.mention)
        await member.add_roles(role)

    if len(birthday_mentions) != 0:
        await guild.get_channel(channel_id).send(embed = _embedMessage.create("Happy Birthday!", "Happy birthday to:\n" + ' '.join(birthday_mentions), "blue"))
