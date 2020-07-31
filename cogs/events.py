import os
import sys
import json
import math
import time
from os.path import getmtime
from utils.data import getJSON

import discord
from discord.ext import commands
from discord.ext.tasks import loop
from datetime import datetime
from datetime import timedelta

from utils.cli_logging import *

import psutil
import concurrent.futures
from multiprocessing.pool import ThreadPool
from threading import Thread
from utils.data import getJSON
from utils.start_server import *

class Events(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.config = getJSON("config.json")
        self.check_for_change.start()

    def hour_passed(self, oldepoch):
        return time.time() - oldepoch >= 7200

    @loop(seconds=60.0)
    async def check_for_change(self):
        # Check for Updates
        process("Checking for New Update")
        WATCHED_FILES = ["index.py", "cogs/easter.py", "cogs/events.py", "cogs/image.py", "cogs/info.py", "cogs/mod.py", "cogs/music.py", "cogs/other.py", "cogs/utility.py", "utils/cli_logging.py", "utils/data.py", "utils/safe_math.py", "utils/start_server.py", "utils/web_api.py"]
        WATCHED_FILES_MTIMES = [(f, getmtime(f)) for f in WATCHED_FILES]
        
        process("Pulling from git")
        os.system("git pull")

        changed = []
        for f, mtime in WATCHED_FILES_MTIMES:
            if getmtime(f) != mtime:
                changed.append(f)
                # One of the files has changed, so restart the script.
                info('Change Detected...')
                process('--> restarting')
                # When running the script via `./daemon.py` (e.g. Linux/Mac OS), use
                #os.execv(__file__, sys.argv)
                # When running the script via `python daemon.py` (e.g. Windows), use
                os.execv(sys.executable, ['python'] + sys.argv)
        if len(changed) == 0:
            info("No files changes")

        # Check Server Status
        with open('db/minecraft_server.json') as json_file:
            servers = json.load(json_file)
        if len(servers["data"]) == 0:
            os.system('''ps axf | grep ngrok | grep -v grep | awk '{print "kill -9 " $1}' | sh''')
        else:
            if self.hour_passed(float(servers["data"][0]["createdAt"])):
                # kill the processes
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
            else:
                # update the message with left time
                print("Attempting to edit message")
                start_time = servers["data"][0]["createdAt"]
                current_time = time.time()
                elapsed_time = math.ceil(current_time-start_time)

                time_remaining = 7200-elapsed_time
                time_remaining_formatted = str(timedelta(seconds=time_remaining))
                
                # edit the message
                channel = self.bot.get_channel(servers["data"][0]["msgChannel"])
                message = await channel.fetch_message(servers["data"][0]["msgID"])

                sip = get_ip()

                timeStarted = servers["data"][0]["createdAt"]

                Server_embed = discord.Embed(
                    title='Private BedWars Minecraft Server',
                    color=0x2ECC71
                )
                Server_embed.add_field(name="Server IP", value=f"`{sip}`")
                Server_embed.add_field(name="Server Info", value=f"Ram: 3GB\n CPU: i3-2100\n Max Players: 4")
                Server_embed.add_field(name="Time Remaining", value=f"`{time_remaining_formatted}`", inline=True)
                Server_embed.set_footer(text="Made with ❤️ by Roxiun")
                
                await message.edit(embed=Server_embed, content=None)
                

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if not self.config.join_message:
            return
        try:
            to_send = sorted([chan for chan in guild.channels if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
        except IndexError:
            pass
        info("Joined new guild")

    @check_for_change.before_loop
    async def before_check_for_change(self):
        process('Waiting for Bot start...')
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            print(f"{ctx.author} > {ctx.message.clean_content} ({ctx.guild.name})")
        except AttributeError:
            print(f"{ctx.author} > {ctx.message.clean_content} (Private Message)")

    @commands.Cog.listener()
    async def on_ready(self):
        
        if self.config.status_type == "idle":
            status_type = discord.Status.idle
        elif self.config.status_type == "dnd":
            status_type = discord.Status.dnd
        else:
            status_type = discord.Status.online
        
        if self.config.playing_type == "listening":
            playing_type = 2
        elif self.config.playing_type == "watching":
            playing_type = 3
        else:
            playing_type = 0

        await self.bot.change_presence(
            activity=discord.Activity(type=playing_type, name=self.config.playing),
            status=status_type
        )
        print(f"RoxBot is in {len(self.bot.guilds)} servers!")
        print(f"{75 - len(self.bot.guilds)} servers to go")

        with open('db/minecraft_server.json') as json_file:
            servers = json.load(json_file)
        if len(servers["data"]) == 0:
            os.system('''ps axf | grep ngrok | grep -v grep | awk '{print "kill -9 " $1}' | sh''')
        else:
            if self.hour_passed(float(servers["data"][0]["createdAt"])):
                # kill the processes
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
            else:
                # update the message with left time
                print("Attempting to edit message")
                start_time = float(servers["data"][0]["createdAt"])
                current_time = time.time()
                elapsed_time = math.ceil(current_time-start_time)

                time_remaining = 7200-elapsed_time
                time_remaining_formatted = str(timedelta(seconds=time_remaining))
                
                # edit the message
                channel = self.bot.get_channel(servers["data"][0]["msgChannel"])
                message = await channel.fetch_message(servers["data"][0]["msgID"])

                sip = get_ip()

                timeStarted = servers["data"][0]["createdAt"]

                Server_embed = discord.Embed(
                    title='Private BedWars Minecraft Server',
                    color=0x2ECC71
                )
                Server_embed.add_field(name="Server IP", value=f"`{sip}`")
                Server_embed.add_field(name="Server Info", value=f"Ram: 3GB\n CPU: i3-2100\n Max Players: 4")
                Server_embed.add_field(name="Time Remaining", value=f"`{time_remaining_formatted}`", inline=True)
                Server_embed.set_footer(text="Made with ❤️ by Roxiun")
                
                await message.edit(embed=Server_embed, content=None)
                
    
def setup(bot):
    bot.add_cog(Events(bot))