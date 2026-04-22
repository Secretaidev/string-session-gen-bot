from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import pyromod
import config
from database import db
from utils import small_caps
import os

if not os.path.exists("plugins"):
    os.makedirs("plugins")

class StringGenBot(Client):
    def __init__(self):
        super().__init__(
            name="StringGenBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            plugins=dict(root="plugins"),
            workers=100
        )

    async def start(self):
        await super().start()
        print(small_caps("ʙᴏᴛ sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!"))

    async def stop(self, *args):
        await super().stop()
        print(small_caps("ʙᴏᴛ sᴛᴏᴘᴘᴇᴅ!"))

if __name__ == "__main__":
    StringGenBot().run()
