import discord
from discord.ext import commands

import asyncio
from random import choice

from core.persist import PersistentView

TICKET_CATEGORY = 1507235813287792720
MODERATOR_ROLE = 1502960657069244507

async def is_ticket(interaction: discord.Interaction):
    channel = interaction.channel
    return channel.name.split('-')[0] == 'ticket'

async def close_ticket(interaction):
    if not await is_ticket(interaction):
        await interaction.response.send_message(content='This is not a ticket!', ephemeral=True)
        return
    
    await interaction.response.send_message(content='Are you sure? You will lose all data in this ticket.', view=Confirm(), ephemeral=True)

class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
    
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.success)
    async def confirm_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await is_ticket(interaction):
            await interaction.response.send_message(content='This is not a ticket!', ephemeral=True)
            return
        
        channel = interaction.channel
        cur_time = 3
        msg = await channel.send(content=f'Closing in {cur_time}')

        for i in range(cur_time-1, -1, -1):
            await asyncio.sleep(1)
            await msg.edit(content=f"Closing in {i}")
        
        await channel.delete()

class Close(PersistentView):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='Close', style=discord.ButtonStyle.danger, custom_id='close_button_persist')
    async def close_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await close_ticket(interaction)

class ReportButton(PersistentView):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='Open a Ticket 🎟️', style=discord.ButtonStyle.danger, custom_id='report_button_persist')
    async def report_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        guild = interaction.guild
        category = guild.get_channel(TICKET_CATEGORY)
        mod_role = guild.get_role(MODERATOR_ROLE)
        assigned_mod = choice([user for user in mod_role.members])
        while assigned_mod == user:
            assigned_mod = choice([user for user in mod_role.members])

        for channel in category.channels:
            if channel.name == f'ticket-{user.name}':
                await interaction.response.send_message(content='You already have an active ticket!', ephemeral=True)
                return

        channel = await guild.create_text_channel(f'ticket-{user.name}', category=category)
        await channel.set_permissions(user, read_messages=True, send_messages=True, attach_files=True, add_reactions=True)
        await interaction.response.send_message(content=f'I have made a channel for you at {channel.mention}', ephemeral=True)

        await channel.send(content=f'Hi {user.mention}, this is your ticket. {assigned_mod.mention} is the assigned mod for this ticket.', view=Close())