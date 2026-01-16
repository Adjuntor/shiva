#Allows to import config.py from the directory above
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.config as config

#Discord lib
import discord
from discord.ext import commands

class ColorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def assign(self, interaction: discord.Interaction, button: discord.ui.Button, colorarray):
        color = None
        for x in range(len(colorarray)):
            if interaction.guild.id == colorarray[x][0]:
                color = interaction.guild.get_role(int(colorarray[x][1]))
        try:
            assert isinstance(color, discord.Role)
        except AssertionError:
            await interaction.response.send_message(f"Color/Role doesn't exist on this server.", ephemeral=True)
        if color in interaction.user.roles:
            await interaction.user.remove_roles(color)
            await interaction.response.send_message(f"Removed {color.name} color.", ephemeral=True)
        else:
            await interaction.user.add_roles(color)
            await interaction.response.send_message(f"Assigned {color.name} color.", ephemeral=True)

    @discord.ui.button(label='Red', emoji="🟥", style=discord.ButtonStyle.grey, custom_id=f"role_color_red")
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ColorView.assign(self, interaction, button, config.ROLE_COLOR_RED)
    
    @discord.ui.button(label='Greeen', emoji="🟩", style=discord.ButtonStyle.grey, custom_id=f"role_color_green")
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ColorView.assign(self, interaction, button, config.ROLE_COLOR_GREEN)    
        
    @discord.ui.button(label='Blue', emoji="🟦", style=discord.ButtonStyle.grey, custom_id=f"role_color_blue")
    async def blue(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ColorView.assign(self, interaction, button, config.ROLE_COLOR_BLUE)

    @discord.ui.button(label='Yellow', emoji="🟨", style=discord.ButtonStyle.grey, custom_id=f"role_color_yellow")
    async def yellow(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ColorView.assign(self, interaction, button, config.ROLE_COLOR_YELLOW)
    
    @discord.ui.button(label='Purple', emoji="🟪", style=discord.ButtonStyle.grey, custom_id=f"role_color_purple")
    async def purple(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ColorView.assign(self, interaction, button, config.ROLE_COLOR_PURPLE)
    
    @discord.ui.button(label='Brown', emoji="🟫", style=discord.ButtonStyle.grey, custom_id=f"role_color_brown")
    async def brown(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ColorView.assign(self, interaction, button, config.ROLE_COLOR_BROWN)
    
    @discord.ui.button(label='Orange', emoji="🟧", style=discord.ButtonStyle.grey, custom_id=f"role_color_orange")
    async def orange(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ColorView.assign(self, interaction, button, config.ROLE_COLOR_ORANGE)
    
    @discord.ui.button(label='Grey', emoji="⬛", style=discord.ButtonStyle.grey, custom_id=f"role_color_grey")
    async def grey(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ColorView.assign(self, interaction, button, config.ROLE_COLOR_GREY)

    @discord.ui.button(label='Cyan', emoji="🔵", style=discord.ButtonStyle.grey, custom_id=f"role_color_cyan")
    async def cyan(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ColorView.assign(self, interaction, button, config.ROLE_COLOR_CYAN)
    
    @discord.ui.button(label='Teal', emoji="🟢", style=discord.ButtonStyle.grey, custom_id=f"role_color_teal")
    async def teal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ColorView.assign(self, interaction, button, config.ROLE_COLOR_TEAL)
    
    @discord.ui.button(label='Pink', emoji="🔴", style=discord.ButtonStyle.grey, custom_id=f"role_color_pink")
    async def pink(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ColorView.assign(self, interaction, button, config.ROLE_COLOR_PINK)
    
class Color(commands.Cog, name="Color"):
    """Assign color to people"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Color Cog initialized')
        self.bot.add_view(ColorView())

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def color(self, ctx):
        await ctx.message.delete()
        await ctx.send("Choose a color for your name. Choose the same color to remove it.", view=ColorView())

async def setup(bot: commands.Bot):

    await bot.add_cog(Color(bot))
