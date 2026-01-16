#Allows to import config.py from the directory above
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.config as config

#Discord lib
import discord
from discord.ext import commands

class Help(commands.Cog, name="Help"):
    """Help cog"""
    @commands.Cog.listener()
    async def on_ready(self):
        print('Help Cog initialized')

    def __init__(self, bot: commands.Bot):
        self.bot = bot
   
    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def help(self, ctx):
        return

async def setup(bot: commands.Bot):

  await bot.add_cog(Help(bot))
