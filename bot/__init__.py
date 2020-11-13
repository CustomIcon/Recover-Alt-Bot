"""Client Initial."""
import pyromod.listen
import logging
from configparser import ConfigParser
from datetime import datetime

from bot.bot import bot

from os import environ

# Logging at the start to catch everything
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    handlers=[logging.StreamHandler()],
)
LOGS = logging.getLogger(__name__)

name = "bot"

# Read from config file
config_file = f"{name}.ini"
config = ConfigParser()
config.read(config_file)

API_ID = environ.get('API_ID', None) or config.get("pyrogram", "api_id")
API_HASH = environ.get('API_HASH', None) or config.get("pyrogram", "api_hash")

# Extra details
__version__ = "1.1"
__author__ = "pokurt"

# Global Variables
CMD_HELP = {}
client = None
START_TIME = datetime.now()

bot = bot(name)
