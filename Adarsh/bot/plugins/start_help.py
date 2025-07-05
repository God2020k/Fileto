# (c) adarsh-goel
import logging
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant
from Adarsh.bot import StreamBot
from Adarsh.vars import Var
from Adarsh.utils.database import Database

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize DB
db = Database(Var.DATABASE_URL, Var.name)

# Buttons (with or without login)
def get_main_buttons():
    buttons = [
        [
            InlineKeyboardButton("⚡ Start", callback_data="start"),
            InlineKeyboardButton("📚 Help", callback_data="help"),
        ],
        [
            InlineKeyboardButton("📡 Ping", callback_data="ping"),
            InlineKeyboardButton("📊 Status", callback_data="status"),
        ],
        [
            InlineKeyboardButton("❤️ Channel", callback_data="channel"),
            InlineKeyboardButton("😎 Owner", callback_data="owner"),
        ]
    ]

    if Var.MY_PASS:
        buttons[0].append(InlineKeyboardButton("🔑 Login", callback_data="login"))
        buttons[1].append(InlineKeyboardButton("🌐 DC", callback_data="dc"))
    else:
        buttons[0].append(InlineKeyboardButton("🌐 DC", callback_data="dc"))

    return InlineKeyboardMarkup(buttons)

# Subscription checker
async def check_subscription(bot, user_id):
    if Var.UPDATES_CHANNEL == "None":
        return True
    try:
        user = await bot.get_chat_member(Var.UPDATES_CHANNEL, user_id)
        return user.status != "kicked"
    except UserNotParticipant:
        return "not_joined"
    except Exception as e:
        logger.error(f"Subscription check error: {e}")
        return False

# Register new users
async def register_user(bot, user):
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"👤 New User Joined:\n[{user.first_name}](tg://user?id={user.id}) started the bot."
        )

# START COMMAND
@StreamBot.on_message((filters.command("start") | filters.regex("start⚡️")) & filters.private)
async def start_handler(bot, message):
    user = message.from_user
    await register_user(bot, user)

    check = await check_subscription(bot, message.chat.id)
    if check == "not_joined":
        await bot.send_photo(
            chat_id=message.chat.id,
            photo="https://graph.org/file/4b8bf6ec079dbe5aac0cf.jpg",
            caption="<b>🔐 Join our updates channel to use this bot.</b>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔓 Join Now", url=f"https://t.me/{Var.UPDATES_CHANNEL}")]
            ])
        )
        return
    elif not check:
        await bot.send_message(
            chat_id=message.chat.id,
            text="❌ Something went wrong. Contact [Support](https://t.me/SAM_DUB_LEZHa)",
            disable_web_page_preview=True
        )
        return

    await bot.send_photo(
        chat_id=message.chat.id,
        photo="https://graph.org/file/4b8bf6ec079dbe5aac0cf.jpg",
        caption=f"👋 Hi {user.mention(style='md')}!\n\n"
                "🤖 I am a bot that gives you direct and streamable download links from Telegram media.\n"
                "📥 Send me any file to begin.",
        reply_markup=get_main_buttons()
    )

# HELP COMMAND
@StreamBot.on_message((filters.command("help") | filters.regex("help📚")) & filters.private)
async def help_handler(bot, message):
    user = message.from_user
    await register_user(bot, user)

    check = await check_subscription(bot, message.chat.id)
    if check == "not_joined":
        await bot.send_photo(
            chat_id=message.chat.id,
            photo="https://graph.org/file/4b8bf6ec079dbe5aac0cf.jpg",
            caption="🛠 To use this bot, you must join the updates channel first.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔓 Join Updates", url=f"https://t.me/{Var.UPDATES_CHANNEL}")]
            ])
        )
        return
    elif not check:
        await bot.send_message(
            chat_id=message.chat.id,
            text="❌ Something went wrong. Contact the [Owner](https://t.me/SMD_Owner).",
            disable_web_page_preview=True
        )
        return

    await message.reply_text(
        "<b>📘 Help Section</b>\n\n"
        "• Just send me a file and I’ll reply with a download link.\n"
        "• Add me to your channel and I can auto-generate links there too.\n"
        "• Use /list for all available commands.",
        disable_web_page_preview=True,
        reply_markup=get_main_buttons()
    )

# CALLBACK HANDLER
@StreamBot.on_callback_query()
async def button_callbacks(bot, query: CallbackQuery):
    data = query.data
    user = query.from_user

    if data == "start":
        await query.message.edit_caption(
            caption=f"👋 Hi {user.mention(style='md')}!\n\n"
                    "I'm here to generate streaming/download links for your Telegram files.",
            reply_markup=get_main_buttons()
        )
    elif data == "help":
        await query.message.edit_caption(
            caption="📚 <b>Help Section</b>\n\n"
                    "Send me any file and I'll give you streamable and download links.\n"
                    "Add me to a channel for automatic link generation.",
            reply_markup=get_main_buttons()
        )
    elif data == "login":
        await query.answer("Login is not required. You're already good to go!", show_alert=True)
    elif data == "dc":
        await query.answer("🌍 Current Data Center: Detected automatically by Telegram", show_alert=True)
    elif data == "ping":
        await query.answer("🏓 Pong! I'm alive.", show_alert=True)
    elif data == "status":
        total_users = await db.total_users_count()
        await query.message.edit_caption(
            caption=f"📊 <b>Bot Status</b>\n\nTotal users: <code>{total_users}</code>",
            reply_markup=get_main_buttons()
        )
    elif data == "channel":
        await query.message.edit_caption(
            caption=f"📢 <b>Our Updates Channel</b>\n\n@{Var.UPDATES_CHANNEL}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔔 Join Channel", url=f"https://t.me/{Var.UPDATES_CHANNEL}")]
            ])
        )
    elif data == "owner":
        await query.message.edit_caption(
            caption="👨‍💻 <b>Bot Developer</b>\n\nContact: @SMD_Owner",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 Message Owner", url="https://t.me/SMD_Owner")]
            ])
        )
    else:
        await query.answer("❓ Unknown action", show_alert=True)
