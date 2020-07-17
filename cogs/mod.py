import os
import time
import discord
from utils.data import getJSON


from discord.ext import commands
from datetime import datetime

class Moderator(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.config = getJSON("config.json")
    
    @commands.command(
        name='kick',
        description='Kicks a member from the server',
        aliases=[]
    )
    async def kick(self, ctx):    
        pass
                

    

def setup(bot):
    bot.add_cog(Moderator(bot))