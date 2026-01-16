#Allows to import config.py from the directory above
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.config as config

#Discord lib
import discord
from discord.ext import commands

class HClassesView(discord.ui.View):
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

    @discord.ui.button(label='HUnter', emoji="🟥", style=discord.ButtonStyle.gray, custom_id=f"hclasses_hunter")
    async def hunter(self, interaction: discord.Interaction, button: discord.ui.Button):
        await HClassesView.assign(self, interaction, button, 804580722072485898)
    @discord.ui.button(label='FIghter', emoji="🔴", style=discord.ButtonStyle.gray, custom_id=f"hclasses_fighter")
    async def fighter(self, interaction: discord.Interaction, button: discord.ui.Button):
        await HClassesView.assign(self, interaction, button, 804581444629823508)

    @discord.ui.button(label='RAnger', emoji="🟦", style=discord.ButtonStyle.gray, custom_id=f"hclasses_ranger")
    async def ranger(self, interaction: discord.Interaction, button: discord.ui.Button):
        await HClassesView.assign(self, interaction, button, 804581518314831882)
    @discord.ui.button(label='GUnner', emoji="🔵", style=discord.ButtonStyle.gray, custom_id=f"hclasses_gunner")
    async def gunner(self, interaction: discord.Interaction, button: discord.ui.Button):
        await HClassesView.assign(self, interaction, button,804581626847428609)

    @discord.ui.button(label='FOrce', emoji="🟨", style=discord.ButtonStyle.gray, custom_id=f"hclasses_force")
    async def force(self, interaction: discord.Interaction, button: discord.ui.Button):
        await HClassesView.assign(self, interaction, button, 804581708435423232)
    @discord.ui.button(label='TEchter', emoji="🟡", style=discord.ButtonStyle.gray, custom_id=f"hclasses_techter")
    async def techter(self, interaction: discord.Interaction, button: discord.ui.Button):
        await HClassesView.assign(self, interaction, button, 804581788885581824)

    @discord.ui.button(label='BRaver', emoji="🟩", style=discord.ButtonStyle.gray, custom_id=f"hclasses_braver")
    async def braver(self, interaction: discord.Interaction, button: discord.ui.Button):
        await HClassesView.assign(self, interaction, button, 804581853751148585)
    @discord.ui.button(label='BOuncer', emoji="🟢", style=discord.ButtonStyle.gray, custom_id=f"hclasses_bouncer")
    async def bouncer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await HClassesView.assign(self, interaction, button, 804581926622986250)

    @discord.ui.button(label='WAker', emoji="🟧", style=discord.ButtonStyle.gray, custom_id=f"hclasses_waker")
    async def waker(self, interaction: discord.Interaction, button: discord.ui.Button):
        await HClassesView.assign(self, interaction, button, 804581985301299201)

    @discord.ui.button(label='SLayer', emoji="❇️", style=discord.ButtonStyle.gray, custom_id=f"hclasses_slayer")
    async def slayer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await HClassesView.assign(self, interaction, button, 1095928651851243581)

class HClasses(commands.Cog, name="HClasses"):
    """Assign Classes Roles to people"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('HClasses Cog initialized')
        self.bot.add_view(HClassesView())

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def hclasses(self, ctx):
        await ctx.message.delete()
        await ctx.send("Choose your classes.", view=HClassesView())

async def setup(bot: commands.Bot):
    await bot.add_cog(HClasses(bot))

