import discord
from commands import _mongoFunctions, _embedMessage


async def send_birthday_message(client: discord.Client, guild_id: int, channel_id: int):
    guild_id = int(guild_id)
    channel_id = int(channel_id)

    guild = client.get_guild(guild_id)

    birthday_role = discord.utils.get(guild.roles, name = _mongoFunctions.get_settings(guild_id)['birthday_role'])

    # Remove Birthday Role from all Members
    for member in guild.members:
        if birthday_role in member.roles:
            await member.remove_roles(birthday_role)

    birthday_mentions = []

    user_documents = _mongoFunctions.get_all_birthdays_today()

    # Checks if member exists in guild, adds their mention to list of mentions, and gives them birthday role
    for document in user_documents:
        member = discord.utils.get(guild.members, id = document['user_id'])
        if member is None:
            continue
        birthday_mentions.append(member.mention)
        await member.add_roles(birthday_role)

    if len(birthday_mentions) != 0:
        await guild.get_channel(int(channel_id)).send(embed = _embedMessage.create("Happy Birthday!", "Happy birthday to:\n" + ' '.join(birthday_mentions), "blue"))
