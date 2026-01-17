# ============================================================
# AIRA Personality Version - Updated by KD's AI Partner 🌸
# Fixes: MessageNotModified Error & Callback Handlers
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto
)
from pyrogram.errors import MessageNotModified
from config import BOT_USERNAME, SUPPORT_GROUP, UPDATE_CHANNEL, START_IMAGE, OWNER_ID
import db
import random

def register_handlers(app: Client):

    # --- Utility: Safe Edit Media (Fixes 400 Error) ---
    async def safe_edit_menu(callback_query, text, buttons):
        try:
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
        except MessageNotModified:
            await callback_query.answer("Aap pehle se isi menu mein hain! ✨", show_alert=False)
        except Exception as e:
            print(f"Error: {e}")

    # --- Main Start Menu Logic ---
    async def send_start_menu(message, user_name):
        text = f"""
✨ **Hi {user_name}! Main hoon AIRA** 🎀

Aapka swagat hai! Main ek smart aur friendly group manager hoon. 
Mujhe dosti karna aur groups ko safe rakhna pasand hai! 🌸

**Main aapki help kaise kar sakti hoon?**
─────────────────────────────
• 🛡️ **Anti-Spam**: Links ko main turant hata deti hoon!
• 🔒 **Lock System**: Group elements ko lock karein.
• 📋 **Rules**: Aapke group ke usool, meri zimmedari.
• 💤 **AFK Mode**: Jab aap busy hon, main sab sambhaal lungi.

Kya aap mujhe apne group mein add karenge? 🙈
"""
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎀 Add AIRA to Group 🎀", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [
                InlineKeyboardButton("🌸 Support", url=SUPPORT_GROUP),
                InlineKeyboardButton("📢 Updates", url=UPDATE_CHANNEL),
            ],
            [
                InlineKeyboardButton("※ Owner", url=f"tg://user?id={OWNER_ID}"),
                InlineKeyboardButton("📚 Help Menu", callback_data="help_menu"),
            ]
        ])

        if hasattr(message, 'reply_photo'): # If it's a new command
            await message.reply_photo(START_IMAGE, caption=text, reply_markup=buttons)
        else: # If it's a callback (Back button)
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await message.edit_media(media=media, reply_markup=buttons)

    # --- Start Command ---
    @app.on_message(filters.private & filters.command("start"))
    async def start_command(client, message):
        user = message.from_user
        await db.add_user(user.id, user.first_name)
        await send_start_menu(message, user.first_name)

    # --- Help Categories Menu ---
    @app.on_callback_query(filters.regex("help_menu"))
    async def help_callback(client, callback_query):
        text = "🌸 **Help Menu** 🌸\n\nChoose a category to explore my powers:"
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⚙️ Moderation", callback_data="mod_h"),
                InlineKeyboardButton("🔒 Locks", callback_data="lock_h"),
            ],
            [
                InlineKeyboardButton("📋 Rules/Filters", callback_data="rules_h"),
                InlineKeyboardButton("👋 Greetings", callback_data="greet_h"),
            ],
            [
                InlineKeyboardButton("💤 AFK System", callback_data="afk_h"),
                InlineKeyboardButton("👤 Owner", callback_data="owner_h")
            ],
            [InlineKeyboardButton("🔙 Back to Home", callback_data="back_home")]
        ])
        await safe_edit_menu(callback_query, text, buttons)

    # --- Back to Home Handler ---
    @app.on_callback_query(filters.regex("back_home"))
    async def back_home_callback(client, callback_query):
        await send_start_menu(callback_query.message, callback_query.from_user.first_name)
        await callback_query.answer()

    # --- Individual Help Handlers (Example: AFK) ---
    @app.on_callback_query(filters.regex("afk_h"))
    async def afk_help_callback(client, callback_query):
        text = "**💤 AFK System**\n\nJab aap busy hon, toh `/afk [reason]` likhein. Main sabko bata dungi! ✨"
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help_menu")]])
        await safe_edit_menu(callback_query, text, buttons)

    # --- Owner Help Handler ---
    @app.on_callback_query(filters.regex("owner_h"))
    async def owner_help_callback(client, callback_query):
        text = "**👤 Owner Commands**\n\nSirf mere Owner ke liye:\n- `/broadcast`: Sabko msg bhejein.\n- `/stats`: Meri growth check karein. 📈"
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help_menu")]])
        await safe_edit_menu(callback_query, text, buttons)

    # ==========================================
    # 🕵️‍♂️ KD SPECIAL: INTROVERT PROTECTION
    # ==========================================
    @app.on_message(filters.private & filters.text & ~filters.command(["start", "help", "id"]))
    async def handle_strangers(client, message):
        if message.from_user.id != int(OWNER_ID):
            responses = [
                "Hehe, main sirf KD ki baatein sunti hoon! 🎀",
                "Aap mujhse dosti karna chahte hain? Pehle mere owner se puchiye! 😉",
                "Main thodi busy hoon rules banane mein, baad mein baat karein? ✨"
            ]
            await message.reply_text(random.choice(responses))
