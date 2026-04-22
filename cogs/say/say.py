# Allows to import config.py from the directory above
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.config as config

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

class Sayslash(commands.Cog):
    """Make the bot say things with slash commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        print("Say Slash Cog initialized")

    @app_commands.command(name="say", description="Only my master can make me say things.")
    @app_commands.describe(channel="Channel to send the message in", text="Text for the bot to say", file="Attach a file to send with the message")
    @app_commands.guild_only()
    async def sayslash(self, interaction: discord.Interaction, text: Optional[str], channel: Optional[discord.TextChannel] = None, file: Optional[discord.Attachment] = None ):
        # Owner check (since @commands.is_owner doesn't work here)
        if interaction.user.id != self.bot.owner_id:
            await interaction.response.send_message("You are not allowed to use this command pathetic worm! Only my master can.", ephemeral=True)
            return

        if not channel:
            channel = interaction.channel

        files = []
        if file:
            files.append(await file.to_file())

        if not (text or files):
            await interaction.response.send_message(
                f"`You have to put something...`",
                ephemeral=True
            )
            return

        # Defer since sending to another channel can take time
        await interaction.response.defer(ephemeral=True)
        await channel.send(text, files=files)
        await interaction.followup.send("Message sent.", ephemeral=True)
    
    @commands.command(name="say")
    @commands.guild_only()
    @commands.is_owner()
    async def say(self, ctx, channel: Optional[discord.TextChannel], *, text:str=""):
        files = []
        for attachment in ctx.message.attachments:
            file = await attachment.to_file(spoiler=attachment.is_spoiler())
            files.append(file)
        if not channel:
            channel = ctx.channel
        if not (text or files):
           await ctx.send(f"`{config.PREFIX} say CHANNEL(optional) TEXT` CHANNEL name and TEXT to be send, if no channel name it sends to this one")
           return
        await ctx.message.delete()
        await channel.send(f"{text}", files=files)


async def setup(bot: commands.Bot):
    await bot.add_cog(Sayslash(bot))
