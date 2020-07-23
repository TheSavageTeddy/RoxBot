import os
import sys
from os.path import getmtime

import discord
from discord.ext import commands, tasks

import json
from utils.data import getJSON

from termcolor import colored
from utils.cli_logging import *

#https://gist.github.com/Modelmat/ff2dc0953bf0f399fdd2083b74b4755d
def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixesJSON = json.load(f)

    if str(message.guild.id) in prefixesJSON:
        return prefixesJSON[str(message.guild.id)]
    else:
        prefixes = ['?']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '?'

    return commands.when_mentioned_or(*prefixes)(bot, message)

config = getJSON("config.json")

bot = commands.Bot(
    command_prefix=get_prefix,
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