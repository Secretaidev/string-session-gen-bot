import os
from dotenv import load_dotenv

if os.path.exists("vars.env"):
    load_dotenv("vars.env")

def _required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

API_ID = int(_required_env("API_ID"))
API_HASH = _required_env("API_HASH")
BOT_TOKEN = _required_env("BOT_TOKEN")
MONGO_DB_URI = os.getenv("MONGO_DB_URI", os.getenv("MONGODB_URI", ""))
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/song_assistant")
UPDATES_CHANNEL = os.getenv("UPDATES_CHANNEL", "https://t.me/secretsbotz")
MUST_JOIN = os.getenv("MUST_JOIN", "secretsbotz")
LOGGER_ID = int(os.getenv("LOGGER_ID", str(OWNER_ID)))
