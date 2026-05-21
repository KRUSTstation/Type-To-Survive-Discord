import discord
from discord.ext import commands
from discord import app_commands

from core.restrictions import owner_only
from discord_bot.classes.modmail import suggestion

class ModMail(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='suggestion_setup', description='Sets up the suggestion prompt')
    @owner_only()
    async def suggestion_setup(self, interaction: discord.Interaction):
        channel = interaction.channel

        embed = discord.Embed(title='Make a suggestion', color=discord.Color.blurple())
        embed.add_field(name='Instructions', value=(
                        '1. _Press the `suggest` button_\n'
                        '2. _Enter your suggestion_\n'
                        '3. _You will get a dm when your suggestion is approved and will be put up on the thread_'
        ), inline=False)
        embed.add_field(name='What do I suggest?', value='_Any improvements/mechanics in the discord server or in game_', inline=False)

        await channel.send(embed=embed, view=suggestion.SuggestButton())
        await interaction.response.send_message("Done!", ephemeral=True)

async def setup(bot):   
    await bot.add_cog(ModMail(bot))