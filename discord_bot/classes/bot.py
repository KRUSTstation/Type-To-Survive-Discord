import discord
from discord.ext import commands

intents = discord.Intents.all()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents, help_command=None)

    async def on_ready(self):
        await self.change_presence(
            status=discord.Status.dnd,
            activity=discord.Game("Listening to /help")
        )

        print(f"Online as {self.user}")

    async def setup_hook(self):
        await self.tree.sync()