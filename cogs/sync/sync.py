#Allows to import config.py from the directory above
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.config as config

#Discord lib
import discord
from discord.ext import commands

class Sync(commands.Cog, name="Sync"):
    """Sync slash commands"""
    @commands.Cog.listener()
    async def on_ready(self):
        print('Sync Cog initialized')

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx, guilds: commands.Greedy[discord.Object], spec: int):
        if not guilds:
            await ctx.message.delete()
            if spec == "1":
                await ctx.send("Executing global sync")
                synced = await ctx.bot.tree.sync()          
            elif spec == "2":
                await ctx.send("Sync current guild")
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "3":
                await ctx.send("Copying global commands to current guild")
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "4":
                await ctx.send("Clearing all commands from current guild")
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                await ctx.send("The typed number is not an option.")
            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return
        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1
        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
    
    @sync.error
    async def on_command_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
                embed=discord.Embed(title="Sync slash commands",description="""`"""+config.PREFIX+"""sync 1` Global Sync
    `"""+config.PREFIX+"""sync 2` Sync current guild
    `"""+config.PREFIX+"""sync 3` copies all global app commands to current guild and syncs
    `"""+config.PREFIX+"""sync 4` clears all commands from the current guild target and syncs (removes guild commands)
    `"""+config.PREFIX+"""sync id_1 id_2`  syncs guilds with id 1 and 2
            """,color=config.EMBEDCOLOR)
                await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("You have to type a number.")

async def setup(bot: commands.Bot):

  await bot.add_cog(Sync(bot))
