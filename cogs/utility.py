import os
import sys
import time
import discord
import random
import asyncio
from utils.data import getJSON

from discord.ext import commands
from datetime import datetime

from utils.safe_math import NumericStringParser
from utils.cli_logging import *

import base64
import codecs
from requests.utils import requote_uri

class Utility(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.config = getJSON("config.json")

        self.colors = {
            'DEFAULT': 0x000000,
            'WHITE': 0xFFFFFF,
            'AQUA': 0x1ABC9C,
            'GREEN': 0x2ECC71,
            'BLUE': 0x3498DB,
            'PURPLE': 0x9B59B6,
            'LUMINOUS VIVID PINK': 0xE91E63,
            'GOLD': 0xF1C40F,
            'ORANGE': 0xE67E22,
            'RED': 0xE74C3C,
            'GREY': 0x95A5A6,
            'NAVY': 0x34495E,
            'DARK AQUA': 0x11806A,
            'DARK GREEN': 0x1F8B4C,
            'DARK BLUE': 0x206694,
            'DARK PURPLE': 0x71368A,
            'DARK VIVID PINK': 0xAD1457,
            'DARK GOLD': 0xC27C0E,
            'DARK ORANGE': 0xA84300,
            'DARK RED': 0x992D22,
            'DARK GREY': 0x979C9F,
            'DARKER GREY': 0x7F8C8D,
            'LIGHT GREY': 0xBCC0C0,
            'DARK NAVY': 0x2C3E50,
            'BLURPLE': 0x7289DA,
            'GREYPLE': 0x99AAB5,
            'DARK BUT NOT BLACK': 0x2C2F33,
            'NOT QUITE BLACK': 0x23272A
        }
    
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
        choice = choice.replace("@", "")
        choice = choice.replace("`", "")

        await ctx.send(content=f"I choose `{choice}`")

    @commands.command(
        name='sendembed',
        description='Sends an embed in the selected channel',
        aliases=['send_embed', 'embed', 'botembed', 'bot_embed']
    )
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def send_embed(self, ctx, channel: discord.TextChannel = None):
        def echeck(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        if not channel:
            e = discord.Embed(description="What channel would you like send the embed in?", colour=0x2ECC71)
            await ctx.send(embed=e)

            try:
                msg = await self.bot.wait_for('message', timeout=60.0, check=echeck)
            except asyncio.TimeoutError:
                e = discord.Embed(description=":no_entry_sign: You did not reply in time!", colour=0xE74C3C)
                await ctx.send(embed=e)
                return
            else:
                try:
                    channelVar = int(str(msg.content).replace("<#", "").replace(">", ""))
                    print(msg.content)
                    print(channelVar)
                except:
                    try:
                        channelID = int(msg.content)
                    except:
                        e = discord.Embed(description=":no_entry_sign: Something went wrong with the channel you specified", colour=0xE74C3C)
                        await ctx.send(embed=e)
                        return
        else:
            try:
                channelID = channel.id
            except:
                e = discord.Embed(description=":no_entry_sign: Something went wrong with the channel you specified", colour=0xE74C3C)
                await ctx.send(embed=e)
                return
        
        channel_to_send = self.bot.get_channel(channelID)

        e = discord.Embed(description="What would you like the title to be?", colour=0x2ECC71)
        await ctx.send(embed=e)

        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=echeck)
        except asyncio.TimeoutError:
            e = discord.Embed(description=":no_entry_sign: You did not reply in time!", colour=0xE74C3C)
            await ctx.send(embed=e)
            return
        else:
            try:
                embedTitle = str(msg.content)
            except:
                e = discord.Embed(description=":no_entry_sign: Something went wrong with the channel you specified", colour=0xE74C3C)
                await ctx.send(embed=e)
                return

        e = discord.Embed(description="What would you like the description to be?", colour=0x2ECC71)
        await ctx.send(embed=e)

        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=echeck)
        except asyncio.TimeoutError:
            e = discord.Embed(description=":no_entry_sign: You did not reply in time!", colour=0xE74C3C)
            await ctx.send(embed=e)
            return
        else:
            try:
                embedDescription = str(msg.content)
            except:
                e = discord.Embed(description=":no_entry_sign: Something went wrong with the channel you specified", colour=0xE74C3C)
                await ctx.send(embed=e)
                return

        #color_list = [c.lower() for c in self.colors.values()]

        e = discord.Embed(description="What would you colour to be?", colour=0x2ECC71)
        e.set_footer(text="Send `None` for the default colour")
        await ctx.send(embed=e)

        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=echeck)
        except asyncio.TimeoutError:
            e = discord.Embed(description=":no_entry_sign: You did not reply in time!", colour=0xE74C3C)
            await ctx.send(embed=e)
            return
        else:
            userInput =  str(msg.content)
            if userInput.lower() == "none":
                embedColour = self.colors["DEFAULT"]
            else:
                try:
                    embedColour = self.colors[str(userInput).upper()]
                except KeyError:
                    e = discord.Embed(description=":no_entry_sign: Something went wrong with the channel you specified", colour=0xE74C3C)
                    await ctx.send(embed=e)
                    return

        embed = discord.Embed(
            title=embedTitle,
            description=embedDescription,
            color=embedColour
        )

        embed.set_footer(text=f"Sent by {ctx.message.author.name}")

        await channel_to_send.send(embed=embed)

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
            e.add_field(name="Avaliable encoding types", value=f"`base16 base32 base64 base85 hex binary url rot13 rot47 `")
            e.set_footer(text="Made with ❤️ by Roxiun")
            await ctx.send(embed=e)

    @encode.command(name="base64", aliases=["b64"])
    async def encode_base64(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(title="Result", colour=0x2ECC71)
    
        result = base64.b64encode(input.encode('UTF-8')).decode('utf-8')
        e.add_field(name="Input", value=f"`{input}`")
        e.add_field(name="Output", value=f"`{result}`")
        e.set_footer(text="Made with ❤️ by Roxiun")

        await ctx.send(embed=e)
    
    @encode.command(name="base32", aliases=["b32"])
    async def encode_base32(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(title="Result", colour=0x2ECC71)
    
        result = base64.b32encode(input.encode('UTF-8')).decode('utf-8')
        e.add_field(name="Input", value=f"`{input}`")
        e.add_field(name="Output", value=f"`{result}`")
        e.set_footer(text="Made with ❤️ by Roxiun")

        await ctx.send(embed=e)
    
    @encode.command(name="base16", aliases=["b16"])
    async def encode_base16(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(title="Result", colour=0x2ECC71)
    
        result = base64.b16encode(input.encode('UTF-8')).decode('utf-8')
        e.add_field(name="Input", value=f"`{input}`")
        e.add_field(name="Output", value=f"`{result}`")
        e.set_footer(text="Made with ❤️ by Roxiun")

        await ctx.send(embed=e)
    
    @encode.command(name="base85", aliases=["b85"])
    async def encode_base85(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(title="Result", colour=0x2ECC71)
    
        result = base64.b85encode(input.encode('UTF-8')).decode('utf-8')
        e.add_field(name="Input", value=f"`{input}`")
        e.add_field(name="Output", value=f"`{result}`")
        e.set_footer(text="Made with ❤️ by Roxiun")

        await ctx.send(embed=e)

    @encode.command(name="hex", aliases=[])
    async def encode_hex(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(title="Result", colour=0x2ECC71)
    
        result = (input.encode('UTF-8').hex()).decode('utf-8')
        e.add_field(name="Input", value=f"`{input}`")
        e.add_field(name="Output", value=f"`{result}`")
        e.set_footer(text="Made with ❤️ by Roxiun")

        await ctx.send(embed=e)  
    
    @encode.command(name="url", aliases=[])
    async def encode_url(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(title="Result", colour=0x2ECC71)
    
        result = requote_uri(str(input))
        e.add_field(name="Input", value=f"`{input}`")
        e.add_field(name="Output", value=f"`{result}`")
        e.set_footer(text="Made with ❤️ by Roxiun")

        await ctx.send(embed=e)  
    
    @encode.command(name="rot13", aliases=['r13'])
    async def encode_rot13(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(title="Result", colour=0x2ECC71)
    
        result = codecs.encode(str(input), "rot-13")
        e.add_field(name="Input", value=f"`{input}`")
        e.add_field(name="Output", value=f"`{result}`")
        e.set_footer(text="Made with ❤️ by Roxiun")

        await ctx.send(embed=e)  
    
    #https://github.com/VoxelPixel
    @encode.command(name="rot47", aliases=['r47'])
    async def encode_rot47(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(title="Result", colour=0x2ECC71)
    
        message = str(input)
        key = 47
        encryp_text = ""

        for i in range(len(message)):
            temp = ord(message[i]) + key
            if ord(message[i]) == 32:
                encryp_text += " "
            elif temp > 126:
                temp -= 94
                encryp_text += chr(temp)
            else:
                encryp_text += chr(temp)
            
        result = encryp_text

        e.add_field(name="Input", value=f"`{input}`")
        e.add_field(name="Output", value=f"`{result}`")
        e.set_footer(text="Made with ❤️ by Roxiun")

        await ctx.send(embed=e) 

    @commands.group(
        name='decode',
        description='Decode the input',
        aliases=['decrypt']
    )
    async def decode(self, ctx):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(
                title='Decode Command',
                description=f"Decodes the given input",
                color=0x2ECC71
            )
            e.add_field(name="Usage", value=f"`?decode <decoding_type> <input>`")
            e.add_field(name="Avaliable decoding types", value=f"`base16 base32 base64 base85 hex binary url rot13 rot47 `")
            e.set_footer(text="Made with ❤️ by Roxiun")
            await ctx.send(embed=e)   

    @commands.command(name="prune", aliases=[])
    async def prune(self, ctx, user: discord.Member = None):
        if not user:
            e = discord.Embed(description=":no_entry_sign: Comming Soon", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(description=":no_entry_sign: Comming Soon", colour=0xE74C3C)
        e.set_footer(text="Made with ❤️ by Roxiun")

        await ctx.send(embed=e)  

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
