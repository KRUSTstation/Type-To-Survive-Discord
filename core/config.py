from dotenv import load_dotenv
import os

load_dotenv()

# Dev options
DEBUG = os.getenv('DEBUG') == '1'

# Discord
OWNER_USERID = 767714143146868756
RESTRICTED_CMDS = {'suggestion_setup', 'report_setup'}
DISCORD_TOKEN = os.getenv('BOT_TOKEN')