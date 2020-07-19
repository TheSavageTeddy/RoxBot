import os
import sys
from os.path import getmtime

import discord
from discord.ext import commands, tasks
from tasks import loop

import json
from utils.data import getJSON

from termcolor import colored
from utils.cli_logging import *


config = getJSON("config.json")

bot = commands.Bot(
    command_prefix=config.prefix,
    prefix=config.prefix,
    owner_id=config.owners,
    case_insensitive=True
)

@loop(seconds=60)
async def check_for_change():
    info("Checking for New Update")
    WATCHED_FILES = ["index.py", "cogs/easter.py", "cogs/events.py", "cogs/image.py", "cogs/info.py", "cogs/mod.py", "cogs/music.py", "cogs/other.py", "cogs/utility.py", "utils/cli_logging.py", "utils/data.py", "utils/safe_math.py", "utils/start_server.py", "utils/web_api.py", 'test.txt']
    WATCHED_FILES_MTIMES = [(f, getmtime(f)) for f in WATCHED_FILES]
    process("Pulling from git")
    os.system("git pull")

    for f, mtime in WATCHED_FILES_MTIMES:
        if getmtime(f) != mtime:
            # One of the files has changed, so restart the script.
            info('Change Detected...')
            process('--> restarting')
            # When running the script via `./daemon.py` (e.g. Linux/Mac OS), use
            #os.execv(__file__, sys.argv)
            # When running the script via `python daemon.py` (e.g. Windows), use
            os.execv(sys.executable, ['python'] + sys.argv)

@bot.event
async def on_ready():                                       # Do this when the bot is logged in
    info(f'Logged in as {bot.user.name} - {bot.user.id}')  # Print the name and ID of the bot logged in.
    return

bot.remove_command('help')
for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

bot.run(config.token, bot=True, reconnect=True)