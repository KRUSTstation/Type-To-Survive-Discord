from .classes.bot import Bot    
from core.config import DISCORD_TOKEN as TOKEN

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN not set in environment (.env)")

bot = Bot()

async def main():
    async with bot:
        await bot.load_extension("discord_bot.cogs.BasicCmds")
        
        await bot.start(TOKEN)
        print("Online")