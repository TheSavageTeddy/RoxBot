import os
import time
import math
import asyncio
import discord
from utils.data import getJSON


from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, BadArgument, check
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
        name='whois',
        description='Gets info about a user',
        aliases=['userinfo', 'user', 'user_info']
    )
    @commands.guild_only()
    async def whois(self, ctx, user: discord.Member = None):
        if not user:
            e = discord.Embed(description=":no_entry_sign: You must specify a user", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        show_roles = ', '.join(
            [f"<@&{x.id}>" for x in sorted(user.roles, key=lambda x: x.position, reverse=True) if x.id != ctx.guild.default_role.id]
        ) if len(user.roles) > 1 else 'None'

        userObject = self.bot.get_user(user.id)

        e = discord.Embed(title=f"{user}", colour=0x2ECC71)
    
        e.add_field(name="Discord Tag", value=f"{str(user)}")
        e.add_field(name="Nickname", value=user.nick if hasattr(user, "nick") else "None")
        e.add_field(name="User ID", value=user.id)
        e.add_field(name="Account Created", value=user.created_at.strftime("%d %B %Y, %H:%M"))
        e.add_field(name="Server Join Data", value=user.joined_at.strftime("%d %B %Y, %H:%M"))
        e.add_field(name="Is Bot?", value=str(userObject.bot))
        e.set_thumbnail(url=user.avatar_url)
        e.set_footer(text="Made with ❤️ by Roxiun")

        e.add_field(
            name="Roles",
            value=show_roles,
            inline=False
        )

        await ctx.send(embed=e)

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
            await ctx.guild.kick(user, reason=f"{reason}- {ctx.message.author.name}")
            e = discord.Embed(colour=0x2ECC71)
            e.set_author(
                name=f"{userName} has been kicked",
                icon_url=user.avatar_url
            )
            desc = ""
            desc += f"**Reason**: {reason}\n"
            desc += f"**Moderator:** {ctx.message.author.mention}"
            e.description = desc
            await ctx.send(embed=e)

    @commands.command(
        name='mute',
        description='Mutes a member in the server',
        aliases=['shutup','shut']
    )
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True)
    async def mute(self, ctx, user: discord.Member = None, *, reason: str = None):
        if not user:
            e = discord.Embed(description=":no_entry_sign: You must specify a user", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        process(f"Mute Command Called by {ctx.message.author.name}")
        
        userName = str(user)
        m = ctx.guild.get_member(user)
        muted_role = next((g for g in ctx.guild.roles if "muted" in g.name.lower() and not ("roles" in g.name.lower())), None)
        if not muted_role:
            e = discord.Embed(description=":no_entry_sign: You must have role with the word `Muted` in it", colour=0xE74C3C)
            await ctx.send(embed=e)
            return
        else:
            await user.add_roles(muted_role)
            e = discord.Embed(colour=0x2ECC71)
            e.set_author(
                name=f"{userName} has been muted",
                icon_url=user.avatar_url
            )
            desc = ""
            desc += f"**Reason**: {reason}\n"
            desc += f"**Moderator:** {ctx.message.author.mention}"
            e.description = desc
            await ctx.send(embed=e)

    @commands.command(
        name='unmute',
        description='Mutes a member in the server',
        aliases=[]
    )
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True)
    async def unmute(self, ctx, user: discord.Member = None, *, reason: str = None):
        if not user:
            e = discord.Embed(description=":no_entry_sign: You must specify a user", colour=0xE74C3C)
            await ctx.send(embed=e)
            return

        process(f"Mute Command Called by {ctx.message.author.name}")
        
        userName = str(user)
        m = ctx.guild.get_member(user)
        muted_role = next((g for g in ctx.guild.roles if "muted" in g.name.lower() and not ("roles" in g.name.lower())), None)
        if not muted_role:
            e = discord.Embed(description=":no_entry_sign: You must have role with the word `Muted` in it", colour=0xE74C3C)
            await ctx.send(embed=e)
            return
        else:
            await user.remove_roles(muted_role)
            e = discord.Embed(colour=0x2ECC71)
            e.set_author(
                name=f"{userName} has been unmuted",
                icon_url=user.avatar_url
            )
            desc = ""
            desc += f"**Reason**: {reason}\n"
            desc += f"**Moderator:** {ctx.message.author.mention}"
            e.description = desc
            await ctx.send(embed=e)

    @commands.command(
        name='tempmute',
        description='Temporarily mutes a member in the server',
        aliases=['tempshutup','tempshut', 'temporarilymute']
    )
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True)
    async def tempmute(self, ctx, user: discord.Member = None, timem: str = None, *, reason: str = None):
        if ctx.message.author.id == self.config.owners[0]:
            if not user:
                e = discord.Embed(description=":no_entry_sign: You must specify a user", colour=0xE74C3C)
                await ctx.send(embed=e)
                return
            elif not timem:
                e = discord.Embed(description=":no_entry_sign: You must specify a duration", colour=0xE74C3C)
                await ctx.send(embed=e)
                return

            abreviations = {
                "seconds":"seconds",
                "second":"seconds",
                "secs":"seconds",
                "sec":"seconds",
                "minutes":"minutes",
                "minute":"minutes",
                "mins":"minutes",
                "min":"minutes",
                "m":"minutes", 
                "s":"seconds"
            }

            if timem:
                try:
                    timem = float(timem)
                except:
                    await ctx.send("Not supported yet sorry!")
                    return

            process(f"Tempmute Command Called by {ctx.message.author.name}")
            
            userName = str(user)
            m = ctx.guild.get_member(user)
            muted_role = next((g for g in ctx.guild.roles if "muted" in g.name.lower() and not ("roles" in g.name.lower())), None)
            if not muted_role:
                e = discord.Embed(description=":no_entry_sign: You must have role with the word `Muted` in it", colour=0xE74C3C)
                await ctx.send(embed=e)
                return
            else:
                await user.add_roles(muted_role)
                mute_time = time.time()
                e = discord.Embed(colour=0x2ECC71)
                e.set_author(
                    name=f"{userName} has been muted",
                    icon_url=user.avatar_url
                )
                desc = ""
                desc += f"**Reason**: {reason}\n"
                desc += f"**Moderator:** {ctx.message.author.mention}"
                e.description = desc
                await ctx.send(embed=e)
                with open('db/mod.json') as json_file:
                    mod = json.load(json_file)
                old_mod_list = mod["data"]
                mod_list = mod["data"]
                mod_list.append({"time_muted":str(mute_time), "user":user.id, "length_muted":str(timem)})
                mod["data"] = mod_list
                with open('db/mod.json', 'w') as outfile:
                    json.dump(mod, outfile)
                
                if timem <= 120:
                    await asyncio.sleep(math.ceil(timem))
                    await user.remove_roles(muted_role)
                    with open('db/mod.json') as json_file:
                        mod = json.load(json_file)
                    mod["data"] = old_mod_list
                    with open('db/mod.json', 'w') as outfile:
                        json.dump(mod, outfile)




    @commands.command(
        name='ban',
        description='Bans a member from the server',
        aliases=['permban']
    )
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, user: discord.Member, *, reason: str = None):
        process(f"Ban Command Called by {ctx.message.author.name}")
        if user.guild_permissions.administrator:
            e = discord.Embed(description=":no_entry_sign: You cannot ban an administrator", colour=0xE74C3C)
            await ctx.send(embed=e)
        else:
            userName = str(user)
            m = ctx.guild.get_member(user)
            await ctx.guild.ban(user, reason=f"{reason} - {ctx.message.author.name}")
            e = discord.Embed(colour=0x2ECC71)
            e.set_author(
                name=f"{userName} has been banned",
                icon_url=user.avatar_url
            )
            desc = ""
            desc += f"**Reason**: {reason}\n"
            desc += f"**Moderator:** {ctx.message.author.mention}"
            e.description = desc
            await ctx.send(embed=e)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, discord.Forbidden):
            e = discord.Embed(description=":no_entry_sign: :no_entry_sign: I'm missing permissions to do that.\n Maybe user/role is higher than me?", colour=0xE74C3C)
            await ctx.send(embed=e)
        else:
            e = discord.Embed(description=":no_entry_sign: Something went wrong", colour=0xE74C3C)
            e.set_footer(text="Make Sure I have permissions to kick, and am higher than the specified member")
            await ctx.send(embed=e)
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, discord.Forbidden):
            e = discord.Embed(description=":no_entry_sign: :no_entry_sign: I'm missing permissions to do that.\n Maybe user/role is higher than me?", colour=0xE74C3C)
            await ctx.send(embed=e)
        else:
            e = discord.Embed(description=":no_entry_sign: Something went wrong", colour=0xE74C3C)
            e.set_footer(text="Make Sure I have permissions to ban, and am higher than the specified member")
            await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Moderator(bot))