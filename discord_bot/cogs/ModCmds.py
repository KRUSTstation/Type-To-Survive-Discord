import discord
from discord.ext import commands
from discord import app_commands

import datetime

from core.restrictions import mod_only

class ModCmds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # @app_commands.command(name='mute', description='Mutes the target user')
    # @mod_only()
    # async def mute(self, interaction: discord.Interaction, user: discord.Member, minutes: int):
    #     moderator = interaction.user

    #     if not interaction.guild: await interaction.response.send_message('This command can only be used in a server.', ephemeral=True); return

    #     if minutes <= 0: await interaction.response.send_message('Minutes must be greater than 0.', ephemeral=True); return

    #     if user.id == moderator.id: await interaction.response.send_message('You cannot mute yourself.', ephemeral=True); return

    #     if user.id == interaction.client.user.id: await interaction.response.send_message('You cannot mute me.', ephemeral=True); return

    #     if user.top_role >= moderator.top_role and interaction.guild.owner_id != moderator.id: await interaction.response.send_message('You cannot mute someone with an equal or higher role.', ephemeral=True); return

    #     # maybe can apply own mute system?
    #     duration = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)

    #     await user.timeout(duration, reason=f"Muted by {moderator}")
    #     await interaction.response.send_message(f'{user.mention} has been muted for {minutes} minutes.', ephemeral=True)

    # @app_commands.command(name='kick', description='Kick the target user')
    # @mod_only()
    # async def kick(self, interaction: discord.Interaction, user: discord.Member):
    #     moderator = interaction.user

    #     if not interaction.guild: await interaction.response.send_message('This command can only be used in a server.', ephemeral=True); return

    #     if user.id == moderator.id: await interaction.response.send_message('You cannot kick yourself.', ephemeral=True); return

    #     if user.id == interaction.client.user.id: await interaction.response.send_message('You cannot kick me.', ephemeral=True); return

    #     if user.top_role >= moderator.top_role and interaction.guild.owner_id != moderator.id: await interaction.response.send_message('You cannot kick someone with an equal or higher role.', ephemeral=True); return

    #     # maybe can apply own kick system?
    #     await user.kick(reason=f'Kicked by {moderator}')
    #     await interaction.response.send_message(f'{user.mention} has been kicked', ephemeral=True)

async def setup(bot):   
    await bot.add_cog(ModCmds(bot))