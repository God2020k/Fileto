# (c) adarsh-goel 
from Adarsh.bot import StreamBot
from Adarsh.vars import Var
import logging
logger = logging.getLogger(__name__)
from Adarsh.bot.plugins.stream import MY_PASS
from Adarsh.utils.human_readable import humanbytes
from Adarsh.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size
db = Database(Var.DATABASE_URL, Var.name)

# Removed ReplyKeyboardMarkup import since we use inline keyboards now

if MY_PASS:
    buttonz = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("start⚡️", callback_data="start"),
                InlineKeyboardButton("help📚", callback_data="help"),
                InlineKeyboardButton("login🔑", callback_data="login"),
                InlineKeyboardButton("DC", callback_data="dc"),
            ],
            [
                InlineKeyboardButton("Channel❤️", callback_data="channel"),
                InlineKeyboardButton("ping📡", callback_data="ping"),
                InlineKeyboardButton("status📊", callback_data="status"),
                InlineKeyboardButton("Owner😎", callback_data="owner"),
            ],
        ]
    )
else:
    buttonz = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("start⚡️", callback_data="start"),
                InlineKeyboardButton("help📚", callback_data="help"),
                InlineKeyboardButton("DC", callback_data="dc"),
            ],
            [
                InlineKeyboardButton("Channel❤️", callback_data="channel"),
                InlineKeyboardButton("ping📡", callback_data="ping"),
                InlineKeyboardButton("status📊", callback_data="status"),
                InlineKeyboardButton("Owner😎", callback_data="owner"),
            ],
        ]
    )
from pyrogram.types import CallbackQuery

# Your inline keyboard (example)
buttonz = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("start⚡️", callback_data="start"),
        InlineKeyboardButton("help📚", callback_data="help"),
        InlineKeyboardButton("login🔑", callback_data="login"),
        InlineKeyboardButton("DC", callback_data="dc"),
    ],
    [
        InlineKeyboardButton("Channel❤️", callback_data="channel"),
        InlineKeyboardButton("ping📡", callback_data="ping"),
        InlineKeyboardButton("status📊", callback_data="status"),
        InlineKeyboardButton("Owner😎", callback_data="owner"),
    ],
])

# Callback query handler for buttons
@StreamBot.on_callback_query()
async def on_button_click(bot, query: CallbackQuery):
    data = query.data  # Get the callback_data from the button clicked

    if data == "start":
        await query.answer()  # Acknowledge button press (avoids loading icon)
        await query.message.edit_text(
            "Welcome back! Use /start to begin or send me a file.",
            reply_markup=buttonz
        )

    elif data == "help":
        await query.answer()
        await query.message.edit_text(
            "Help Menu:\n\n- Send any file to get links.\n- Use /list for commands.\n- Contact owner for support.",
            reply_markup=buttonz
        )

    elif data == "login":
        await query.answer("Login feature is under development.", show_alert=True)

    elif data == "dc":
        await query.answer()
        await query.message.edit_text(
            "Disconnected from current session. Use /start to begin again.",
            reply_markup=buttonz
        )

    elif data == "channel":
        await query.answer()
        await query.message.edit_text(
            f"Join our Channel: https://t.me/{Var.UPDATES_CHANNEL}",
            reply_markup=buttonz
        )

    elif data == "ping":
        await query.answer("Pong! 🏓")
        # optionally edit or send a new message with ping time

    elif data == "status":
        await query.answer()
        # Example: fetch status from somewhere
        await query.message.edit_text(
            "Bot is running smoothly! ✅",
            reply_markup=buttonz
        )

    elif data == "owner":
        await query.answer()
        await query.message.edit_text(
            "Contact Owner: @SMD_Owner",
            reply_markup=buttonz
        )

    else:
        await query.answer("Unknown action.", show_alert=True)
  ),
            )
