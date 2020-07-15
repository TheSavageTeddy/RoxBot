import os
import time
import discord
from utils.data import getJSON

from discord.ext import commands
from datetime import datetime

class Info(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.config = getJSON("config.json")
    
    @commands.command(
        name='help',
        description='The help command',
        aliases=['commands', 'command'],
        usage='cog'
    )
    async def help_command(self, ctx, cog='all'):
        ''' Replaces Default Command'''

        if cog == 'all':
            help_embed = discord.Embed(
                title='RoxBot Commands',
                color=0x2ECC71
            )
            help_embed.add_field(name="Moderator", value="`?help mod`")
            help_embed.add_field(name="Images", value="`?help image`")
            help_embed.add_field(name="Utility", value="`?help util`")
            help_embed.add_field(name="Info", value="`?help info`")
            help_embed.add_field(name="Other", value="`?help other`")
        else:
            emojiCategory = {"Moderator":":tools:", "Image":":camera:", "Utility":":tools:","Info":":question:","Other":""}
            categoryAlias = {}
            
            cogs = [c for c in self.bot.cogs.keys()]

            lower_cogs = [c.lower() for c in cogs]

            if cog.lower() in lower_cogs:
                help_embed = discord.Embed(
                    title=f'{emojiCategory[cog.title()]} {cog.title()} Commands',
                    color=0x2ECC71
                )
                commands_list = self.bot.get_cog(cogs[ lower_cogs.index(cog.lower()) ]).get_commands()
                help_text=''

                for command in commands_list:
                    help_text += f'`{command.name}` '
                help_embed.description = help_text
            
            else:
                await ctx.send('Invalid category specified.')
                return

            '''
            if cog == 'mod' or cog =='moderator':
                help_embed = discord.Embed(
                    title=':tools: Moderator Commands',
                    color=0x2ECC71
                )
                hcommands = [
                    ""
                ]
                help_embed.description = f"`{'` `'.join(hcommands.sort())}`"
            
            elif cog == 'image' or cog =='img':
                help_embed = discord.Embed(
                    title=':camera: Image Commands',
                    color=0x2ECC71
                )
                hcommands = [
                    "deadchat",
                    "distractedboyfriend"
                ]
                help_embed.description = f"`{'` `'.join(hcommands.sort())}`"
            
            elif cog == 'utils' or cog =='util' or cog =='utility' or cog =='utilities':
                help_embed = discord.Embed(
                    title=':tools: Utility Commands',
                    color=0x2ECC71
                )
                hcommands = [
                    "choose",
                    "math"
                ]
                help_embed.description = f"`{'` `'.join(hcommands.sort())}`"
            '''

        await ctx.send(embed=help_embed)
    
    @commands.command(
        name='ping',
        description='Gets the response time of the bot',
        aliases=['lag', 'responsetime']
    )
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        message = await ctx.send("🏓 Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")

def setup(bot):
    bot.add_cog(Info(bot))