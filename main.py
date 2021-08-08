import traceback
from os.path import join

import discord
import logging
from discord.ext import commands
import os
from dotenv import load_dotenv

from utils.guild import get_prefix

load_dotenv()

token = os.getenv('BOT_TOKEN')
BOT_OWNERS = list(map(int, os.getenv("BOT_OWNERS").split(' ')))

print(BOT_OWNERS)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename = 'discord.log', encoding = 'utf-8', mode = 'w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix = get_prefix, owner_ids = BOT_OWNERS)


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    print(f'Successfully logged in and booted...!')


cogs_dir = "cogs"

if __name__ == "__main__":
    for (dir_path, dir_names, filenames) in os.walk(cogs_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                extension = join(dir_path, filename).replace('.py', '').replace('\\', '.')
                try:
                    bot.load_extension(extension)
                except (discord.ClientException, ModuleNotFoundError):
                    print(f'Failed to load extension {extension}.')
                    traceback.print_exc()

    bot.run(token, bot = True, reconnect = True)
