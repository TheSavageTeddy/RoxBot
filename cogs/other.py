import os
import time
import discord
from threading import Thread
from utils.data import getJSON

from utils.start_server import *

from discord.ext import commands
from datetime import datetime

class Other(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.config = getJSON("config.json")
    
    @commands.command(
        name='bedwars',
        description='Starts a private bedwars server',
        aliases=['bedwarsserver', 'bw', 'privategame', 'privatebedwars']
    )
    async def bedwars(self, ctx):
        Server_embed = discord.Embed(
            title='Starting Server...',
            color=0x2ECC71
        )
        Server_embed.add_field(name="Server IP", value=f"`Generating... 16 seconds`")
        Server_embed.add_field(name="Server Info", value=f"Ram: 3GB\n CPU: i3-2100\n Max Players: 4")
        Server_embed.set_footer(text="Made with ❤️ by Roxiun")
        msg = await ctx.send(embed=Server_embed)
        async with ctx.typing():
            Thread(target=start_server).start()
            for i in range(15,-1,-1):
                Server_embed = discord.Embed(
                    title='Starting Server...',
                    color=0x2ECC71
                )
                Server_embed.add_field(name="Server IP", value=f"`Generating... {i} seconds`")
                Server_embed.add_field(name="Server Info", value=f"Ram: 3GB\n CPU: i3-2100\n Max Players: 4")
                Server_embed.set_footer(text="Made with ❤️ by Roxiun")
                await msg.edit(
                    embed=Server_embed,
                    content=None
                )
                time.sleep(1)
            
            genServerIP = get_ip()
            Server_embed = discord.Embed(
                title='Private BedWars Minecraft Server',
                color=0x2ECC71
            )
            Server_embed.add_field(name="Server IP", value=f"`{genServerIP}`")
            Server_embed.add_field(name="Server Info", value=f"Ram: 3GB\n CPU: i3-2100\n Max Players: 4")
            Server_embed.set_footer(text="Made with ❤️ by Roxiun")
            await msg.edit(
                embed=Server_embed,
                content=None
            )
                

    

def setup(bot):
    bot.add_cog(Other(bot))