#Allows to import config.py from the directory above
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.config as config

#Discord lib
import discord
from discord.ext import commands

#File manipulation Libs
from typing import Optional
from io import BytesIO

class Say(commands.Cog, name="Say"):
    """Make the bot say things"""
    @commands.Cog.listener()
    async def on_ready(self):
        print('Say Cog initialized')

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def say(self, ctx, channel: Optional[discord.TextChannel], *, text:str=""):
        await ctx.message.delete()
        files = []
        for file in ctx.message.attachments:
            fp = BytesIO()
            await file.save(fp)
            files.append(discord.File(fp, filename=file.filename, spoiler=file.is_spoiler()))
        if not channel:
            channel = ctx.channel
        if not text and not files:
           await ctx.send(f"`{config.PREFIX} say CHANNEL(optional) TEXT` CHANNEL name and TEXT to be send, if no channel name it sends to this one")
           return
        await channel.send(f"{text}", files=files)

async def setup(bot: commands.Bot):

  await bot.add_cog(Say(bot))
