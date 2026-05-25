import discord
from discord.ext import commands
from discord import app_commands

from random import choice

from core.config import RESTRICTED_CMDS, MOD_CMDS
from core.restrictions import check_owner, check_mod, mod_only

class BasicCmds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check latency")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! Latency: `{latency}ms` ", ephemeral=True)
    
    @app_commands.command(name='help', description="Need info on some commands?")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title='Help', color=discord.Color.red())

        for cmd in self.bot.tree.get_commands():
            if cmd.name in RESTRICTED_CMDS and not check_owner(interaction.user.id) or cmd.name in MOD_CMDS and check_mod(interaction.user):
                continue

            embed.add_field(name=f"`/{cmd.name}`", value=cmd.description or "No description", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name='sus', description="suspicious")
    async def sus(self, interaction: discord.Interaction):
        from core.cmds.sus_emoticons import emoticons

        await interaction.response.send_message(choice(emoticons))

    @app_commands.command(name='say', description="Repeat after me!!")
    @mod_only()
    async def say(self, interaction: discord.Interaction, string: str):
        if not string: await interaction.response.send_message('String cannot be empty', ephemeral=True); return

        await interaction.response.defer()

        channel = interaction.channel
        
        await channel.send(string)

async def setup(bot):   
    await bot.add_cog(BasicCmds(bot))