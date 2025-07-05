from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import shutil
import psutil
from config import API_ID, API_HASH, BOT_TOKEN
from utils_bot import readable_time, get_readable_file_size

StartTime = time.time()

app = Client(
    "streambot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

START_TEXT = "Your Telegram DC is: `{}`"

@app.on_message(filters.regex("Owner😎"))
async def owner_handler(client, message):
    await message.reply(
        "I am coded by [SMD Admin](@SMD_Owner)",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🦋𝐒𝐌𝐃_𝐎𝐰𝐧𝐞𝐫🍁", url="https://t.me/SMD_Owner")]
        ]),
        disable_web_page_preview=True
    )

@app.on_message(filters.regex("Channel❤️"))
async def channel_handler(client, message):
    await message.reply(
        "<b>𝐇𝐄𝐑𝐄'𝐒 𝐓𝐇𝐄 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝐋𝐈𝐍𝐊</b>",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🍁𝐉𝐎𝐈𝐍 𝐇𝐄𝐑𝐄🦋", url="https://t.me/SAM_DUB_LEZHa")]
        ]),
        disable_web_page_preview=True
    )

@app.on_message(filters.regex("DC"))
async def dc_handler(client, message):
    dc_id = getattr(message.from_user, "dc_id", "Unavailable")
    await message.reply_text(START_TEXT.format(dc_id))

@app.on_message(filters.command("list"))
async def command_list(client, message):
    LIST_MSG = (
        f"Hi {message.from_user.mention}!\nHere is a list of all my commands:\n\n"
        "1. `start⚡️`\n"
        "2. `help📚`\n"
        "3. `login🔑`\n"
        "4. `Channel❤️`\n"
        "5. `ping📡`\n"
        "6. `status📊`\n"
        "7. `DC`\n"
        "8. `Owner😎`"
    )
    await message.reply_text(LIST_MSG)

@app.on_message(filters.regex("ping📡"))
async def ping_handler(client, message):
    start = time.time()
    reply = await message.reply_text("Pinging...")
    end = time.time()
    latency = (end - start) * 1000
    await reply.edit_text(f"Pong!\n{latency:.3f} ms")

@app.on_message(filters.private & filters.regex("status📊"))
async def status_handler(client, message):
    current_time = readable_time(time.time() - StartTime)
    total, used, free = shutil.disk_usage(".")
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    text = (
        f"<b>Bot Uptime:</b> {current_time}\n"
        f"<b>Total Disk:</b> {total}\n"
        f"<b>Used:</b> {used} | <b>Free:</b> {free}\n\n"
        f"📊 <b>Data Usage</b>\n"
        f"<b>Upload:</b> {sent}\n"
        f"<b>Download:</b> {recv}\n\n"
        f"📈 <b>Performance</b>\n"
        f"<b>CPU:</b> {cpu}%\n"
        f"<b>RAM:</b> {ram}%\n"
        f"<b>Disk:</b> {disk}%"
    )

    await message.reply_text(text)

app.run()
