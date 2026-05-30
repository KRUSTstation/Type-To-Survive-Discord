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

        if channel.id in [PRIVATE_LOGGING_CHANNEL] or member == message.author.bot: return

        embed = discord.Embed(title='Message Sent')

        embed.add_field(name='Message', value=message.content)
        embed.add_field(name='Author', value=member.mention)
        embed.add_field(name='Channel sent', value=channel.mention)

        if channel.id in [LOGGING_CHANNEL]:
            await send_private_log(message.guild, embed)
        else:
            await send_log(message.guild, embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        member = message.author
        channel = message.channel

        if channel.id in [PRIVATE_LOGGING_CHANNEL]: return

        async for entry in message.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
            if entry.user == message.author.bot: return

            embed = discord.Embed(title='Message deleted')
            
            embed.add_field(name='Message', value=message.content)
            embed.add_field(name='Author', value=member.mention)
            embed.add_field(name='Deleted by', value=entry.user.mention)
            embed.add_field(name='Channel', value=channel.mention)

        if channel.id in [LOGGING_CHANNEL]:
            await send_private_log(message.guild, embed)
        else:
            await send_log(message.guild, embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        member = before.author
        channel = before.channel

        if channel.id in [PRIVATE_LOGGING_CHANNEL] or member == before.author.bot: return

        embed = discord.Embed(title='Message edited')
        
        embed.add_field(name='Before', value=before.content)
        embed.add_field(name='After', value=after.content)
        embed.add_field(name='Author', value=member.mention)
        embed.add_field(name='Channel', value=channel.mention)

        if channel.id in [LOGGING_CHANNEL]:
            await send_private_log(before.guild, embed)
        else:
            await send_log(before.guild, embed)

class PrivateLogging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    

async def setup(bot):   
    await bot.add_cog(Logging(bot))
    await bot.add_cog(PrivateLogging(bot))