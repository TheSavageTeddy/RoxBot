import os
import discord
from utils.data import getJSON

from discord.ext import commands
from datetime import datetime

from utils.web_api import ImageAPI

class Image(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.config = getJSON("config.json")
        self.API_Handler = ImageAPI()
    
    @commands.command(
        name='deadchat',
        description='Deadchat',
        aliases=['dead', 'chatdead']
    )
    async def deadchat(self, ctx):
        e = discord.Embed(colour=0x2ECC71)
        e.set_image(url="https://i.imgur.com/0WjrVUN.png")
        e.set_footer(text="Made with ❤️ by Roxiun")

        await ctx.send(embed=e)

    @commands.command(
        name='distractedboyfriend',
        description='Distracted Boyfriend meme',
        aliases=['boyfriend', 'distractedbf', 'dbf']
    )
    async def distractedboyfriend(self, ctx):
        msg = ctx.message.content

        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        args = msg[len(prefix_used) + len(alias_used):].split(',')

        
        if len(args) > 3:
            await ctx.send(":x: Too many arguments (Max 3)")
        
        image = self.API_Handler.getImgflip("112126428", args)
        
        e = discord.Embed(colour=0x2ECC71)
        e.set_image(url=image)
        e.set_footer(text="Made with ❤️ by Roxiun & Imgflip")

        await ctx.send(embed=e)

# https://api.imgflip.com/caption_image?template_id=112126428&text0=abcd&text1=hadsh&username=roxiun&password=supergoodpassword

def setup(bot):
    bot.add_cog(Image(bot))