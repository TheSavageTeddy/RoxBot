import os
import time
import re
import urllib.request
import urllib.parse
from youtube_search import YoutubeSearch
import asyncio
import discord
import youtube_dl
from utils.data import getJSON

from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get

from dotenv import load_dotenv
from googleapiclient import discovery

from datetime import datetime

load_dotenv()

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')


    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        os.system(f"mv {filename} audio/{filename}")
        filename = f"audio/{filename}"
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.config = getJSON("config.json")
        self.players = {}

        self.api_key = os.getenv("api_key")
        self.youtube = discovery.build('youtube', 'v3', developerKey=self.api_key)
    
    def convert_YouTube_duration_to_seconds(self, duration):
        day_time = duration.split('T')
        day_duration = day_time[0].replace('P', '')
        day_list = day_duration.split('D')
        if len(day_list) == 2:
            day = int(day_list[0]) * 60 * 60 * 24
            day_list = day_list[1]
        else:
            day = 0
            day_list = day_list[0]
        hour_list = day_time[1].split('H')
        if len(hour_list) == 2:
            hour = int(hour_list[0]) * 60 * 60
            hour_list = hour_list[1]
        else:
            hour = 0
            hour_list = hour_list[0]
        minute_list = hour_list.split('M')
        if len(minute_list) == 2:
            minute = int(minute_list[0]) * 60
            minute_list = minute_list[1]
        else:
            minute = 0
            minute_list = minute_list[0]
        second_list = minute_list.split('S')
        if len(second_list) == 2:
            second = int(second_list[0])
        else:
            second = 0
        return day + hour + minute + second

    @commands.command(
        name='summon',
        description='Moves the bot to your current voice channel',
        aliases=['movevc', 'move']
    )
    async def summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        if not channel and not ctx.author.voice:
            await ctx.send(':x: You need to be in a voice channel or specify a channel')
            return

        destination = channel or ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        
        if voice and voice.is_connected():
            await voice.move_to(destination)
            await ctx.send(":white_check_mark: Sucessfuly moved to the channel")
        else:
            await destination.connect()
            await ctx.send(":white_check_mark: Sucessfuly joined the channel")
        
        while True:
            await asyncio.sleep(10)
            if len([member.id for member in destination.members]) == 1:
                await ctx.voice_client.disconnect()
                return

    @commands.command(
        name='play',
        description='Plays music from youtube',
        aliases=['youtubeplay', 'music']
    )
    async def yt(self, ctx, *, url='somereallygoodthingwhichnoonewouldsearch'):
        if url == "somereallygoodthingwhichnoonewouldsearch":
            await ctx.send(":x: You must specify a URL or name")
        elif "youtube.com" in url or "youtu.be" in url:
            destination = ctx.author.voice.channel
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

            await ctx.send('Now playing: {}'.format(player.title))
            while True:
                await asyncio.sleep(15)
                if len([member.id for member in destination.members]) == 1:
                    await ctx.voice_client.disconnect()
                    return
        else:
            destination = ctx.author.voice.channel
            def check(reaction, user):
                    return user == ctx.message.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌')
            try:
                async with ctx.typing():
                    req = self.youtube.search().list(q=str(url), part='snippet', type='video', maxResults=10, pageToken=None)
                    results  = req.execute()
                    # results = YoutubeSearch(str(url), max_results=10).to_dict()
            except:
                await ctx.send(":x: Couldnt find any videos from that query.")
                return
            channel = ctx.message.channel
            for i in range(9):
                async with ctx.typing():
                    videoid = results['items'][i]['id']['videoId']
                    req2 = self.youtube.videos().list(part='snippet,contentDetails', id=videoid)
                    res2 = req2.execute()
                    videoEmbed = discord.Embed(
                        title=f"{results['items'][i]['snippet']['title']}",
                        color=0x2ECC71
                    )
                    videoEmbed.set_thumbnail(url=results['items'][i]['snippet']["thumbnails"]["high"])
                    videoEmbed.add_field(name="**Description**\n", value=f"{results['items'][i]['snippet']['description']}\n", inline=False)
                    videoEmbed.add_field(name="**Info**\n", value=f"Result #{i+1}\n Duration: {str(convert_YouTube_duration_to_seconds(res2['contentDetails'][i]['duration']))}\n Views: {results[i]['views']}\n Channel Name: {results['items'][i]['snippet']['channelTitle']}", inline=False)
                    videoEmbed.set_footer(text=f"Made with ❤️ by Roxiun")
                    message = await ctx.send(embed=videoEmbed)
                    await message.add_reaction(chr(0x2705))
                    await message.add_reaction(chr(0x274C))
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        await channel.send(':x: Reaction timed out.')
                    else:
                        if str(reaction) == "✅":
                            musicURL = f"http://www.youtube.com/watch?v={results['items'][i]['id']['videoId']}"
                            print(musicURL)
                            break
                    
                    async with ctx.typing():
                        player = await YTDLSource.from_url(musicURL, loop=self.bot.loop)
                        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                    
                    await ctx.send('Now playing: {}'.format(player.title))
                    await asyncio.sleep(15)
                    if len([member.id for member in destination.members]) == 1:
                        await ctx.voice_client.disconnect()
                        return
                        
    @commands.command(
        name='stop',
        description='Stops music and disconnects the bot',
        aliases=['quit', 'stopmusic', 'endsong']
    )
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        await ctx.voice_client.disconnect()


    @yt.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send(":x: You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

def setup(bot):
    bot.add_cog(Music(bot))