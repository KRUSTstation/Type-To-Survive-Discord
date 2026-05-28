import discord
from discord.ext import commands
import datetime

from core.persist import PersistentView
from core.config import MODERATOR_ROLEID, SUGGESTION_COOLDOWN
from .report import Confirm

SUGGESTION_ADMIN_CHANNEL = 1506858865915068477
SUGGESTION_FORUM = 1506883312063348797

_suggestion_cooldowns = {}

async def is_suggestion(interaction: discord.Interaction):
    if not isinstance(interaction.channel, discord.Thread) or not interaction.channel.parent.id == SUGGESTION_FORUM:
        return False
    
    if int(interaction.channel.name.split(' ')[-1].strip('<>@')) == interaction.user.id:
        return True
    
    for role in interaction.user.roles:
        if role.id == MODERATOR_ROLEID:
            return True 
        
    return False

async def close_suggestion(interaction: discord.Interaction):
    if not await is_suggestion(interaction):
        await interaction.response.send_message(content='This is not part of the suggestion forum', ephemeral=True)
        return
    
    await interaction.response.send_message(content='Are you sure? You will lose all data in this thread.', view=Confirm(), ephemeral=True)

class SuggestButton(PersistentView):
    def __init__(self): 
        super().__init__()

    @discord.ui.button(label='Suggest', style=discord.ButtonStyle.blurple, custom_id='suggest_button_persistent')
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _suggestion_cooldowns.get(interaction.user.name) and _suggestion_cooldowns[interaction.user.name] >= datetime.datetime.now():
            await interaction.response.send_message(f'You cannot make a suggestion for another {int((_suggestion_cooldowns[interaction.user.name] - datetime.datetime.now()).total_seconds() // 60)} minutes', ephemeral=True)
            return

        await interaction.response.send_modal(SuggestModal())

class ApproveButton(PersistentView):
    def __init__(self): 
        super().__init__()

    async def get_embed_info(self, interaction: discord.Interaction):
        message = interaction.message
        embed = message.embeds[0]
        author = next(f.value for f in embed.fields if f.name == 'Author')
        title = next(f.value for f in embed.fields if f.name == 'Title')
        description = next(f.value for f in embed.fields if f.name == 'Description')
        return author, title, description

    @discord.ui.button(label='Approve', style=discord.ButtonStyle.success, custom_id='approve_button_persistent')
    async def approve_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        author, title, description = await self.get_embed_info(interaction)

        for child in self.children:
            child.disabled = True

        forum = interaction.guild.get_channel(SUGGESTION_FORUM)

        thread = await forum.create_thread(
            name=f'{title.replace('`', '')} by {author}',
            content=f'{author}:\n{description.replace('`', '')}'
        )

        await thread.message.add_reaction('⭐')
        # await thread.message.add_reaction('') # maybe downvote ovver here

        user_id = int(author.replace("<@", "").replace("!", "").replace(">", ""))
        user = await interaction.client.fetch_user(user_id)

        await user.send(f'Your suggestion of title {title} has been put up on the forum')

        await interaction.edit_original_response(view=self)
        await interaction.followup.send((
            f'Suggestion by {author} has been put up by {interaction.user.mention}\n'
            f'Title: {title}'
        ))
    
    @discord.ui.button(label='Discard', style=discord.ButtonStyle.blurple, custom_id='discard_button_persistent')
    async def discard_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        author, title, description = await self.get_embed_info(interaction)

        for child in self.children:
            child.disabled = True

        user_id = int(author.replace("<@", "").replace("!", "").replace(">", ""))
        user = await interaction.client.fetch_user(user_id)

        await user.send(f'Your suggestion of title {title} has been discarded')

        await interaction.edit_original_response(view=self)

        await interaction.followup.send((
            f'Suggestion by {author} has been discarded by {interaction.user.mention}\n'
            f'Title: {title}'
        ))

class SuggestModal(discord.ui.Modal, title="Suggestion"):
    suggest_title = discord.ui.TextInput(
        label="Your title here",
        style=discord.TextStyle.short,
        placeholder="Type title here...",
        required=True,
        max_length=100
    )

    description = discord.ui.TextInput(
        label="Your description here",
        style=discord.TextStyle.paragraph,
        placeholder="Type description here... Make it as descriptive as possible so people understand what you want",
        required=True,
        max_length=4000
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title='Suggestion')
        embed.add_field(name='Author', value=interaction.user.mention, inline=False)
        embed.add_field(name='Title', value=f'`{self.suggest_title.value}`')
        embed.add_field(name='Description', value=f'```{self.description.value}```', inline=False)

        channel = interaction.client.get_channel(SUGGESTION_ADMIN_CHANNEL)

        await channel.send(embed=embed, view=ApproveButton())

        _suggestion_cooldowns[interaction.user.name] = datetime.datetime.now() + datetime.timedelta(minutes=SUGGESTION_COOLDOWN)

        await interaction.response.send_message((
        f'Thanks for your suggestion!\n'
        f'Title: `{self.suggest_title.value}`\n'
        f'Description: ```{self.description.value}```\n'
        f'Author: {interaction.user.mention}'
        ), ephemeral=True)