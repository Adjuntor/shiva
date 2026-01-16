#Allows to import config.py from the directory above
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.config as config

#Discord lib
import discord
from discord import app_commands
from discord.ext import commands

#Math lib
import simpleeval
simpleeval.MAX_STRING_LENGTH = 2000
simpleeval.MAX_POWER = 5000
simpleeval.MAX_SHIFT = 100

class Math(commands.Cog, name="Math"):
    """Solve math expressions"""
    @commands.Cog.listener()
    async def on_ready(self):
        print("Math Cog initialized")

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="math", description="Solve math expressions")
    @app_commands.describe(
        expression='Type the expression to be solved',
    )
    async def math(self, interaction: discord.Interaction, expression: str = None):
        if expression==None:
            embed=discord.Embed(title="2 plus 2 is 4 minus 1 that's 3, Quick Maths", url="https://youtu.be/3M_5oYU-IsU?t=63", description="Usage: `math <equation>`", color=config.EMBEDCOLOR)
            embed.add_field(name="Tips", value="""
            `+` Add things `math 2+2`-> 4
`-` Subtract things `math 4-1` -> 3
`/` Divide one thing by another `math 10/2` -> 5
`*` Multiply one thing by another `math 2*3` -> 6
`**` \"To the power of\" `math 2**3` -> 8
`%` Modulus.(remainder) `math 15 % 4` -> 3
`==` Equals `math 1 == 2` -> False
`<` Less than. `math 1 < 2` -> True
`>` Greater than. `math 1 > 2` -> False
`<=` Less than or Equal to `math 1 <= 2` -> True
`>=` Greater than or Equal to `math 1 >= 2` -> False
`in` Find if is "in" something `math "meseta" in "my storage"` -> False   
        """)
            await interaction.response.send_message(embed=embed)
        try:
            await interaction.response.send_message(f'Expression:```{expression}```\nResult:```{simpleeval.simple_eval(expression)}```')
        except Exception as error:
             return await interaction.response.send_message(f'Expression:```{expression}```\nResult:```{error}```')

async def setup(bot: commands.Bot):

    await bot.add_cog(Math(bot))
