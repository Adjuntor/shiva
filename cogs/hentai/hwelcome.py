#Allows to import config.py from the directory above
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.config as config

#Discord lib
import discord
from discord.ext import commands

class HWelcomeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def assign(self, interaction: discord.Interaction, button: discord.ui.Button, role):
        hrole = interaction.guild.get_role(role)
        try:
            assert isinstance(hrole, discord.Role)
        except AssertionError:
            await interaction.response.send_message(f"Role doesn't exist on this server.", ephemeral=True)
        if hrole in interaction.user.roles:
            await interaction.user.remove_roles(hrole)
            await interaction.response.send_message(f"Removed {hrole.name} role.", ephemeral=True)
        else:
            await interaction.user.add_roles(hrole)
            await interaction.response.send_message(f"Assigned {hrole.name} role.", ephemeral=True)

    @discord.ui.button(label='Friend', style=discord.ButtonStyle.blurple, custom_id=f"hwelcome_friend")
    async def friend(self, interaction: discord.Interaction, button: discord.ui.Button):
        await HWelcomeView.assign(self, interaction, button, 801020025154699264)
    
    @discord.ui.button(label='Member', style=discord.ButtonStyle.green, custom_id=f"hwelcome_member")
    async def member(self, interaction: discord.Interaction, button: discord.ui.Button):
        await HWelcomeView.assign(self, interaction, button, 800959291494236161)    
    
class HWelcome(commands.Cog, name="HWelcome"):
    """Assign Welcome Roles to people"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('HWelcome Cog initialized')
        self.bot.add_view(HWelcomeView())

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def hwelcome(self, ctx):
        await ctx.message.delete()
        await ctx.send("Choose if you are a friend or a member of the alliance.", view=HWelcomeView())

async def setup(bot: commands.Bot):

    await bot.add_cog(HWelcome(bot))
