from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from pyrogram.errors import MessageNotModified, MessageIdInvalid
from config import BOT_USERNAME, SUPPORT_GROUP, UPDATE_CHANNEL, START_IMAGE, OWNER_ID
import db

def register_handlers(app: Client):

    # --- Utility: Safe Edit (Fixes 400 Errors) ---
    async def safe_edit(message, text, buttons):
        try:
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await message.edit_media(media=media, reply_markup=buttons)
        except (MessageNotModified, MessageIdInvalid):
            pass # Error ignore karein taaki logs saaf rahein

    # --- Start Menu Logic ---
    async def send_start_menu(message, user_name, is_callback=False):
        text = f"✨ **Hi {user_name}! Main hoon AIRA** 🎀\n\nAapka swagat hai! Kya aap mujhe apne group mein add karenge? 🙈"
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎀 Add AIRA to Group 🎀", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [InlineKeyboardButton("🌸 Support", url=SUPPORT_GROUP), InlineKeyboardButton("📢 Updates", url=UPDATE_CHANNEL)],
            [InlineKeyboardButton("※ Owner", url=f"tg://user?id={OWNER_ID}"), InlineKeyboardButton("📚 Help Menu", callback_data="help_menu")]
        ])
        
        if is_callback:
            await safe_edit(message, text, buttons)
        else:
            await message.reply_photo(START_IMAGE, caption=text, reply_markup=buttons)

    # --- Handlers ---
    @app.on_message(filters.private & filters.command("start"))
    async def start_command(client, message):
        user = message.from_user
        await db.add_user(user.id, user.first_name)
        await send_start_menu(message, user.first_name)

    @app.on_callback_query(filters.regex("help_menu"))
    async def help_callback(client, callback_query):
        text = "🌸 **AIRA Help Menu** 🌸\n\nKiski help chahiye aapko?"
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚙️ Moderation", callback_data="mod_h"), InlineKeyboardButton("🔒 Locks", callback_data="lock_h")],
            [InlineKeyboardButton("📋 Rules/Filters", callback_data="rules_h"), InlineKeyboardButton("💤 AFK System", callback_data="afk_h")],
            [InlineKeyboardButton("🔙 Back to Home", callback_data="back_home")]
        ])
        await safe_edit(callback_query.message, text, buttons)
        await callback_query.answer()

    @app.on_callback_query(filters.regex("back_home"))
    async def back_home_callback(client, callback_query):
        await send_start_menu(callback_query.message, callback_query.from_user.first_name, is_callback=True)
        await callback_query.answer()
