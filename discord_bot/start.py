import discord

import os
from dotenv import load_dotenv

from .classes.bot import Bot

# Cogs


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN not set in environment (.env)")

bot = Bot()

async def main():
    async with bot:
        await bot.load_extension("discord_bot.cogs.BasicCmds")
        
        await bot.start(TOKEN)
        print("Online")