import discord
from discord import app_commands

from core.config import OWNER_USERID

def owner_only():
    async def predicate(interaction: discord.Interaction):
        return interaction.user.id == OWNER_USERID
    
    return app_commands.check(predicate)