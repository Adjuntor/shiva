#Allows to import config.py from the directory above
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.config as config

#Discord lib
import discord
from discord.ext import commands

class YesButton(discord.ui.View):
    def __init__(self, ctx, author, amount:int):
        super().__init__()
        self.ctx = ctx
        self.author = author
        self.amount = amount

    @discord.ui.button(label="Yes",style=discord.ButtonStyle.green)
    async def green_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.send_message(f"Deleted {self.amount} Messages", ephemeral=True)
        await interaction.message.delete()
        await self.ctx.channel.purge(limit=self.amount)
    
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
    
class Cleanup(commands.Cog, name="Cleanup"):
    """Remove messages from current channel"""
    @commands.Cog.listener()
    async def on_ready(self):
        print('Cleanup Cog initialized')

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def cleanup(self, ctx, amount:int):
        await ctx.message.delete()
        if amount <=0:
                await ctx.send("Has to be a number greater than 0.")
                return
        view = YesButton(ctx, ctx.author, amount)
        await ctx.send(f"Are you sure you want to delete **{amount}** messages?", view=view, delete_after=10)

    @cleanup.error
    async def on_command_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"`{config.PREFIX} cleanup AMOUNT` Number of messages to be deleted.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("You have to write a number.")

async def setup(bot: commands.Bot):

  await bot.add_cog(Cleanup(bot))
