import os
import time
import discord
from utils.data import getJSON

from discord.ext import commands
from datetime import datetime

class Emotes(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.config = getJSON("config.json")
    
    @commands.command(
        name='emote',
        description='Sends animated emotes for you',
        aliases=['emotes', 'blob', 'bloob', 'blooob', 'bloooob', 'blooooob', 'bloooooob', 'blooooooob'],
        usage='cog'
    )
    async def emote(self, ctx, *, text=''):
        """ Specify the emote after and the bot will send the emote for you!
        """
        emotes_list = {
            'blob':'<a:blob:644339810432974872>', 
            'bloob':'<a:bloob:644339810672050176>',
            'blooob':'<a:blooob:644339813297684511>',
            'bloooob':'<a:bloooob:644339814245728266>',
            'blooooob':'<a:blooooob:644339820579258369>',
            'bloooooob':'<a:bloooooob:644339813092163624>',
            'blooooooob':'<a:bloooooob:649127203329802259>',
            'trash bloob':'<a:bloooooob:649127203329802259>'
        }

        if ctx.invoked_with in [*emotes_list]:
            await ctx.send(f"{emotes_list[ctx.invoked_with]}")
        else:
            try:
                await ctx.send(f"{emotes_list[str(text)]}")
            except KeyError:
                await ctx.send("No emote found :x:")

def setup(bot):
    bot.add_cog(Emotes(bot))