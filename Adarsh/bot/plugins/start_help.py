from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant
from Adarsh.bot import StreamBot
from Adarsh.vars import Var
from Adarsh.utils.database import Database

# ─── Logger & Database ─────────────────────────────
import logging
logger = logging.getLogger(__name__)
db = Database(Var.DATABASE_URL, Var.name)

# ─── Inline Buttons ────────────────────────────────
def get_main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("start⚡️", callback_data="start"),
            InlineKeyboardButton("help📚", callback_data="help"),
            InlineKeyboardButton("login🔑", callback_data="login"),
            InlineKeyboardButton("DC", callback_data="dc"),
        ],
        [
            InlineKeyboardButton("Channel❤️", url=f"https://t.me/{Var.UPDATES_CHANNEL}"),
            InlineKeyboardButton("ping📡", callback_data="ping"),
            InlineKeyboardButton("status📊", callback_data="status"),
            InlineKeyboardButton("Owner😎", url="https://t.me/SMD_Owner"),
        ],
    ])

def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back", callback_data="start")]
    ])

# ─── /start Command ────────────────────────────────
@StreamBot.on_message((filters.command("start") | filters.regex('start⚡️')) & filters.private)
async def start_handler(client, message):
    user_id = message.from_user.id
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id)
        await client.send_message(
            Var.BIN_CHANNEL,
            f"👤 New User Joined: [{message.from_user.first_name}](tg://user?id={user_id})"
        )
    
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await client.get_chat_member(Var.UPDATES_CHANNEL, user_id)
            if user.status == "kicked":
                return await message.reply("🚫 You are banned from using this bot.")
        except UserNotParticipant:
            return await message.reply_photo(
                photo="https://graph.org/file/4b8bf6ec079dbe5aac0cf.jpg",
                caption="🔒 Join the update channel to use this bot.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Join Now 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")]
                ])
            )

    await message.reply_photo(
        photo="https://graph.org/file/4b8bf6ec079dbe5aac0cf.jpg",
        caption=f"Hi {message.from_user.mention(style='md')}!\n\n"
                "I am a File to Link Generator Bot.\n\n"
                "Send any file to get direct download and streamable link.",
        reply_markup=get_main_keyboard()
    )

# ─── /help Command ────────────────────────────────
@StreamBot.on_message((filters.command("help") | filters.regex("help📚")) & filters.private)
async def help_handler(client, message):
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await client.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                return await message.reply("🚫 You are banned from using this bot.")
        except UserNotParticipant:
            return await message.reply_photo(
                photo="https://graph.org/file/4b8bf6ec079dbe5aac0cf.jpg",
                caption="🔐 Join the channel to use the bot.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Join Channel 🍁", url=f"https://t.me/{Var.UPDATES_CHANNEL}")]
                ])
            )

    await message.reply_text(
        "<b>📤 Send me any file and I will generate a streamable/downloadable link for you.</b>\n\n"
        "<b>📌 Add me to your channel for automated file linking.</b>",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Owner 👨‍💻", url="https://t.me/SMD_Owner")],
            [InlineKeyboardButton("Source Code 🧠", url="https://t.me/SMD_BOTz")],
            [InlineKeyboardButton("Back ⬅️", callback_data="start")]
        ]),
        disable_web_page_preview=True
    )

# ─── Callback Query Handler ───────────────────────
@StreamBot.on_callback_query()
async def callback_handler(client, query: CallbackQuery):
    data = query.data

    if data == "start":
        await query.message.edit_caption(
            caption="👋 Welcome back!\n\nSend a file to get a link.",
            reply_markup=get_main_keyboard()
        )
    elif data == "help":
        await query.message.edit_caption(
            caption="🆘 **Help Section**\n\n"
                    "Just send me any file and I’ll give you a link.\n"
                    "Use me in your channel too!",
            reply_markup=back_keyboard()
        )
    elif data == "login":
        await query.answer("🔐 Login is currently disabled.", show_alert=True)
    elif data == "dc":
        await query.answer("📡 Your nearest data center is being located...", show_alert=True)
    elif data == "ping":
        await query.answer("🏓 Pong! Bot is alive.", show_alert=True)
    elif data == "status":
        await query.answer("📊 Status: All systems operational.", show_alert=True)
    else:
        await query.answer("❓ Unknown action", show_alert=True)
