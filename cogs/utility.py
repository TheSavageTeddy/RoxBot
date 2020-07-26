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
import binascii
from requests.utils import requote_uri
from urllib.parse import unquote

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
    
    def decode_binary_string(self, s):
        return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

    @commands.command(
        name='math',
        description='Evaluates the maths equations',
        aliases=['maths', 'calc', 'calculat', 'add', 'addition', 'multiply', 'calculate','eval','evaluate'],
    )
    async def math_command(self, ctx):
        msg = ctx.message.content

        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        equation = msg[len(prefix_used) + len(alias_used):]

        nsp = NumericStringParser()
        solved = str(nsp.eval(equation))
        
        text = f'''```js\n{solved}```'''

        await ctx.send(content=text)
    
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
                    channelID = int((((str(msg.content)).replace("<", "")).replace("#", "")).replace(">", ""))
                    print(msg.content)
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

        if not channel_to_send:
            e = discord.Embed(description=":no_entry_sign: That channel does not exists", colour=0xE74C3C)
            e.set_footer(text="(Or I don't have permissions to view it)")
            await ctx.send(embed=e)
            return


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
                    e = discord.Embed(description=":no_entry_sign: Something went wrong with the colour you specified", colour=0xE74C3C)
                    await ctx.send(embed=e)
                    return

        embed = discord.Embed(
            title=embedTitle,
            description=embedDescription,
            color=embedColour
        )

        embed.set_footer(text=f"Sent by {ctx.message.author.name}")

        await channel_to_send.send(embed=embed)

    @commands.command(
        name='editembed',
        description='Edits the embed in the selected channel',
        aliases=['edit_embed', 'embededit', 'embed_edit', 'edit']
    )
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def edit_embed(self, ctx, channel: discord.TextChannel = None, message: int = None):
        def echeck(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        if not channel or not message:
            if not channel:
                e = discord.Embed(description="What channel is the embed in?", colour=0x2ECC71)
                await ctx.send(embed=e)

                try:
                    msg = await self.bot.wait_for('message', timeout=60.0, check=echeck)
                except asyncio.TimeoutError:
                    e = discord.Embed(description=":no_entry_sign: You did not reply in time!", colour=0xE74C3C)
                    await ctx.send(embed=e)
                    return
                else:
                    try:
                        channelID = int((((str(msg.content)).replace("<", "")).replace("#", "")).replace(">", ""))
                        print(msg.content)
                    except:
                        try:
                            channelID = int(msg.content)
                        except:
                            e = discord.Embed(description=":no_entry_sign: Something went wrong with the channel you specified", colour=0xE74C3C)
                            await ctx.send(embed=e)
                            return                
            if not message:
                e = discord.Embed(description="What is the embed message id?", colour=0x2ECC71)
                await ctx.send(embed=e)
                
                try:
                    msg = await self.bot.wait_for('message', timeout=60.0, check=echeck)
                except asyncio.TimeoutError:
                    e = discord.Embed(description=":no_entry_sign: You did not reply in time!", colour=0xE74C3C)
                    await ctx.send(embed=e)
                    return
                else:
                    try:
                        messageID = int(msg)
                    except:
                        e = discord.Embed(description=":no_entry_sign: Invalid Message ID", colour=0xE74C3C)
                        await ctx.send(embed=e)
                        return

        
            channel = self.bot.get_channel(channelID)
            message = await channel.fetch_message(messageID)
        
        else:
            channel = self.bot.get_channel(channel.id)
            message = await channel.fetch_message(message)

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
                    e = discord.Embed(description=":no_entry_sign: Something went wrong with the colour you specified", colour=0xE74C3C)
                    await ctx.send(embed=e)
                    return

        embed = discord.Embed(
            title=embedTitle,
            description=embedDescription,
            color=embedColour
        )

        embed.set_footer(text=f"Sent by {ctx.message.author.name}")

        await message.edit(embed=embed, content=None)


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
    
        result = (input.encode('UTF-8').hex())#.decode('utf-8')
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

    @encode.command(name="binary", aliases=['bin'])
    async def encode_binary(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(title="Result", colour=0x2ECC71)
    
        result = ''.join(format(ord(c), '08b') for c in str(input))
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

    @decode.command(name="base64", aliases=["b64"])
    async def decode_base64(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(title="Result", colour=0x2ECC71)
    
        result = base64.b64decode(input.encode('UTF-8')).decode('utf-8')
        e.add_field(name="Input", value=f"`{input}`")
        e.add_field(name="Output", value=f"`{result}`")
        e.set_footer(text="Made with ❤️ by Roxiun")

        await ctx.send(embed=e)
    
    @decode.command(name="base16", aliases=["b16"])
    async def decode_base16(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(title="Result", colour=0x2ECC71)
    
        result = base64.b16decode(input.encode('UTF-8')).decode('utf-8')
        e.add_field(name="Input", value=f"`{input}`")
        e.add_field(name="Output", value=f"`{result}`")
        e.set_footer(text="Made with ❤️ by Roxiun")

        await ctx.send(embed=e)
    
    @decode.command(name="base32", aliases=["b32"])
    async def decode_base32(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(title="Result", colour=0x2ECC71)
    
        result = base64.b32decode(input.encode('UTF-8')).decode('utf-8')
        e.add_field(name="Input", value=f"`{input}`")
        e.add_field(name="Output", value=f"`{result}`")
        e.set_footer(text="Made with ❤️ by Roxiun")

        await ctx.send(embed=e)
    
    @decode.command(name="base85", aliases=["b85"])
    async def decode_base85(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(title="Result", colour=0x2ECC71)
    
        result = base64.b85decode(input.encode('UTF-8')).decode('utf-8')
        e.add_field(name="Input", value=f"`{input}`")
        e.add_field(name="Output", value=f"`{result}`")
        e.set_footer(text="Made with ❤️ by Roxiun")

        await ctx.send(embed=e)
    
    @decode.command(name="rot13", aliases=['r13'])
    async def decode_rot13(self, ctx, *, input: commands.clean_content = None):
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
    
    @decode.command(name="hex", aliases=[])
    async def decode_hex(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(title="Result", colour=0x2ECC71)
    
        result = (binascii.unhexlify(input.encode('UTF-8'))).decode('utf-8')
        e.add_field(name="Input", value=f"`{input}`")
        e.add_field(name="Output", value=f"`{result}`")
        e.set_footer(text="Made with ❤️ by Roxiun")

        await ctx.send(embed=e)  

    @decode.command(name="url", aliases=[])
    async def decode_url(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(title="Result", colour=0x2ECC71)
    
        result = unquote(str(input))
        e.add_field(name="Input", value=f"`{input}`")
        e.add_field(name="Output", value=f"`{result}`")
        e.set_footer(text="Made with ❤️ by Roxiun")

        await ctx.send(embed=e)

    @decode.command(name="rot47", aliases=['r47'])
    async def decode_rot47(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(title="Result", colour=0x2ECC71)
    
        message = str(input)
        key = 47
        decryp_text = ""

        for i in range(len(message)):
            temp = ord(message[i]) - key
            if ord(message[i]) == 32:
                decryp_text += " "
            elif temp < 32:
                temp += 94
                decryp_text += chr(temp)
            else:
                decryp_text += chr(temp)
            
        result = decryp_text

        e.add_field(name="Input", value=f"`{input}`")
        e.add_field(name="Output", value=f"`{result}`")
        e.set_footer(text="Made with ❤️ by Roxiun")

        await ctx.send(embed=e) 

    @decode.command(name="binary", aliases=['bin'])
    async def decode_binary(self, ctx, *, input: commands.clean_content = None):
        if not input:
            e = discord.Embed(description=":no_entry_sign: You must give an input string", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        e = discord.Embed(title="Result", colour=0x2ECC71)
    
        result = self.decode_binary_string(str(input).replace(" ", ""))
        e.add_field(name="Input", value=f"`{input}`")
        e.add_field(name="Output", value=f"`{result}`")
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
        aliases=['sd','poweroff']
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

    @commands.command(
        name='avatar',
        description='Gets the profile picture of user',
        aliases=['pfp', 'profilepicture']
    )
    async def avatar(self, ctx, member: discord.Member = None):
        if not member:
            e = discord.Embed(description=":no_entry_sign: You must specify a user", colour=0xE74C3C)
            await ctx.send(embed=e)
            return
        
        e = discord.Embed(title=f"{str(member)}", colour=0x2ECC71)
        e.set_image(url=member.avatar_url)

        await ctx.send(embed=e)



    @commands.command(
        name='8ball',
        description='Ask the 8ball something!',
        aliases=['eightball','8b']
    )
    async def eight_ball(self,ctx):
        responses = ["YES!", "yeah", "why not", "definetly", 
            "idk", "maybe", "not sure", "don't ask me", "error: try again"
            ,"NO", "bad idea", "nah", "why would you"]
        choice = random.choice(responses)
        e = discord.Embed(description=f"{choice}", colour=0x2ECC71)
        await ctx.send(embed=e)


    @commands.command(
        name='coinflip',
        description='Flip a coin! Has chance to land on heads or tails. Or even b24gaXRzIHNpZGUh',
        aliases=['cf', 'coin_flip','coin','flipacoin','flipcoin','flip_coin']
    )
    async def coinflip(self,ctx):
        coinflip = ["The coin landed on `heads!`","The coin landed on `tails!`"]
        if int(random.randint(0,100)) == int(69):
            result="THE COIN LANDED ON ITS SIDE OMG WTF?!?!?!"
        else:
            result = random.choice(coinflip)
        e = discord.Embed(description=f"{result}", colour=0x2ECC71)
        await ctx.send(embed=e)



    @commands.command(
        name='dice',
        description='Roll a die/dice with numbers 1-6 on them!',
        aliases=['rolldie', 'rolldice']
    )
    async def dice(self,ctx):
        outcomes = [
'''
```js
 __________
|          |
|          |
|     •    |
|          |
|__________|


''',
'''
```js
 __________
|          |
|       •  |
|          |
|  •       |
|__________|


''',
'''
```js
 __________
|          |
|        • |
|     •    |
|  •       |
|__________|


''',
'''
```js
 __________
|          |
|  •    •  |
|          |
|  •    •  |
|__________|


''',
'''
```js
 __________
|          |
|  •    •  |
|     •    |
|  •    •  |
|__________|


''',
'''
```js
 __________
|          |
|  •    •  |
|  •    •  |
|  •    •  |
|__________|


'''
]

        result=random.choice(outcomes)
        e = discord.Embed(description=f"{result}\n\n```", colour=0x2ECC71)
        e.set_footer(text="Made with ❤️ by Roxiun & TheSavageTeddy!")
        msg = await ctx.send(embed=e)

        for i in range(7):
            await asyncio.sleep(0.1)
            result=random.choice(outcomes)
            e = discord.Embed(description=f"{result}\n\n```", colour=0x2ECC71)
            e.set_footer(text="Made with ❤️ by Roxiun & TheSavageTeddy!")
            await msg.edit(
                embed=e,
                content=None
            )
        
        
        result=random.choice(outcomes)
        n = outcomes.index(result)
        e = discord.Embed(description=f"{result}\nYou rolled a {n}!\n```", colour=0x2ECC71)
        e.set_footer(text="Made with ❤️ by Roxiun & TheSavageTeddy!")

        await msg.edit(
            embed=e,
            content=None
        )

def setup(bot):
    bot.add_cog(Utility(bot))
