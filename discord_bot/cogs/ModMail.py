import discord
from discord.ext import commands
from discord import app_commands

from core.restrictions import owner_only

class ModMail(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='suggestion_setup', description='Sets up the suggestion prompt')
    @owner_only()
    async def suggestion_setup(interaction: discord.Interaction):
        

async def setup(bot):   
    await bot.add_cog(ModMail(bot))