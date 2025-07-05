from Adarsh.bot import StreamBot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters
import time
import shutil
import psutil

from utils_bot import get_readable_file_size, readable_time
from Adarsh import StartTime

START_TEXT = "Your Telegram DC Is : `{}`"

# Owner Button Handler
@StreamBot.on_message(filters.regex(r"Owner😎"))
async def owner_handler(client, message):
    await message.reply(
        text="I am Coded By [SMD Admin](@SMD_Owner)",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🦋𝐒𝐌𝐃_𝐎𝐰𝐧𝐞𝐫🍁", url="https://t.me/SMD_Owner")]
        ]),
        disable_web_page_preview=True
    )

# Channel Button Handler
@StreamBot.on_message(filters.regex(r"Channel❤️"))
async def channel_handler(client, message):
    await message.reply(
        text="<b>𝐇𝐄𝐑𝐄'𝐒 𝐓𝐇𝐄 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝐋𝐈𝐍𝐊</b>",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🍁𝐉𝐎𝐈𝐍 𝐇𝐄𝐑𝐄🦋", url="https://t.me/SAM_DUB_LEZHa")]
        ]),
        disable_web_page_preview=True
    )

# Get Telegram DC ID
@StreamBot.on_message(filters.regex(r"DC"))
async def dc_handler(client, message):
    dc_id = message.from_user.dc_id
    await message.reply_text(
        text=START_TEXT.format(dc_id),
        disable_web_page_preview=True,
        quote=True
    )

# List All Commands
@StreamBot.on_message(filters.command("list"))
async def list_handler(client, message):
    LIST_MSG = (
        "Hi! {} 👋\n\n"
        "Here's a list of all my available commands:\n\n"
        "1. `start⚡️`\n"
        "2. `help📚`\n"
        "3. `login🔑`\n"
        "4. `Channel❤️`\n"
        "5. `ping📡`\n"
        "6. `status📊`\n"
        "7. `DC`\n"
        "8. `Owner😎`"
    )
    await message.reply_text(
        LIST_MSG.format(message.from_user.mention(style="md"))
    )

# Ping Command
@StreamBot.on_message(filters.regex(r"ping📡"))
async def ping_handler(client, message):
    start_time = time.time()
    temp = await message.reply("Pinging...")
    end_time = time.time()
    ping_time = (end_time - start_time) * 1000
    await temp.edit(f"🏓 Pong! `{ping_time:.3f} ms`")

# Status Command
@StreamBot.on_message(filters.private & filters.regex(r"status📊"))
async def status_handler(client, message):
    uptime = readable_time(time.time() - StartTime)

    total, used, free = shutil.disk_usage(".")
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)

    net = psutil.net_io_counters()
    sent = get_readable_file_size(net.bytes_sent)
    recv = get_readable_file_size(net.bytes_recv)

    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    stats_text = (
        f"<b>🤖 Bot Uptime:</b> {uptime}\n"
        f"<b>💾 Disk Space:</b> {total}\n"
        f"<b>📂 Used:</b> {used} | <b>Free:</b> {free}\n\n"
        f"<b>📊 Data Usage:</b>\n"
        f"⇪ Upload: {sent}\n"
        f"⇩ Download: {recv}\n\n"
        f"<b>🧠 CPU:</b> {cpu}% | <b>RAM:</b> {ram}% | <b>Disk:</b> {disk}%"
    )

    await message.reply_text(stats_text, disable_web_page_preview=True)
