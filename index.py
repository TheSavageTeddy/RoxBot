import os
import sys
from os.path import getmtime

import discord
from discord.ext import commands, tasks

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