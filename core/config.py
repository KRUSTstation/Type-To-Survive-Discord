from dotenv import load_dotenv
import os

load_dotenv()

# Dev options
DEBUG = os.getenv('DEBUG') == '1'

# Discord
OWNER_USERID = 767714143146868756
RESTRICTED_CMDS = {'suggestion_setup', 'report_setup', 'say'}

MODERATOR_ROLEID = 1502960657069244507
MOD_CMDS = {'mute', 'kick'}

DISCORD_TOKEN = os.getenv('BOT_TOKEN')