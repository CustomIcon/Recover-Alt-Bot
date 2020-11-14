from os import environ
from configparser import ConfigParser
from pyrogram import Client


API_ID = environ.get("API_ID", None)
API_HASH = environ.get("API_HASH", None)
SESSION = environ.get("SESSION", None)


class bot(Client):
    def __init__(self, name):
        """Custom Pyrogram Client."""
        name = name.lower()
        config_file = f"{name}.ini"
        config = ConfigParser()
        config.read(config_file)
        plugins = dict(
            root=f"{name}.plugins",
        )
        super().__init__(
            SESSION or config.get('pyrogram', 'string'),
            api_id=API_ID,
            api_hash=API_HASH,
            config_file=config_file,
            workers=16,
            plugins=plugins,
            workdir="./",
            app_version="bot v1.1",
        )

    async def start(self):
        await super().start()
        print("Bot started. Hi.")
    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")
