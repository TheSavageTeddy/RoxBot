import os
import sys
import time
import discord
import random
from utils.data import getJSON

from discord.ext import commands
from datetime import datetime

from utils.safe_math import NumericStringParser
from utils.cli_logging import *

import base64

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

    @commands.group(
        name='encode',
        description='Encodes the input',
        aliases=['encrypt']
    )
    async def encode(self, ctx):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(
                title='Encode Command',
                description=f"Encodes the given input",
                color=0x2ECC71
            )
            e.add_field(name="Usage", value=f"`?encode <encoding_type> <input>`")
            e.add_field(name="Avaliable encoding types", value=f"`base16 base32 base64 base85 hex binary url rot13 rot 47 `")
            e.set_footer(text="Made with ❤️ by Roxiun")
            await ctx.send(embed=e)

    @encode.command(name="base64", aliases=["b64"])
    async def encode_base64(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(colour=0x2ECC71)
    
        result = base64.urlsafe_b64encode(input.encode('UTF-8')).decode('utf-8')
        e.add_field(name="Input", value=f"{input}")
        e.add_field(name="Output", value=f"{result}")

        await ctx.send(e)

    @commands.command(
        name='shutdown',
        description='Shuts down the bot (Owner only)',
        aliases=['sd']
    )
    async def shutdown(self,ctx):
        if ctx.message.author.id == self.config.owners[0]: #replace OWNERID with your user id
            info("Shutdown")
            try:
                smsg = await ctx.send(content="Attemping to shutdown...")
                process("Pulling from git")
                os.system("git pull")
                await self.bot.logout()
            except:
                await smsg.edit(content=":x: An error occured")
                warning("EnvironmentError")
                self.bot.clear()
        else:
            await ctx.send("You do not own this bot!")
    
    @commands.command(
        name='restart',
        description='Restarts down the bot (Owner only)',
        aliases=[]
    )
    async def restart(self,ctx):
        if ctx.message.author.id == self.config.owners[0]: #replace OWNERID with your user id
            info("Restart")
            try:
                rmsg = await ctx.send(content="Attemping to restart...")
                process("Pulling from git")
                os.system("git pull")
                os.execv(sys.executable, ['python'] + sys.argv)
            except Exception as e:
                await smsg.edit(content=f":x: An error occured\n {e}")
                warning("Error")
        else:
            await ctx.send("You do not own this bot!")

    @commands.command(
        name='test',
        description='Testing command(Owner only)',
        aliases=[]
    )
    async def test(self,ctx):
        if ctx.message.author.id == self.config.owners[0]: #replace OWNERID with your user id
            try:
                rmsg = await ctx.send(content="<:github:734317758438965330> (Emoji test)")
            except Exception as e:
                await smsg.edit(content=f":x: An error occured\n {e}")
                warning("Error in testing command")
        else:
            await ctx.send("You do not have testing permissions!")

def setup(bot):
    bot.add_cog(Utility(bot))
