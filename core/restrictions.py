import discord
from discord import app_commands

from core.config import OWNER_USERID

def owner_only():
    async def predicate(interaction: discord.Interaction):
        return check_owner(interaction.user.id)
    
    return app_commands.check(predicate)

def check_owner(id):
    return int(id) == OWNER_USERID