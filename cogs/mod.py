import os
import time
import discord
from utils.data import getJSON


from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, BadArgument
from discord.ext.tasks import loop
from datetime import datetime

from utils.cli_logging import *

# From: https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/mod.py
class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f"{argument} is not a valid member or member ID.") from None
        else:
            return m.id


class ActionReason(commands.Converter):
    async def convert(self, ctx, argument):
        ret = argument

        if len(ret) > 512:
            reason_max = 512 - len(ret) - len(argument)
            raise commands.BadArgument(f'reason is too long ({len(argument)}/{reason_max})')
        return ret

class Moderator(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.config = getJSON("config.json")
    
    @commands.command(
        name='kick',
        description='Kicks a member from the server',
        aliases=[]
    )
    @commands.guild_only()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user: discord.User, *, reason=None):
        process("Kick Command Called")
        if user.guild_permissions.administrator:
            await ctx.send(f":x: You cannot kick an admin from the server")
        else:
            userID = user.id
            userName = user.name
            await ctx.guild.kick(member, reason=reason)
            await ctx.send(f":white_check_mark: Sucessfully kicked {userName} (ID: {userID}) from the server.")

                
    @kick.error
    async def kick_error(self, error, ctx):
        #if isinstance(error, MissingPermissions):
        await ctx.send(f":x: An Error occured:\n {error}")
        #else:
        #    await ctx.send(":x: Something went wrong")

    

def setup(bot):
    bot.add_cog(Moderator(bot))