import discord
from discord.ext import commands

intents = discord.Intents.all()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)

    async def on_ready(self):
        print(f"Online as {self.user}")

    async def setup_hook(self):
        await self.tree.sync()bot