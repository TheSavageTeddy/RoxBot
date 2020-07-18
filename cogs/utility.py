import os
import time
import discord
import random
from utils.data import getJSON

from discord.ext import commands
from datetime import datetime

from utils.safe_math import NumericStringParser


class Utility(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.config = getJSON("config.json")
    
    @commands.command(
        name='math',
        description='Evaluates the maths equations',
        aliases=['maths', 'calc', 'calculat', 'add', 'addition', 'multiply', 'calculate'],
    )
    async def math_command(self, ctx):
        msg = ctx.message.content

        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        equation = msg[len(prefix_used) + len(alias_used):]

        nsp = NumericStringParser()
        solved = str(nsp.eval(equation))

        await ctx.send(content=f"```{solved}```")
    
    @commands.command(
        name='choose',
        description='Makes a random choice',
        aliases=['choice', 'chooser']
    )
    async def choose(self, ctx):
        msg = ctx.message.content

        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        choice = random.choice(msg[len(prefix_used) + len(alias_used):].split())

        await ctx.send(content=f"I choose `{choice}`")

    @commands.command(
        name='shutdown',
        description='Shuts down the bot (Owner only)',
        aliases=['sd']
    )
    async def shutdown(self,ctx):
        if ctx.message.author.id == self.config.owners[0]: #replace OWNERID with your user id
            print("shutdown")
        try:
            await self.bot.logout()
        except:
            print("EnvironmentError")
            self.bot.clear()
        else:
            await ctx.send("You do not own this bot!")

def setup(bot):
    bot.add_cog(Utility(bot))
