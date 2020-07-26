import os
import time
import discord
import asyncio
import pickle

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
        return time.time() - oldepoch >= 7200

    '''
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
        
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(start_server, ())
        for i in range(15,-1,-1):
            async with ctx.typing():
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
        async with ctx.typing():
            pid_list = async_result.get()
            self.pid_listClass = async_result.get()
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
                timeRemaining = 7200 - elapsedTime # time left in seconds
                
                Server_embed = discord.Embed(
                    title='Private BedWars Minecraft Server',
                    color=0x2ECC71
                )
                Server_embed.add_field(name="Server IP", value=f"`{genServerIP}`")
                Server_embed.add_field(name="Server Info", value=f"Ram: 3GB\n CPU: i3-2100\n Max Players: 4")
                Server_embed.add_field(name="Time Remaining", value=f"`{str(timedelta(seconds=timeRemaining))}`", inline=True)
                Server_embed.set_footer(text="Made with ❤️ by Roxiun")
                await msg.edit(
                    embed=Server_embed,
                    content=None
                )
                
    @commands.command(
        name='bedwarsstop',
        description='Stops the private bedwars server',
        aliases=['bedwarsserverstop', 'bwstop', 'privategamestop', 'privatebedwarsstop']
    )
    async def bedwarsstop(self, ctx):  
        if psutil.pid_exists(self.pid_listClass["Minecraft"]):
            p = psutil.Process(self.pid_listClass["Minecraft"])
            p.terminate()
            p2 = psutil.Process(self.pid_listClass["ngrok"])
            p2.terminate()
            await ctx.send("Server Stopped!")
        else:
            await ctx.send(":x: Couldnt find a running server")

    @commands.command(
        name='tstsmp',
        description='Starts a private TheSavageTeddy SMP',
        aliases=[]
    )
    async def tstSMP(self, ctx):
        Server_embed = discord.Embed(
            title='Starting Server...',
            color=0x2ECC71
        )
        Server_embed.add_field(name="Server IP", value=f"`Generating... 16 seconds`")
        Server_embed.add_field(name="Server Info", value=f"Ram: 3GB\n CPU: i3-2100\n Max Players: 4")
        Server_embed.set_footer(text="Made with ❤️ by Roxiun")
        msg = await ctx.send(embed=Server_embed)
        
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(start_server_smp, ())
        for i in range(15,-1,-1):
            async with ctx.typing():
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
        async with ctx.typing():
            pid_list = async_result.get()
            self.pid_listClass = async_result.get()
            genServerIP = get_ip()
            Server_embed = discord.Embed(
                title='Private TheSavageTeddy SMP Minecraft Server',
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
                    title='Private TheSavageTeddy SMP Minecraft Server',
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
                    title='Private TheSavageTeddy SMP Minecraft Server',
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
                timeRemaining = 7200 - elapsedTime # time left in seconds
                
                Server_embed = discord.Embed(
                    title='Private TheSavageTeddy SMP Minecraft Server',
                    color=0x2ECC71
                )
                Server_embed.add_field(name="Server IP", value=f"`{genServerIP}`")
                Server_embed.add_field(name="Server Info", value=f"Ram: 3GB\n CPU: i3-2100\n Max Players: 4")
                Server_embed.add_field(name="Time Remaining", value=f"`{str(timedelta(seconds=timeRemaining))}`", inline=True)
                Server_embed.set_footer(text="Made with ❤️ by Roxiun")
                await msg.edit(
                    embed=Server_embed,
                    content=None
                )
    '''
    #'''
    @commands.group(
        name='minecraftserver',
        description='Creates private minecraft servers',
        aliases=['mcserver', 'mcs']
    )
    async def minecraftserver(self, ctx):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(
                title='Minecraft Command',
                description=f"Creates private minecraft servers",
                color=0x2ECC71
            )
            e.add_field(name="Usage", value=f"`?minecraft <start/stop> <server_type>`")
            e.add_field(name="Avaliable server types", value=f"`bedwars smp-tst`")
            e.set_footer(text="Made with ❤️ by Roxiun")
            await ctx.send(embed=e)  

    
    @minecraftserver.command(
        name='start',
        description='Starts private minecraft servers',
        aliases=['turnon', 'on']
    )
    async def start_minecraft(self, ctx, serverType: str = None):
        if not serverType:
            e = discord.Embed(description=":no_entry_sign: You must specify a server type", colour=0xE74C3C)
            await ctx.send(embed=e)
            return
        
        type_aliases = {
            "bw":"bedwars",
            "bedwar":"bedwars",
            "bed":"bedwars",
            "bedwars":"bedwars",
            "survival-tst":"smp-tst",
            "survival-thesavageteddy":"smp-tst",
            "smp-thesavageteddy":"smp-tst",
            "survivalmultiplayer-thesavageteddy":"smp-tst",
            "survivalmultiplayer-tst":"smp-tst",
            "smp-tst":"smp-tst",
            "bw-beta":"bedwars-beta",
            "bedwar-beta":"bedwars-beta",
            "bed-beta":"bedwars-beta",
            "bedwars-beta":"bedwars-beta"
        }

        if any((serverType in i) for i in type_aliases.items()):
            Server_embed = discord.Embed(
                title='Starting Server...',
                color=0x2ECC71
            )
            Server_embed.add_field(name="Server IP", value=f"`Generating... 16 seconds`")
            Server_embed.add_field(name="Server Info", value=f"Ram: 3GB\n CPU: i3-2100\n Max Players: 4")
            Server_embed.set_footer(text="Made with ❤️ by Roxiun")
            msg = await ctx.send(embed=Server_embed)
        
            if not get_ip():
                pool = ThreadPool(processes=1)
                print(type_aliases[serverType])
                async_result = pool.apply_async(start_server, args=(type_aliases[serverType],))
                for i in range(15,-1,-1):
                    async with ctx.typing():
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
                        asyncio.sleep(1)
                async with ctx.typing():
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
            
                with open('db/minecraft_server.json') as json_file:
                    servers = json.load(json_file)
                servers["data"][0] = {"user":ctx.message.author.name, "msgID":msg.id,"msgChannel":msg.channel.id,"createdAt":str(serverStartTime), "PID":pid_list}

                with open('db/minecraft_server.json', 'w+') as outfile:
                    json.dump(servers, outfile)

            else:
                sip = get_ip()
                Server_embed = discord.Embed(
                    title='Existing Server Found',
                    desciption='Become a [donator](https://www.patreon.com/roxiun)\nfor completly private servers',
                    color=0x2ECC71
                )
                Server_embed.add_field(name="Server IP", value=f"`{sip}`")
                Server_embed.add_field(name="Server Info", value=f"Ram: 3GB\n CPU: i3-2100\n Max Players: 4")
                Server_embed.set_footer(text="Made with ❤️ by Roxiun")
                await msg.edit(
                    embed=Server_embed,
                    content=None
                )
                return
        else:
            e = discord.Embed(description=":no_entry_sign: That is not a valid server type", colour=0xE74C3C)
            e.set_footer(text="Use ?minecraftserver for a list of server types")
            await ctx.send(embed=e)
            return

    @minecraftserver.command(
        name='stop',
        description='Stops private minecraft servers',
        aliases=['turnoff', 'off']
    )
    async def stop_minecraft(self, ctx):
        with open('db/minecraft_server.json') as json_file:
            servers = json.load(json_file)
        if len(servers["data"]) == 0:
            if 

    #'''

def setup(bot):
    bot.add_cog(Other(bot))