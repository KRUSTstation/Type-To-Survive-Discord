from discord_bot import start as start_discord

import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def __run_discord():
    try:
        asyncio.run(start_discord.main())
    except KeyboardInterrupt:
        pass

def main():
    __run_discord()

if __name__ == '__main__':
    main()