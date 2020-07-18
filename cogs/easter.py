import os
import discord
from utils.data import getJSON

from discord.ext import commands
from datetime import datetime

class EasterEggs(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.config = getJSON("config.json")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if "the earth king has invited you to lake laogai" in message.content.lower():
            await message.channel.send("I am honoured to accept his invitation.")

def setup(bot):
    bot.add_cog(EasterEggs(bot))
