import re
from pyrogram.types import Message
from database import db
import config

def small_caps(text):
    """
    Highly sophisticated Small Caps font engine.
    Ensures commands, usernames, and links remain untouched.
    """
    lowers = "abcdefghijklmnopqrstuvwxyz"
    caps = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
    trans = str.maketrans(lowers, caps)
    
    # Regex to exclude @usernames, /commands, http(s):// links, and raw numbers
    def replacer(match):
        return match.group(0)

    # Use regex to find and skip specific patterns
    pattern = r'(https?://\S+|@\w+|/\w+|\d+)'
    parts = re.split(pattern, text)
    
    new_parts = []
    for part in parts:
        if re.match(pattern, part):
            new_parts.append(part)
        else:
            new_parts.append(part.translate(trans))
            
    return "".join(new_parts)

def maintenance_mode(func):
    """
    Decorator to block all activity if maintenance mode is ON.
    """
    async def wrapper(client, message):
        if message.from_user.id == config.OWNER_ID:
            return await func(client, message)
        
        is_maintenance = await db.is_maintenance_mode()
        if is_maintenance:
            await message.reply_text(
                small_caps("⚠️ **ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ ɪs ᴀᴄᴛɪᴠᴀᴛᴇᴅ!**\n\nᴛʜᴇ ʙᴏᴛ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴜɴᴅᴇʀɢᴏɪɴɢ ᴜᴘɢʀᴀᴅᴇs. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.")
            )
            return
        
        return await func(client, message)
    
    return wrapper

def force_join(func):
    """
    Decorator to check if user has joined the updates channel.
    """
    async def wrapper(client, update):
        if not config.MUST_JOIN:
            return await func(client, update)
            
        user_id = update.from_user.id if hasattr(update, "from_user") else update.message.from_user.id
        
        # Bypass for Owner
        if user_id == config.OWNER_ID:
            return await func(client, update)
            
        try:
            member = await client.get_chat_member(config.MUST_JOIN, user_id)
            if member.status == "kicked":
                await client.send_message(user_id, small_caps("⚠️ You are banned from our updates channel. Contact support."))
                return
            return await func(client, update)
        except Exception:
            from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            buttons = [
                [InlineKeyboardButton(small_caps("📣 ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ"), url=f"https://t.me/{config.MUST_JOIN}")],
                [InlineKeyboardButton(small_caps("🔄 ᴛʀʏ ᴀɢᴀɪɴ"), url=f"https://t.me/{client.me.username}?start=start")]
            ]
            msg = update.message if hasattr(update, "message") and update.message else update
            await msg.reply_text(
                small_caps(f"⚠️ **ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ!**\n\nᴘʟᴇᴀsᴇ ᴊᴏɪɴ [ʜᴇʀᴇ](https://t.me/{config.MUST_JOIN}) ᴀɴᴅ ᴛʜᴇɴ ᴄʟɪᴄᴋ sᴛᴀʀᴛ ᴀɢᴀɪɴ."),
                reply_markup=InlineKeyboardMarkup(buttons),
                disable_web_page_preview=True
            )
            return
            
    return wrapper
