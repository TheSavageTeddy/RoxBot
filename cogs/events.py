import os
import discord
from utils.data import getJSON

from discord.ext import commands
from datetime import datetime

class Events(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.config = getJSON("config.json")
    
    @tasks.loop(seconds=10)
    async def check_for_change(self):
        info("Checking for New Update")
        WATCHED_FILES = ["index.py", "cogs/easter.py", "cogs/events.py", "cogs/image.py", "cogs/info.py", "cogs/mod.py", "cogs/music.py", "cogs/other.py", "cogs/utility.py", "utils/cli_logging.py", "utils/data.py", "utils/safe_math.py", "utils/start_server.py", "utils/web_api.py", 'test.txt']
        WATCHED_FILES_MTIMES = [(f, getmtime(f)) for f in WATCHED_FILES]
        
        process("Pulling from git")
        os.system("git pull")

        for f, mtime in WATCHED_FILES_MTIMES:
            if getmtime(f) != mtime:
                # One of the files has changed, so restart the script.
                info('Change Detected...')
                process('--> restarting')
                # When running the script via `./daemon.py` (e.g. Linux/Mac OS), use
                #os.execv(__file__, sys.argv)
                # When running the script via `python daemon.py` (e.g. Windows), use
                os.execv(sys.executable, ['python'] + sys.argv)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if not self.config.join_message:
            return
        try:
            to_send = sorted([chan for chan in guild.channels if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
        except IndexError:
            pass
        else:
            await to_send.send(self.config.join_message)

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

    
def setup(bot):
    bot.add_cog(Events(bot))