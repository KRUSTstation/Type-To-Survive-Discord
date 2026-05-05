from dotenv import load_dotenv
import os

load_dotenv()

# Dev options
DEBUG = os.getenv('DEBUG') == '1'

# Discord
DISCORD_TOKEN = os.getenv('BOT_TOKEN')