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
        self.footerText = "Made with ❤️ by Roxiun, TheSavageTeddy & Imgflip"
    
    @commands.command(
        name='deadchat',
        description='Deadchat',
        aliases=['dead', 'chatdead']
    )
    async def deadchat(self, ctx):
        e = discord.Embed(colour=0x2ECC71)
        e.set_image(url="https://i.imgur.com/0WjrVUN.png")
        e.set_footer(self.footerText)

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
            return
        elif len(args) == 1 and args[0] == '':
            await ctx.send("You must specify some text dummy")
            return
        
        image = self.API_Handler.getImgflip("112126428", args)
        
        e = discord.Embed(colour=0x2ECC71)
        e.set_image(url=image)
        e.set_footer(self.footerText)

        await ctx.send(embed=e)
    
    @commands.command(
        name='drake',
        description='Drake Choice meme',
        aliases=['drakeposting', 'hotline', 'hotlinebling', 'drakehotlinebling']
    )
    async def drake(self, ctx):
        msg = ctx.message.content

        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        args = msg[len(prefix_used) + len(alias_used):].split(',')

        
        if len(args) > 2:
            await ctx.send(":x: Too many arguments (Max 2)")
            return
        elif len(args) == 1 and args[0] == '':
            await ctx.send("You must specify some text dummy")
            return
        
        image = self.API_Handler.getImgflip("181913649", args)
        
        e = discord.Embed(colour=0x2ECC71)
        e.set_image(url=image)
        e.set_footer(self.footerText)

        await ctx.send(embed=e)
    @commands.command(
        name='changemymind',
        description='Steven Crowder\'s sign, prove me wrong',
    )
    async def changemymind(self, ctx):
        msg = ctx.message.content

        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        args = msg[len(prefix_used) + len(alias_used):].split(',')

        
        if len(args) > 2:
            await ctx.send(":x: Too many arguments (Max 2)")
            return
        elif len(args) == 1 and args[0] == '':
            await ctx.send("You must specify some text dummy")
            return
        
        image = self.API_Handler.getImgflip("129242436", args)
        
        e = discord.Embed(colour=0x2ECC71)
        e.set_image(url=image)
        e.set_footer(self.footerText)

        await ctx.send(embed=e)
    
    @commands.command(
        name='expandingbrain',
        description='3 brain meme',
        aliases=['brains', 'bigbrain']
    )
    async def expandingbrain(self, ctx):
        msg = ctx.message.content

        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        args = msg[len(prefix_used) + len(alias_used):].split(',')

        
        if len(args) > 2:
            await ctx.send(":x: Too many arguments (Max 2)")
            return
        elif len(args) == 1 and args[0] == '':
            await ctx.send("You must specify some text dummy")
            return
        
        image = self.API_Handler.getImgflip("93895088", args)
        
        e = discord.Embed(colour=0x2ECC71)
        e.set_image(url=image)
        e.set_footer(self.footerText)

        await ctx.send(embed=e)
    
    @commands.command(
        name='carswerve',
        description='Car drifts off highway, sharp turn on road',
        aliases=['distractedcar', 'carexit']
    )
    async def carswerve(self, ctx):
        msg = ctx.message.content

        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        args = msg[len(prefix_used) + len(alias_used):].split(',')


        
        if len(args) > 3:
            await ctx.send(":x: Too many arguments (Max 3)")
            return
        elif len(args) == 1 and args[0] == '':
            await ctx.send("You must specify some text dummy")
            return
        
        image = self.API_Handler.getImgflip("124822590", args)
        
        e = discord.Embed(colour=0x2ECC71)
        e.set_image(url=image)
        e.set_footer(self.footerText)

        await ctx.send(embed=e)
    
    @commands.command(
        name='uno',
        description='Draw 25 cards or do something you dont like meme',
        aliases=['unodraw', 'drawcards', 'draw25']
    )
    async def uno(self, ctx):
        msg = ctx.message.content

        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        args = msg[len(prefix_used) + len(alias_used):].split(',')

        
        if len(args) > 3:
            await ctx.send(":x: Too many arguments (Max 2)")
            return
        elif len(args) == 1 and args[0] == '':
            await ctx.send("You must specify some text dummy")
            return

        image = self.API_Handler.getImgflip("93895088", args)
        
        e = discord.Embed(colour=0x2ECC71)
        e.set_image(url=image)
        e.set_footer(self.footerText)



def setup(bot):
    bot.add_cog(Image(bot))
