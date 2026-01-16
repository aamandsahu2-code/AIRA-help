# ============================================================
# Group Manager Bot - Updated Start & Help Handlers
# Author: LearningBotsOfficial (https://github.com/LearningBotsOfficial) 
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto
)
from config import BOT_USERNAME, SUPPORT_GROUP, UPDATE_CHANNEL, START_IMAGE, OWNER_ID
import db

def register_handlers(app: Client):

    # ==========================================================
    # Main Start Menu Logic
    # ==========================================================
    async def send_start_menu(message, user):
        text = f"""
✨ Hello {user}! ✨

👋 I am **AIRA** 🤖, your advanced Group Manager Bot.

**Highlights:**
─────────────────────────────
- 🛡️ Smart Anti-Spam & Link Shield
- 🔒 Advanced Lock System
- 📋 Rules & Filters Management
- 💤 AFK & Activity Tracker
- ⚡ Sleek UI with Inline Controls
"""
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚒️ Add to Group ⚒️", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [
                InlineKeyboardButton("⌂ Support", url=SUPPORT_GROUP),
                InlineKeyboardButton("⌂ Updates", url=UPDATE_CHANNEL),
            ],
            [
                InlineKeyboardButton("※ Owner", url=f"tg://user?id={OWNER_ID}"),
                InlineKeyboardButton("Repo", url="https://github.com/LearningBotsOfficial/AIRAe"),
            ],
            [InlineKeyboardButton("📚 Help Commands 📚", callback_data="help")]
        ])

        if message.text:
            await message.reply_photo(START_IMAGE, caption=text, reply_markup=buttons)
        else:
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await message.edit_media(media=media, reply_markup=buttons)

    # ==========================================================
    # Start Command
    # ==========================================================
    @app.on_message(filters.private & filters.command("start"))
    async def start_command(client, message):
        user = message.from_user
        await db.add_user(user.id, user.first_name)
        await send_start_menu(message, user.first_name)

    # ==========================================================
    # Help Categories Menu
    # ==========================================================
    async def send_help_menu(message):
        text = "╔══════════════════╗\n     **Help Menu**\n╚══════════════════╝\n\nChoose a category to explore commands:"
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⚙️ Moderation", callback_data="moderation"),
                InlineKeyboardButton("🔒 Locks", callback_data="locks"),
            ],
            [
                InlineKeyboardButton("📋 Rules/Filters", callback_data="rules_help"),
                InlineKeyboardButton("👋 Greetings", callback_data="greetings"),
            ],
            [
                InlineKeyboardButton("💤 AFK System", callback_data="afk_help"),
                InlineKeyboardButton("👤 Owner", callback_data="owner_help")
            ],
            [InlineKeyboardButton("🔙 Back to Home", callback_data="back_to_start")]
        ])
        media = InputMediaPhoto(media=START_IMAGE, caption=text)
        await message.edit_media(media=media, reply_markup=buttons)

    # Callback Handlers
    @app.on_callback_query(filters.regex("help"))
    async def help_callback(client, callback_query):
        await send_help_menu(callback_query.message)
        await callback_query.answer()

    @app.on_callback_query(filters.regex("back_to_start"))
    async def back_to_start_callback(client, callback_query):
        await send_start_menu(callback_query.message, callback_query.from_user.first_name)
        await callback_query.answer()

    # --- 1. Greetings Help ---
    @app.on_callback_query(filters.regex("greetings"))
    async def greetings_callback(client, callback_query):
        text = """**👋 Greetings System**\n\n- `/setwelcome <text>`: Custom welcome message set karein.\n- `/welcome on/off`: Welcome msg enable/disable karein.\n\n**Placeholders:** `{mention}`, `{first_name}`, `{username}`, `{title}`"""
        await callback_query.message.edit_media(media=InputMediaPhoto(media=START_IMAGE, caption=text), 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]]))

    # --- 2. Locks Help ---
    @app.on_callback_query(filters.regex("locks"))
    async def locks_callback(client, callback_query):
        text = """**🔒 Locks System**\n\n- `/lock <type>`: Group element lock karein.\n- `/unlock <type>`: Lock kholein.\n- `/locks`: Active locks check karein.\n\n**Types:** `url`, `sticker`, `media`, `username`, `forward`"""
        await callback_query.message.edit_media(media=InputMediaPhoto(media=START_IMAGE, caption=text), 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]]))

    # --- 3. Rules & Filters Help ---
    @app.on_callback_query(filters.regex("rules_help"))
    async def rules_help_callback(client, callback_query):
        text = """**📋 Rules & Filters**\n\n**Rules:**\n- `/setrules <text>`: Rules set karein.\n- `/rules`: Group rules dekhein.\n\n**Filters:**\n- `/filter <keyword> <reply>`: Auto-reply set karein.\n- `/filters`: List active filters.\n- `/stop <keyword>`: Filter delete karein."""
        await callback_query.message.edit_media(media=InputMediaPhoto(media=START_IMAGE, caption=text), 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]]))

    # --- 4. Moderation Help ---
    @app.on_callback_query(filters.regex("moderation"))
    async def moderation_callback(client, callback_query):
        text = """**⚙️ Moderation Tools**\n\n- `/ban` | `/unban`: User ban/unban karein.\n- `/mute` | `/unmute`: User restrict karein.\n- `/kick`: User ko group se nikalein.\n- `/warn` | `/resetwarns`: Warnings manage karein.\n- `/promote` | `/demote`: Admin roles manage karein."""
        await callback_query.message.edit_media(media=InputMediaPhoto(media=START_IMAGE, caption=text), 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]]))

    # --- 5. AFK Help ---
    @app.on_callback_query(filters.regex("afk_help"))
    async def afk_help_callback(client, callback_query):
        text = """**💤 AFK System**\n\n- `/afk <reason>`: AFK mode on karein. Jab aapko koi tag karega bot reply dega.\n- **Activity Tracker:** Automatically tracks when users were last seen active in the chat."""
        await callback_query.message.edit_media(media=InputMediaPhoto(media=START_IMAGE, caption=text), 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]]))

    # --- 6. Owner Commands ---
    @app.on_callback_query(filters.regex("owner_help"))
    async def owner_help_callback(client, callback_query):
        text = """**👤 Owner Commands**\n\n- `/broadcast`: Reply to a msg to send to all users.\n- `/stats`: Bot usage stats dekhein."""
        await callback_query.message.edit_media(media=InputMediaPhoto(media=START_IMAGE, caption=text), 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]]))

    # ==========================================================
    # Broadcast & Stats Commands
    # ==========================================================
    @app.on_message(filters.private & filters.command("broadcast"))
    async def broadcast_message(client, message):
        if message.from_user.id != OWNER_ID:
            return await message.reply_text("❌ Only Owner can use this.")
        if not message.reply_to_message:
            return await message.reply_text("⚠️ Reply to a message to broadcast.")
        
        users = await db.get_all_users()
        sent = 0
        for user_id in users:
            try:
                await message.reply_to_message.copy(user_id)
                sent += 1
            except: pass
        await message.reply_text(f"✅ Broadcast finished! Sent to {sent} users.")

    @app.on_message(filters.private & filters.command("stats"))
    async def stats_command(client, message):
        if message.from_user.id != OWNER_ID: return
        users = await db.get_all_users()
        await message.reply_text(f"📊 **Bot Stats:**\n\nTotal Users: `{len(users)}`")
