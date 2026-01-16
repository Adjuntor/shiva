#Allows to import config.py from the directory above
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.config as config

#Discord lib
import discord
from discord.ext import commands

from io import BytesIO
import datetime

msg_log = config.MOD_MSG_LOG
msg_ignore = config.MOD_MSG_IGNORE
role_chng = config.MOD_ROLE_CHANGE
membr_join = config.MOD_MEMBER_JOIN
membr_leave = config.MOD_MEMBER_LEAVE

class Moderation(commands.Cog, name="Moderation"):
    """Moderation cog"""
    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation Cog initialized')

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            files = []
            for file in message.attachments:
                fp = BytesIO()
                await file.save(fp)
                files.append(discord.File(fp, filename=file.filename, spoiler=file.is_spoiler()))
            for x in range(len(msg_ignore)):
                if message.guild.id == msg_ignore[x][0]:
                    if message.channel.id == msg_ignore[x][1]:
                        return
            for x in range(len(msg_log)):
                if message.guild.id == msg_log[x][0]:
                    embed=discord.Embed(description=f"<@{message.author.id}>: {message.content}", timestamp=datetime.datetime.now(), color=discord.Colour.red())
                    embed.set_author(name=f"{message.author.name} - Deleted Message.", icon_url=message.author.avatar.url)
                    embed.add_field(name=f"Channel:", value=f"<#{message.channel.id}>")
                    await self.bot.get_channel(msg_log[x][1]).send(embed=embed,files=files)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.author.bot:
            if after.embeds:
                return
            for x in range(len(msg_ignore)):
                if before.guild.id == msg_ignore[x][0]:
                    if before.channel.id == msg_ignore[x][1]:
                        return
            for x in range(len(msg_log)):
                if before.guild.id == msg_log[x][0]:
                    embed=discord.Embed(description=f"<@{before.author.id}>: {before.content}", timestamp=datetime.datetime.now(), color=discord.Colour.orange())
                    embed.set_author(name=f"{before.author.name} - Edited Message.", icon_url=before.author.avatar.url)
                    embed.add_field(name=f"After:", value=f"{after.content}")
                    embed.add_field(name=f"Link:", value=f"[See Message](https://discordapp.com/channels/{after.guild.id}/{after.channel.id}/{after.id})")
                    embed.add_field(name=f"Channel:", value=f"<#{before.channel.id}>")
                    await self.bot.get_channel(msg_log[x][1]).send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if len(before.roles) < len(after.roles):
            for x in range(len(role_chng)):
                if after.guild.id == role_chng[x][0]:
                    newRole = next(role for role in after.roles if role not in before.roles)
                    embed=discord.Embed(description=f"<@{after.id}> had the {newRole} role applied.", timestamp=datetime.datetime.now(), color=discord.Colour.greyple())
                    embed.set_author(name=f"{after} - Role Changed.", icon_url=after.avatar.url)
                    await self.bot.get_channel(role_chng[x][1]).send(embed=embed)
        if len(before.roles) > len(after.roles):
            for x in range(len(role_chng)):
                if after.guild.id == role_chng[x][0]:
                    newRole = next(role for role in before.roles if role not in after.roles)
                    embed=discord.Embed(description=f"<@{after.id}> had the {newRole} role removed.", timestamp=datetime.datetime.now(), color=discord.Colour.greyple())
                    embed.set_author(name=f"{after} - Role Changed.", icon_url=after.avatar.url)
                    await self.bot.get_channel(role_chng[x][1]).send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        for x in range(len(role_chng)):
                if member.guild.id == membr_join[x][0]:
                    embed=discord.Embed(description=f"<@{member.id}>", timestamp=datetime.datetime.now(), color=discord.Colour.green())
                    embed.set_author(name=f"{member} - has joined.", icon_url=member.avatar.url)
                    await self.bot.get_channel(membr_join[x][1]).send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        for x in range(len(role_chng)):
                if member.guild.id == membr_leave[x][0]:
                    embed=discord.Embed(description=f"<@{member.id}>", timestamp=datetime.datetime.now(), color=discord.Colour.red())
                    embed.set_author(name=f"{member} - has left.", icon_url=member.avatar.url)
                    await self.bot.get_channel(membr_leave[x][1]).send(embed=embed)


async def setup(bot: commands.Bot):
  await bot.add_cog(Moderation(bot))

