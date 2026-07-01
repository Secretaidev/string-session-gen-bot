import os
from dotenv import load_dotenv

if os.path.exists("vars.env"):
    load_dotenv("vars.env")

def _required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

API_ID = int(_required_env("33612785"))
API_HASH = _required_env("5e0b5d4bf22de8879f3389d785c03813")
BOT_TOKEN = _required_env("8746324484:AAGMWJEquObuX2BT2h8UUazR0riJuiAz8QE")
MONGO_DB_URI = os.getenv("MONGO_DB_URI", os.getenv("mongodb+srv://aditya0:aditya0@cluster0.9m8897t.mongodb.net/?appName=Cluster0", ""))
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "")
UPDATES_CHANNEL = os.getenv("UPDATES_CHANNEL", "https://t.me/Xyron_Bots")
MUST_JOIN = os.getenv("MUST_JOIN", "Xyron_Bots")
LOGGER_ID = int(os.getenv("LOGGER_ID", str(OWNER_ID)))
