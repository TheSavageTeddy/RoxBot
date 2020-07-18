import os
import time
import discord

import psutil
import concurrent.futures
from multiprocessing.pool import ThreadPool
from threading import Thread
from utils.data import getJSON

from utils.start_server import *

from discord.ext import commands
from datetime import datetime
from datetime import timedelta

class Other(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.config = getJSON("config.json")
    
    def hour_passed(self, oldepoch):
        return time.time() - oldepoch >= 60

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
            pool = ThreadPool(processes=1)
            async_result = pool.apply_async(start_server, ())
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
            pid_list = async_result.get()
            genServerIP = get_ip()
            Server_embed = discord.Embed(
                title='Private BedWars Minecraft Server',
                color=0x2ECC71
            )
            Server_embed.add_field(name="Server IP", value=f"`{genServerIP}`")
            Server_embed.add_field(name="Server Info", value=f"Ram: 3GB\n CPU: i3-2100\n Max Players: 4")
            Server_embed.add_field(name="Time Remaining", value=f"`2:00:00`", inline=True)
            Server_embed.set_footer(text="Made with ❤️ by Roxiun")
            await msg.edit(
                embed=Server_embed,
                content=None
            )
            serverStartTime = time.time()
            
            for i in range(120):
                await asyncio.sleep(60)
                if not psutil.pid_exists(pid_list["Minecraft"]):
                    Server_embed = discord.Embed(
                        title='Private BedWars Minecraft Server',
                        color=0x2ECC71
                    )
                    Server_embed.add_field(name="Server IP", value=f"`Offline`")
                    Server_embed.add_field(name="Server Info", value=f"Ram: 3GB\n CPU: i3-2100\n Max Players: 4")
                    Server_embed.add_field(name="Time Remaining", value=f"`0:00:00`", inline=True)
                    Server_embed.set_footer(text="Made with ❤️ by Roxiun")
                    await msg.edit(
                        embed=Server_embed,
                        content=None
                    )
                    return
                elif self.hour_passed(serverStartTime):
                    p = psutil.Process(pid_list["Minecraft"])
                    p.terminate()
                    p2 = psutil.Process(pid_list["ngrok"])
                    p2.terminate()
                    Server_embed = discord.Embed(
                        title='Private BedWars Minecraft Server',
                        color=0x2ECC71
                    )
                    Server_embed.add_field(name="Server IP", value=f"`Offline`")
                    Server_embed.add_field(name="Server Info", value=f"Ram: 3GB\n CPU: i3-2100\n Max Players: 4")
                    Server_embed.add_field(name="Time Remaining", value=f"`0:00:00`", inline=True)
                    Server_embed.set_footer(text="Made with ❤️ by Roxiun")
                    await msg.edit(
                        embed=Server_embed,
                        content=None
                    )
                    return
                else:
                    elapsedTime = i*60 # Time passed in seconds
                    timeRemaining = 60-elapsedTime #7200 - elapsedTime # time left in seconds
                    
                    Server_embed = discord.Embed(
                        title='Private BedWars Minecraft Server',
                        color=0x2ECC71
                    )
                    Server_embed.add_field(name="Server IP", value=f"`Offline`")
                    Server_embed.add_field(name="Server Info", value=f"Ram: 3GB\n CPU: i3-2100\n Max Players: 4")
                    Server_embed.add_field(name="Time Remaining", value=f"`{str(datetime.timedelta(seconds=timeRemaining))}`", inline=True)
                    Server_embed.set_footer(text="Made with ❤️ by Roxiun")
                    await msg.edit(
                        embed=Server_embed,
                        content=None
                    )
                
    @commands.command(
        name='test',
        description='test',
        aliases=[]
    )
    async def test(self, ctx):
        serverStartTime = time.time()

        for i in range(60):
            await asyncio.sleep(1)
            if self.hour_passed(serverStartTime):
                Server_embed = discord.Embed(
                    title='Private BedWars Minecraft Server',
                    color=0x2ECC71
                )
                Server_embed.add_field(name="Server IP", value=f"`Offline`")
                Server_embed.add_field(name="Server Info", value=f"Ram: 3GB\n CPU: i3-2100\n Max Players: 4")
                Server_embed.add_field(name="Time Remaining", value=f"`Ended`", inline=True)
                Server_embed.set_footer(text="Made with ❤️ by Roxiun")
                await msg.edit(
                    embed=Server_embed,
                    content=None
                )
                return
            else:
                elapsedTime = i*60 # Time passed in seconds
                timeRemaining = 60-elapsedTime #7200 - elapsedTime # time left in seconds
                
                Server_embed = discord.Embed(
                    title='Private BedWars Minecraft Server',
                    color=0x2ECC71
                )
                Server_embed.add_field(name="Server IP", value=f"`Offline`")
                Server_embed.add_field(name="Server Info", value=f"Ram: 3GB\n CPU: i3-2100\n Max Players: 4")
                Server_embed.add_field(name="Time Remaining", value=f"`{str(datetime.timedelta(seconds=timeRemaining))}`", inline=True)
                Server_embed.set_footer(text="Made with ❤️ by Roxiun")
                await msg.edit(
                    embed=Server_embed,
                    content=None
                )
                


def setup(bot):
    bot.add_cog(Other(bot))