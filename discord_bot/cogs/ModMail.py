import discord
from discord.ext import commands
from discord import app_commands

from core.restrictions import owner_only
from discord_bot.classes.modmail import suggestion, report

class ModMail(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='close', description='Depending on the channel, this will close it. (eg. tickets/suggestion threads)')
    async def close(self, interaction: discord.Interaction):
        if await report.is_ticket(interaction): # ticket
            await report.close_ticket(interaction)
        elif await suggestion.is_suggestion(interaction): # suggestion
            await suggestion.close_suggestion(interaction)
        else:
            await interaction.response.send_message('This is not a valid channel to close', ephemeral=True)

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

    @app_commands.command(name='report_setup', description='Sets up the reporting prompt')
    @owner_only()
    async def report_setup(self, interaction: discord.Interaction):
        channel = interaction.channel

        embed = discord.Embed(title='Make a ticket', color=discord.Color.blurple())
        embed.add_field(name='Instructions', value=(
                        '1. _Press the button_\n'
                        '2. _A ticket will open for you_\n'
                        '3. _Interact with the assigned moderator and explain your reason for opening a ticket_'
        ), inline=False)

        embed.add_field(name='Why open a ticket?', value='_Report any abuse admins/users and bugs/unintended features in either the discord server or game_\nFeel free to either open a ticket or ping a mod if you need any other help.', inline=False)
        await channel.send(embed=embed, view=report.ReportButton())
        await interaction.response.send_message("Done!", ephemeral=True)

async def setup(bot):   
    await bot.add_cog(ModMail(bot))