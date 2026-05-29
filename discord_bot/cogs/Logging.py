import discord
from discord.ext import commands
from discord import app_commands

from core.restrictions import owner_only
from core.config import LOGGING_CHANNEL, PRIVATE_LOGGING_CHANNEL

def get_logging_channel(guild: discord.Guild):
    return guild.get_channel(LOGGING_CHANNEL)

def get_private_logging_channel(guild: discord.Guild):
    return guild.get_channel(LOGGING_CHANNEL)

async def send_log(guild: discord.Guild, embed: discord.Embed):
    channel = get_logging_channel(guild)
    if channel:
        await channel.send(embed=embed)

async def send_private_log(guild: discord.Guild, embed: discord.Embed):
    channel = get_private_logging_channel(guild)
    if channel:
        await channel.send(embed=embed)

class Logging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        member = message.author
        channel = message.channel

        if channel.id in [LOGGING_CHANNEL, PRIVATE_LOGGING_CHANNEL]: return

        embed = discord.Embed(title='Message Sent')

        embed.add_field(name='Author', value=member.mention)
        embed.add_field(name='Channel sent', value=channel.mention)
        embed.add_field(name='Message', value=message.content)

        await send_log(message.guild, embed)

class PrivateLogging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    

async def setup(bot):   
    await bot.add_cog(Logging(bot))
    await bot.add_cog(PrivateLogging(bot))