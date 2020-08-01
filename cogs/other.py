import os
import time
import math
import discord
import asyncio
import pickle
import json

import psutil
import concurrent.futures
import signal
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

    @commands.group(
        name='minecraftserver',
        description='Creates private minecraft servers',
        aliases=['mcserver', 'mcs', 'bw', 'smp', 'smp-tst', 'smptst', 'bedwars', 'tstsmp', 'tst-smp']
    )
    async def minecraftserver(self, ctx):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(
                title='Minecraft Command',
                description=f"Creates private minecraft servers",
                color=0x2ECC71
            )
            e.add_field(name="Usage", value=f"`?minecraftserver <start/stop> <server_type>`")
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
                ar1 = type_aliases[serverType]
                async_result = pool.apply_async(start_server, args=(ar1,))
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
                    Server_embed.set_footer(text="Hang with us it can take up to 3mins for the server to completly start | Made with ❤️ by Roxiun")
                    await msg.edit(
                        embed=Server_embed,
                        content=None
                    )
                    serverStartTime = time.time()
            
                    with open('db/minecraft_server.json') as json_file:
                        servers = json.load(json_file)
                    
                    servers["data"] = [{"user":ctx.message.author.id, "msgID":msg.id,"msgChannel":msg.channel.id,"createdAt":str(serverStartTime), "PID":pid_list}]
                    print(servers)
                    with open('db/minecraft_server.json', 'w') as outfile:
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
            os.system('''ps axf | grep ngrok | grep -v grep | awk '{print "kill -9 " $1}' | sh''')
            os.system('''ps axf | grep java | grep -v grep | awk '{print "kill -9 " $1}' | sh''')
            e = discord.Embed(description=":no_entry_sign: No Server found", colour=0xE74C3C)
            await ctx.send(embed=e)
            return
        elif psutil.pid_exists(servers["data"][0]["PID"]["Minecraft"]) or psutil.pid_exists(servers["data"][0]["PID"]["ngrok"]):
            if servers["data"][0]["user"] == ctx.message.author.id or ctx.message.author.id == 352308837794971648:
                # kill the processes
                '''
                p = psutil.Process(servers["data"][0]["PID"]["Minecraft"])
                p.terminate()
                p2 = psutil.Process(servers["data"][0]["PID"]["ngrok"])
                p2.terminate()
                '''
                try:
                    os.kill(servers["data"][0]["PID"]["Minecraft"], signal.SIGKILL)
                    os.kill(servers["data"][0]["PID"]["ngrok"], signal.SIGKILL)
                except:
                    print('Process killing failed')

                # edit the message
                channel = self.bot.get_channel(servers["data"][0]["msgChannel"])
                message = await channel.fetch_message(servers["data"][0]["msgID"])

                Server_embed = discord.Embed(
                    title='Private BedWars Minecraft Server',
                    color=0x2ECC71
                )
                Server_embed.add_field(name="Server IP", value=f"`Offline`")
                Server_embed.add_field(name="Server Info", value=f"Ram: 3GB\n CPU: i3-2100\n Max Players: 4")
                Server_embed.add_field(name="Time Remaining", value=f"`0:00:00`", inline=True)
                Server_embed.set_footer(text="Made with ❤️ by Roxiun")
                
                await message.edit(embed=Server_embed, content=None)

                # remove from db
                servers["data"] = []
                with open('db/minecraft_server.json', 'w+') as outfile:
                    json.dump(servers, outfile)
                
                # sends message
                e = discord.Embed(description=":white_check_mark: Server Ended!", colour=0x2ECC71)
                await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Other(bot))