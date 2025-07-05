from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from pyrogram.raw.functions.help import GetNearestDc
from Adarsh.bot import StreamBot  # Import your main bot client

# ───────────────────────────────────────────────────────────────
# Telegram DC Info Command
@StreamBot.on_callback_query(filters.regex("^dc$"))
async def dc_handler(client: Client, query: CallbackQuery):
    try:
        dc_info = await client.invoke(GetNearestDc())
        await query.answer(
            f"📍 Nearest DC: {dc_info.nearest_dc}\n🌐 Current DC: {dc_info.this_dc}",
            show_alert=True
        )
    except Exception as e:
        await query.answer("❌ Unable to fetch DC info.", show_alert=True)
        
# ───────────────────────────────────────────────────────────────
# Ping Handler

@StreamBot.on_callback_query(filters.regex("^ping$"))
async def ping_handler(client: Client, query: CallbackQuery):
    try:
        await query.answer("🏓 Pong! Bot is alive and responding.", show_alert=True)
    except Exception as e:
        await query.answer("⚠️ Ping failed.", show_alert=True)
# ───────────────────────────────────────────────────────────────
# Bot Status Handler
@StreamBot.on_message(filters.regex("status📊"))
async def bot_status(client, message):
    try:
        uptime = readable_time(time.time() - StartTime)
        total, used, free = shutil.disk_usage(".")
        total = get_readable_file_size(total)
        used = get_readable_file_size(used)
        free = get_readable_file_size(free)
        sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
        recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent

        msg = (
            f"<b>🤖 Bot Uptime:</b> {uptime}\n"
            f"<b>💾 Disk Space:</b>\n"
            f"Total: {total} | Used: {used} | Free: {free}\n\n"
            f"<b>📡 Network:</b>\n"
            f"Upload: {sent} | Download: {recv}\n\n"
            f"<b>📊 System Usage:</b>\n"
            f"CPU: {cpu}% | RAM: {ram}% | Disk: {disk}%"
        )

InlineKeyboardMarkup([
    [
        InlineKeyboardButton("DC", callback_data="dc"),
        InlineKeyboardButton("ping📡", callback_data="ping"),
        InlineKeyboardButton("status📊", callback_data="status"),
    ]
])
