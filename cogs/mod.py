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
    async def kick(self, ctx, user: discord.Member, *, reason: str = None):
        process(f"Kick Command Called by {ctx.message.author.name}")
        if user.guild_permissions.administrator:
            e = discord.Embed(description=":no_entry_sign: You cannot kick an administrator", colour=0xE74C3C)
            await ctx.send(embed=e)
        else:
            userName = str(user)
            #await ctx.guild.kick(user, reason=reason)
            e = discord.Embed(colour=0x2ECC71)
            e.set_author(
                name=f"{userName} has been kicked",
                icon_url=member.avatar_url
            )
            desc = ""
            desc += f"**Reason**: {reason}\n"
            desc += f"**Moderator:**{ctx.message.author.mention}"
            e.description = desc
            await ctx.send(embed=e)

                
    @kick.error
    async def kick_error(self, error, ctx):
        #if isinstance(error, MissingPermissions):
            await ctx.send(":no_entry_sign: I'm missing permissions to do that.\n Maybe user/role is higher than me?")
        #else:
        #    await ctx.send(":x: Something went wrong")

    

def setup(bot):
    bot.add_cog(Moderator(bot))