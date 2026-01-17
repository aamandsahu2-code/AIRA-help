from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from config import BOT_USERNAME, SUPPORT_GROUP, UPDATE_CHANNEL, START_IMAGE, OWNER_ID
import db

def register_handlers(app: Client):

    # --- Start Menu Function ---
    async def send_start_menu(message, user_name):
        text = f"✨ **Hi {user_name}! Main hoon AIRA** 🎀\n\nAapka swagat hai! Main ek smart group manager hoon. Kya aap mujhe apne group mein add karenge? 🙈"
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎀 Add AIRA to Group 🎀", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [InlineKeyboardButton("🌸 Support", url=SUPPORT_GROUP), InlineKeyboardButton("📢 Updates", url=UPDATE_CHANNEL)],
            [InlineKeyboardButton("※ Owner", url=f"tg://user?id={OWNER_ID}"), InlineKeyboardButton("📚 Help Menu", callback_data="help")]
        ])
        
        if message.reply_to_message or hasattr(message, 'photo'): # Edit check
            await message.edit_media(media=InputMediaPhoto(media=START_IMAGE, caption=text), reply_markup=buttons)
        else:
            await message.reply_photo(START_IMAGE, caption=text, reply_markup=buttons)

    # --- Start Command ---
    @app.on_message(filters.private & filters.command("start"))
    async def start_cmd(client, message):
        user = message.from_user
        await db.add_user(user.id, user.first_name)
        await send_start_menu(message, user.first_name)

    # --- Main Help Menu ---
    @app.on_callback_query(filters.regex("help"))
    async def help_menu(client, callback_query):
        text = "🌸 **AIRA Help Menu** 🌸\n\nKiski help chahiye aapko?"
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚙️ Moderation", callback_data="mod_help"), InlineKeyboardButton("🔒 Locks", callback_data="lock_help")],
            [InlineKeyboardButton("📋 Rules/Filters", callback_data="rules_help"), InlineKeyboardButton("💤 AFK System", callback_data="afk_help")],
            [InlineKeyboardButton("🔙 Back to Home", callback_data="back_home")]
        ])
        await callback_query.message.edit_media(media=InputMediaPhoto(media=START_IMAGE, caption=text), reply_markup=buttons)

    # --- Back to Home Handler ---
    @app.on_callback_query(filters.regex("back_home"))
    async def back_home(client, callback_query):
        await send_start_menu(callback_query.message, callback_query.from_user.first_name)

    # --- AFK & Rules Handlers (Sample) ---
    @app.on_callback_query(filters.regex("afk_help"))
    async def afk_h(client, callback_query):
        await callback_query.message.edit_caption("💤 **AFK System**\n\nUse `/afk [reason]` jab aap busy hon. Main sabko bata dungi!", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]]))

    # ==========================================
    # 🕵️‍♂️ KD SPECIAL: ANTI-SPY / INTROVERT FILTER
    # ==========================================
    @app.on_message(filters.text & ~filters.me)
    async def introvert_filter(client, message):
        msg_text = message.text.lower()
        if "spy" in msg_text or "kaun ho" in msg_text:
            responses = [
                "Main koi spy nahi hoon, main toh KD ki pyaari AIRA hoon! 🎀",
                "Hehe, mysterious lag rahi hoon kya? Main toh bas help karne aayi hoon! ✨",
                "Secret agent toh nahi hoon, par aapke group ka dhyan zaroor rakh sakti hoon! 😉"
            ]
            import random
            await message.reply_text(random.choice(responses))
