import os
from dotenv import load_dotenv

if os.path.exists("vars.env"):
    load_dotenv("vars.env")

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/song_assistant")
UPDATES_CHANNEL = os.getenv("UPDATES_CHANNEL", "https://t.me/secretsbotz")
MUST_JOIN = os.getenv("MUST_JOIN", "secretsbotz")
LOGGER_ID = int(os.getenv("LOGGER_ID", str(OWNER_ID)))
