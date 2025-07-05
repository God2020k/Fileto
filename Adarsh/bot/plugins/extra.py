from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import shutil
import psutil
from utils_bot import get_readable_file_size, readable_time
from Adarsh import StartTime

# Import your bot instance
from Adarsh.bot import StreamBot

# Constant Text
START_TEXT = "Your Telegram DC Is: `{}`"

# Owner Command Handler
@StreamBot.on_message(filters.regex(r"(?i)^owner"))
async def owner_info(bot, message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="I am Coded By [SMD Admin](@SMD_Owner)",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🦋𝐒𝐌𝐃_𝐎𝐰𝐧𝐞𝐫🍁", url="https://t.me/SMD_Owner")]]
        ),
        disable_web_page_preview=True
    )

# Channel Command Handler
@StreamBot.on_message(filters.regex(r"(?i)^channel"))
async def channel_info(bot, message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="<b>𝐇𝐄𝐑𝐄'𝐒 𝐓𝐇𝐄 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝐋𝐈𝐍𝐊</b>",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🍁𝐉𝐎𝐈𝐍 𝐇𝐄𝐑𝐄🦋", url="https://t.me/SAM_DUB_LEZHa")]]
        ),
        disable_web_page_preview=True,
        parse_mode="html"
    )

# DC Info Handler
@StreamBot.on_message(filters.regex(r"(?i)^dc$"))
async def send_dc(bot, message):
    dc_id = message.from_user.dc_id
    await message.reply_text(START_TEXT.format(dc_id), quote=True)

# Command List Handler
@StreamBot.on_message(filters.command("list"))
async def command_list(bot, message):
    LIST_MSG = (
        "Hi! {}\nHere is a list of all my commands:\n\n"
        "1. `start⚡️`\n2. `help📚`\n3. `login🔑`\n"
        "4. `Channel❤️`\n5. `ping📡`\n6. `status📊`\n"
        "7. `DC`\n8. `Owner😎`"
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=LIST_MSG.format(message.from_user.mention),
        parse_mode="markdown"
    )

# Ping Handler
@StreamBot.on_message(filters.regex("ping📡"))
async def ping(bot, message):
    start_t = time.time()
    msg = await message.reply_text("....")
    elapsed = (time.time() - start_t) * 1000
    await msg.edit(f"Pong!\n{elapsed:.3f} ms")

# Status Handler
@StreamBot.on_message(filters.private & filters.regex("status📊"))
async def stats(bot, message):
    uptime = readable_time(time.time() - StartTime)
    total, used, free = shutil.disk_usage('.')
    stats_text = (
        f"<b>Bot Uptime:</b> {uptime}\n"
        f"<b>Total disk space:</b> {get_readable_file_size(total)}\n"
        f"<b>Used:</b> {get_readable_file_size(used)}  "
        f"<b>Free:</b> {get_readable_file_size(free)}\n\n"
        f"📊Data Usage📊\n<b>Upload:</b> {get_readable_file_size(psutil.net_io_counters().bytes_sent)}\n"
        f"<b>Download:</b> {get_readable_file_size(psutil.net_io_counters().bytes_recv)}\n\n"
        f"<b>CPU:</b> {psutil.cpu_percent()}%  "
        f"<b>RAM:</b> {psutil.virtual_memory().percent}%  "
        f"<b>Disk:</b> {psutil.disk_usage('/').percent}%"
    )
    await message.reply_text(stats_text, parse_mode="html")

# Optionally: Start & Help Command Placeholders
@StreamBot.on_message(filters.command("start"))
async def start(bot, message):
    await message.reply_text("Hello! I'm alive and ready to help you.")

@StreamBot.on_message(filters.command("help"))
async def help_cmd(bot, message):
    await message.reply_text("Use /list to see all available commands.")

