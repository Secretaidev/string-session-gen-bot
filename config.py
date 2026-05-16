import os
from dotenv import load_dotenv

if os.path.exists("vars.env"):
    load_dotenv("vars.env")

# Telegram Desktop API defaults (used when custom keys are not provided)
DEFAULT_API_ID = "2040"
DEFAULT_API_HASH = "b18441a1ff607e10a989891a5462e627"

API_ID = int(os.getenv("API_ID", DEFAULT_API_ID))
API_HASH = os.getenv("API_HASH", DEFAULT_API_HASH)
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_DB_URI = os.getenv("MONGO_DB_URI", os.getenv("MONGODB_URI", ""))
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/song_assistant")
UPDATES_CHANNEL = os.getenv("UPDATES_CHANNEL", "https://t.me/secretsbotz")
MUST_JOIN = os.getenv("MUST_JOIN", "secretsbotz")
LOGGER_ID = int(os.getenv("LOGGER_ID", str(OWNER_ID)))
