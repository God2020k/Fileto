from Adarsh.bot import StreamBot
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import shutil
import psutil
from utils_bot import get_readable_file_size, readable_time
from Adarsh import StartTime


# ───────────────────────────────────────────────────────────────
# Telegram DC Info Command
@StreamBot.on_message(filters.regex("DC"))
async def dc_info(client, message):
    dc_id = getattr(message.from_user, "dc_id", "Unavailable")
    await message.reply_text(
        f"Your Telegram DC Is: `{dc_id}`",
        disable_web_page_preview=True,
        quote=True
    )


# ───────────────────────────────────────────────────────────────
# Owner Info Command
@StreamBot.on_message(filters.regex("Owner😎"))
async def owner_info(client, message):
    await message.reply_text(
        "This bot is created and maintained by the Developer.",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/Your_Developer_Username")
            ],
            [
                InlineKeyboardButton("💬 Support Chat", url="https://t.me/YourSupportGroup")
            ]
        ]),
        disable_web_page_preview=True
    )


# ───────────────────────────────────────────────────────────────
# Channel Info Command
@StreamBot.on_message(filters.regex("Channel❤️"))
async def channel_info(client, message):
    await message.reply_text(
        "<b>Join our official channel for updates and support!</b>",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📢 Join Channel", url="https://t.me/Your_Channel_Link")
            ]
        ]),
        disable_web_page_preview=True
    )


# ───────────────────────────────────────────────────────────────
# Command List Handler
@StreamBot.on_message(filters.command("list"))
async def command_list(client, message):
    user = message.from_user
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    list_msg = (
        f"Hi {mention}, here are all my commands:\n\n"
        "1. `start⚡️` – Start the bot\n"
        "2. `help📚` – Show help info\n"
        "3. `login🔑` – Login\n"
        "4. `Channel❤️` – Join the channel\n"
        "5. `ping📡` – Check latency\n"
        "6. `status📊` – Bot system status\n"
        "7. `DC` – Your Telegram data center ID\n"
        "8. `Owner😎` – Contact developer"
    )
    await message.reply_text(list_msg, parse_mode="Markdown")


# ───────────────────────────────────────────────────────────────
# Ping Handler
@StreamBot.on_message(filters.regex("ping📡"))
async def ping_handler(client, message):
    start = time.time()
    reply = await message.reply_text("Pinging...")
    latency = (time.time() - start) * 1000
    await reply.edit_text(f"🏓 Pong!\nLatency: `{latency:.3f} ms`", parse_mode="Markdown")


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
        await message.reply_text(msg)
    except Exception as e:
        await message.reply_text(f"❌ Error:\n`{str(e)}`", parse_mode="Markdown")
