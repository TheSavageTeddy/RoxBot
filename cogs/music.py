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

from datetime import datetime

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
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
        print(filename)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.config = getJSON("config.json")
        self.players = {}
    
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

    @commands.command(
        name='play',
        description='Plays music from youtube',
        aliases=['youtubeplay', 'music']
    )
    async def yt(self, ctx, *, url='somereallygoodthingwhichnoonewouldsearch'):
        if url == "somereallygoodthingwhichnoonewouldsearch":
            await ctx.send(":x: You must specify a URL or name")
        elif "youtube.com" in url or "youtu.be" in url:
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

            await ctx.send('Now playing: {}'.format(player.title))
        else:
            def check(reaction, user):
                    return user == ctx.message.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌')
            try:
                async with ctx.typing():
                    results = YoutubeSearch(str(url), max_results=10).to_dict()
            except:
                pass
            if len(results) > 0:
                channel = ctx.message.channel
                for i in range(len(results)):
                    videoEmbed = discord.Embed(
                        title=f"{results[i]['title']}",
                        color=0x2ECC71
                    )
                    videoEmbed.set_thumbnail(url=results[i]["thumbnails"][3])
                    videoEmbed.add_field(name="**Description**\n", value=f"{results[i]['long_desc']}\n", inline=False)
                    videoEmbed.add_field(name="**Info**\n", value=f"Result #{i}\n Duration: {results[i]['duration']}\n Views: {results[i]['views']}", inline=False)
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
                            musicURL = f"http://www.youtube.com{results[i]['url_suffix']}"
                            print(musicURL)
                            break
                
                async with ctx.typing():
                    player = await YTDLSource.from_url(musicURL, loop=self.bot.loop, stream=True)
                    ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                
                await ctx.send('Now playing: {}'.format(player.title))
                    

    
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