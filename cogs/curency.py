import os
import discord
from utils.data import getJSON

from discord.ext import commands
from datetime import datetime


class Curency(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.config = getJSON("config.json")
    

def setup(bot):
    bot.add_cog(Curency(bot))