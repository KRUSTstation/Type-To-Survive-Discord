import discord
from discord.ext import commands
from discord import app_commands

class BasicCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check latency")
    async def ping(self, interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! Latency: `{latency}ms` ", ephemeral=True)

async def setup(bot):   
    await bot.add_cog(BasicCmds(bot))