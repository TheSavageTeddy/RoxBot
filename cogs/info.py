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
            help_embed.add_field(name="Moderation", value="`?help moderation`")
            help_embed.add_field(name="Images", value="`?help image`")
            help_embed.add_field(name="Utility", value="`?help utility`")
            help_embed.add_field(name="Info", value="`?help info`")
            help_embed.add_field(name="Currency", value="`?help currency`")
            help_embed.add_field(name="Other", value="`?help other`")
        else:
            cogA = cog.lower()
            emojiCategory = {"Moderator":":tools:", "Image":":camera:", "Utility":":tools:","Info":":question:","Other":"", "Music":":musical_note:"}
            categoryAlias = {}
            
            cogs = [c for c in self.bot.cogs.keys()]

            lower_cogs = [c.lower() for c in cogs]
            
            all_commands  = {}
            for cog in cogs: all_commands[cog] = self.bot.get_cog(cogs[ lower_cogs.index(cog.lower()) ]).get_commands()
            
            for cog in all_commands:
                for c in all_commands[cog]:
                        pass#print(c)
            
            all_commandsData = [c for cog in all_commands for c in all_commands[cog]]
            all_commandsName = [c.name for cog in all_commands for c in all_commands[cog]]


            if cogA in lower_cogs:
                help_embed = discord.Embed(
                    title=f'{emojiCategory[cogA.title()]} {cogA.title()} Commands',
                    color=0x2ECC71
                )
                commands_list = self.bot.get_cog(cogs[ lower_cogs.index(cogA) ]).get_commands()
                help_text=''

                for command in commands_list:
                    help_text += f'`{command.name}` '
                help_embed.description = help_text

            elif cogA in all_commandsName:
                command = all_commandsData[all_commandsName.index(cogA)]
                help_embed = discord.Embed(
                    title=f'Information about ?{command.name}',
                    color=0x2ECC71
                )
                help_embed.add_field(name="**Description**\n", value=f"{command.description}\n", inline=False)
                help_embed.add_field(name="**Aliases**\n", value=f"`{' '.join(command.aliases)}`", inline=False)


            else:
                await ctx.send('Invalid command/category specified.')
                return

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
    
    @commands.command(
        name='invite',
        description='Gets the an invite link for the bot',
        aliases=['botinvite', 'addbot']
    )
    async def botinvite(self, ctx):
        invite_embed = discord.Embed(
            title='Invite me to your Server!',
            color=0x2ECC71
        )
        invite_embed.add_field(name="Full Permissions", value=f"{self.config.bot_invite}")
        invite_embed.add_field(name="Basic Permissions", value=f"{self.config.bot_invite_basic}")
        invite_embed.set_footer(text="Made with ❤️ by Roxiun")
        await ctx.send(embed=invite_embed)
    
    @commands.command(
        name='support',
        description='Gets the support server invite',
        aliases=['server', 'supportserver', 'helpserver', 'helpinvite', 'devserver']
    )
    async def serverinvite(self, ctx):
        invite_embed = discord.Embed(
            title='Here is the offical RoxBot Development and Support Server!',
            description=f"{self.config.server_invite}",
            color=0x2ECC71
        )
        invite_embed.set_footer(text="Made with ❤️ by Roxiun")
        await ctx.send(embed=invite_embed)
    
    @commands.command(
        name='source',
        description='Gets the source code link',
        aliases=['sourcecode']
    )
    async def sourceCode(self, ctx):
        source_embed = discord.Embed(
            title='Here is my Source Code!',
            description=f"https://github.com/Roxiun/RoxBot/",
            color=0x2ECC71
        )
        source_embed.set_footer(text="Made with ❤️ by Roxiun")
        await ctx.send(embed=source_embed)


def setup(bot):
    bot.add_cog(Info(bot))