import discord
from discord import app_commands

from core.config import OWNER_USERID, MODERATOR_ROLEID

def owner_only():
    async def predicate(interaction: discord.Interaction):
        return check_owner(interaction.user.id)
    
    return app_commands.check(predicate)

def check_owner(id):
    return int(id) == OWNER_USERID

def mod_only():
    async def predicate(interaction: discord.Interaction):
        return check_mod(interaction.user)
    
    return app_commands.check(predicate)
    
def check_mod(user: discord.Member):
    for role in user.roles:
        if role.id == MODERATOR_ROLEID:
            return True
        
    return False