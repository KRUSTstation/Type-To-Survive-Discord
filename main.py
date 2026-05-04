from discord_bot import start as start_discord

import asyncio

def __run_discord():
    asyncio.run(start_discord.main())

def main():
    __run_discord()

if __name__ == '__main__':
    main()