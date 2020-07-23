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
    
    @commands.command(
        name='8ball',
        description='Ask the 8ball something!',
        aliases=['ball8', '8b', 'b8'],
    )
    async def math_command(self, ctx):
        msg = ctx.message.content

        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        responses = ["YES!", "yeah", "why not", "definetly", 
                    "idk", "maybe", "not sure", "don't ask me", "error: try again"
                    ,"NO", "bad idea", "nah", "why would you"]

        choice = random.choice(responses)

        await ctx.send(content=f"`{choice}`")
    
    @commands.command(
        name='topic',
        description='Chooses a random topic you can talk about!',
        aliases=['ask', 'topics','question','questions'],
    )
    async def math_command(self, ctx):
        msg = ctx.message.content

        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        topics = ["What is your hobby?", "Do you play any musical instruments?","What do you do in your free time?","What would you do if you suddenly got $10 000?", "Do you like school?","What school subject is your favourite?","Do you like this bot? :D", "How has your day been?","What do you use discord for?","Do you play any computer games?","How many topics do you think this bot has?","What do you do during holidays?","What countries have you visited?","What is your favourite food?","What is your favourite drink?","Do you have any pets?","How much sleep do you get?","What would you do if you got stranded on a desert island with food and water?", "Do you prefer pen or pencil?","Do you prefer typing on computer or writing it down on paper?", "Dogs or cats?", "How do you plan to spent the rest of your day?","What is your favourite animal?","What would you do if you won the lottery?","What would you do if unicorns existed?","Do you believe in flat earth?","Do you believe in global warming?","What do you think is the biggest problem in society?","What did you have for breakfast?","What is the most dangerous thing you have done?","What is the most fun thing you have done?","Hot or cold water?", "What is your favourite season?","What would you do if there was an earthquake?","Have you ever experienced a natural disaster?","Describe your perfect holiday","Describe your perfect house"]

        choice = random.choice(topics)

        await ctx.send(content=f"`{choice}`")

def setup(bot):
    bot.add_cog(Utility(bot))
