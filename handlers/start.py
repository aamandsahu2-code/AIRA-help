# ============================================================
# Group Manager Bot - AIRA Personality Version 🎀
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
    # Main Start Menu Logic (AIRA Personality)
    # ==========================================================
    async def send_start_menu(message, user):
        text = f"""
✨ **Hi {user}! Main hoon AIRA** 🎀

Aapka swagat hai! Main ek smart aur friendly group manager hoon. 
Mujhe aapke group ko safe aur active rakhna bahut pasand hai. 🌸

**Main aapki help kaise kar sakti hoon?**
─────────────────────────────
• 🛡️ **Anti-Spam**: Links aur spam ko main turant hata deti hoon!
• 🔒 **Lock System**: Group elements ko meri marzi se lock karein.
• 📋 **Rules**: Aap jo rules kahenge, main sabko wahi dikhaungi.
• 💤 **AFK Mode**: Jab aap busy ho, main sabko pyaari si notice de dungi.
• 👤 **Moderation**: Badmash users ko main group se nikalne mein expert hoon!

Kya aap mujhe apne group mein add karke mujhse dosti karenge? 🙈
"""
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎀 Add AIRA to Group 🎀", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [
                InlineKeyboardButton("🌸 Support", url=SUPPORT_GROUP),
                InlineKeyboardButton("📢 Updates", url=UPDATE_CHANNEL),
            ],
            [
                InlineKeyboardButton("※ Owner", url=f"tg://user?id={OWNER_ID}"),
                InlineKeyboardButton("Repo", url="https://github.com/LearningBotsOfficial/AIRA"),
            ],
            [InlineKeyboardButton("📚 Mere Commands 📚", callback_data="help")]
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
        text = "╔══════════════════╗\n     🌸 **Help Menu** 🌸\n╚══════════════════╝\n\nChoose a category to explore my powers:"
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
        await callback_query.answer("Exploring AIRA's menu... ✨")

    @app.on_callback_query(filters.regex("back_to_start"))
    async def back_to_start_callback(client, callback_query):
        await send_start_menu(callback_query.message, callback_query.from_user.first_name)
        await callback_query.answer()

    # --- 1. Greetings Help ---
    @app.on_callback_query(filters.regex("greetings"))
    async def greetings_callback(client, callback_query):
        text = """**👋 Greetings System**\n\nAww! Ek naya member aaya hai? Main unka swagat bahut pyaare tareeke se karungi! 🌸\n\n- `/setwelcome <text>`: Custom welcome message set karein.\n- `/welcome on/off`: Welcome msg enable/disable karein.\n\n**Placeholders:** `{mention}`, `{first_name}`, `{username}`, `{title}`"""
        await callback_query.message.edit_media(media=InputMediaPhoto(media=START_IMAGE, caption=text), 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]]))

    # --- 2. Locks Help ---
    @app.on_callback_query(filters.regex("locks"))
    async def locks_callback(client, callback_query):
        text = """**🔒 Locks System**\n\nAgar koi group mein gande links bhej raha hai, toh main use turant rok dungi! 🛡️\n\n- `/lock <type>`: Group element lock karein.\n- `/unlock <type>`: Lock kholein.\n- `/locks`: Check active locks.\n\n**Types:** `url`, `sticker`, `media`, `username`, `forward`"""
        await callback_query.message.edit_media(media=InputMediaPhoto(media=START_IMAGE, caption=text), 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]]))

    # --- 3. Rules & Filters Help ---
    @app.on_callback_query(filters.regex("rules_help"))
    async def rules_help_callback(client, callback_query):
        text = """**📋 Rules & Filters**\n\nGroup ke apne usool hone chahiye, haina? ✨\n\n**Rules:**\n- `/setrules <text>`: Rules set karein.\n- `/rules`: Group rules dekhein.\n\n**Filters:**\n- `/filter <keyword> <reply>`: Auto-reply set karein.\n- `/stop <keyword>`: Filter delete karein."""
        await callback_query.message.edit_media(media=InputMediaPhoto(media=START_IMAGE, caption=text), 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]]))

    # --- 4. Moderation Help ---
    @app.on_callback_query(filters.regex("moderation"))
    async def moderation_callback(client, callback_query):
        text = """**⚙️ Moderation Tools**\n\nBadmashon ke liye AIRA thodi sakht hai! 👢\n\n- `/ban` | `/unban`: User ban/unban karein.\n- `/mute` | `/unmute`: User ko chup karayein.\n- `/kick`: User ko nikalein.\n- `/warn` | `/resetwarns`: Warnings manage karein.\n- `/promote` | `/demote`: Admin roles manage karein."""
        await callback_query.message.edit_media(media=InputMediaPhoto(media=START_IMAGE, caption=text), 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]]))

    # --- 5. AFK Help ---
    @app.on_callback_query(filters.regex("afk_help"))
    async def afk_help_callback(client, callback_query):
        text = """**💤 AFK System**\n\nAgar aap thodi der ke liye ja rahe ho, toh mujhe bata dena! Main sabko bol dungi. ✨\n\n- `/afk <reason>`: AFK mode on karein. \n- **Activity Tracker:** Main nazar rakhti hoon ki kaun kab active tha! 😉"""
        await callback_query.message.edit_media(media=InputMediaPhoto(media=START_IMAGE, caption=text), 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]]))

    # --- 6. Owner Commands ---
    @app.on_callback_query(filters.regex("owner_help"))
    async def owner_help_callback(client, callback_query):
        text = """**👤 Owner Commands**\n\nSirf mere Owner ke liye special commands: 🤫\n\n- `/broadcast`: Sabko message bhejne ke liye.\n- `/stats`: Meri performance check karein."""
        await callback_query.message.edit_media(media=InputMediaPhoto(media=START_IMAGE, caption=text), 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]]))

    # ==========================================================
    # Broadcast & Stats Commands
    # ==========================================================
    @app.on_message(filters.private & filters.command("broadcast"))
    async def broadcast_message(client, message):
        if message.from_user.id != OWNER_ID:
            return await message.reply_text("❌ Sorry, ye command sirf mere Owner ke liye hai.")
        if not message.reply_to_message:
            return await message.reply_text("⚠️ Please kisi message ka reply karein!")
        
        users = await db.get_all_users()
        sent = 0
        for user_id in users:
            try:
                await message.reply_to_message.copy(user_id)
                sent += 1
            except: pass
        await message.reply_text(f"✅ Broadcast finished! Maine {sent} doston ko message bhej diya. ✨")

    @app.on_message(filters.private & filters.command("stats"))
    async def stats_command(client, message):
        if message.from_user.id != OWNER_ID: return
        users = await db.get_all_users()
        await message.reply_text(f"📊 **My Stats:**\n\nTotal Users: `{len(users)}` \nMain itne logon ki help kar rahi hoon! ✨")
