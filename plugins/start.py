from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from database import db
from utils import small_caps, maintenance_mode, force_join
import config

START_TEXT = """
ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ **ᴀᴅᴠᴀɴᴄᴇᴅ sᴛʀɪɴɢ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ**.

ᴛʜɪs ʙᴏᴛ ʜᴇʟᴘs ʏᴏᴜ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ **ᴘʏʀᴏɢʀᴀᴍ** ᴀɴᴅ **ᴛᴇʟᴇᴛʜᴏɴ** sᴇssɪᴏɴ sᴛʀɪɴɢs ᴇᴀsɪʟʏ ᴀɴᴅ sᴇᴄᴜʀᴇʟʏ.
"""

HELP_TEXT = """
💡 **ʜᴏᴡ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴀ sᴛʀɪɴɢ sᴇssɪᴏɴ:**

1. ᴄʟɪᴄᴋ ᴏɴ 'ɢᴇɴᴇʀᴀᴛᴇ sᴇssɪᴏɴ'.
2. ᴄʜᴏᴏsᴇ ʏᴏᴜʀ ᴘʀᴇғᴇʀʀᴇᴅ ʟɪʙʀᴀʀʏ (ᴘʏʀᴏɢʀᴀᴍ ᴏʀ ᴛᴇʟᴇᴛʜᴏɴ).
3. Eɴᴛᴇʀ ʏᴏᴜʀ **API ID** ᴀɴᴅ **API HASH** (ɢᴇᴛ ɪᴛ ғʀᴏᴍ my.telegram.org).
4. Eɴᴛᴇʀ ʏᴏᴜʀ ᴍᴏʙɪʟᴇ ɴᴜᴍʙᴇʀ ᴡɪᴛʜ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ.
5. Sᴇɴᴅ ᴛʜᴇ OTP.
6. Sᴇɴᴅ ᴛᴡᴏ-sᴛᴇᴘ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴘᴀssᴡᴏʀᴅ ɪғ ᴇɴᴀʙʟᴇᴅ.
7. Yᴏᴜ ᴡɪʟʟ ʀᴇᴄᴇɪᴠᴇ ʏᴏᴜʀ sᴇssɪᴏɴ sᴛʀɪɴɢ ɪɴ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs ᴀs ᴡᴇʟʟ ᴀs ʜᴇʀᴇ!

⚠️ **WARNING:** ᴅᴏ ɴᴏᴛ sʜᴀʀᴇ ʏᴏᴜʀ sᴇssɪᴏɴ sᴛʀɪɴɢ ᴡɪᴛʜ ᴀɴʏᴏɴᴇ!
"""

ABOUT_TEXT = """
🤖 **ᴀʙᴏᴜᴛ ᴛʜɪs ʙᴏᴛ:**

📝 **Lᴀɴɢᴜᴀɢᴇ:** `Pʏᴛʜᴏɴ 3`
🧰 **Fʀᴀᴍᴇᴡᴏʀᴋ:** `Pʏʀᴏɢʀᴀᴍ & pyromod`
👨‍💻 **Oᴡɴᴇʀ:** `{0}`
"""

def startup_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(small_caps("🚀 ɢᴇɴᴇʀᴀᴛᴇ sᴇssɪᴏɴ"), callback_data="generate")],
        [
            InlineKeyboardButton(small_caps("💡 ʜᴇʟᴘ"), callback_data="menu_help"),
            InlineKeyboardButton(small_caps("🤖 ᴀʙᴏᴜᴛ"), callback_data="menu_about")
        ],
        [
            InlineKeyboardButton(small_caps("📣 ᴜᴘᴅᴀᴛᴇs"), url=config.UPDATES_CHANNEL),
            InlineKeyboardButton(small_caps("💬 sᴜᴘᴘᴏʀᴛ"), url=config.SUPPORT_CHAT)
        ]
    ])

@Client.on_message(filters.command("start") & filters.private)
@maintenance_mode
@force_join
async def start_cmd(bot, message: Message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        # New User Log directly to Owner DM
        try:
            username = f"@{message.from_user.username}" if message.from_user.username else str(message.from_user.first_name)
            log_text = f"Nᴇᴡ Sᴛᴀʀᴛ Wᴀʟᴀ\nUɴᴀᴍᴇ: {username}"
            await bot.send_message(config.OWNER_ID, small_caps(log_text))
        except Exception:
            pass
            
    mention = message.from_user.mention
    final_caption = f"👋 Hɪɪ {mention}!\n" + small_caps(START_TEXT)
    
    try:
        await message.reply_photo(
            photo="https://telegra.ph/file/af55d7705973fa9f99e3b.jpg", # Placeholder
            caption=final_caption,
            reply_markup=startup_buttons()
        )
    except Exception:
        await message.reply_text(
            final_caption,
            reply_markup=startup_buttons()
        )

@Client.on_callback_query(filters.regex(r"^menu_(help|about|home)$"))
@maintenance_mode
@force_join
async def menu_navigation(bot, query: CallbackQuery):
    action = query.data.split("_")[1]
    
    if action == "help":
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton(small_caps("🔙 ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ"), callback_data="menu_home")]])
        await query.message.edit_caption(caption=small_caps(HELP_TEXT), reply_markup=buttons)
    elif action == "about":
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton(small_caps("🔙 ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ"), callback_data="menu_home")]])
        about_final = ABOUT_TEXT.format(query.from_user.id) # Show their id as reference or real owner if hardcoded
        await query.message.edit_caption(caption=small_caps(about_final), reply_markup=buttons)
    elif action == "home":
        mention = query.from_user.mention
        final_caption = f"👋 Hɪɪ {mention}!\n" + small_caps(START_TEXT)
        await query.message.edit_caption(caption=final_caption, reply_markup=startup_buttons())
