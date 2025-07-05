from Adarsh.bot import StreamBot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters
import time
import shutil, psutil
from utils_bot import *
from Adarsh import StartTime

# Message format template for the DC command
START_TEXT = """Your Telegram DC Is: `{}`"""


# ───────────────────────────────────────────────────────────────
# Handler: Owner Command Triggered By "Owner😎"
# Responds with an inline button linking to the owner's profile
@StreamBot.on_message(filters.regex("Owner😎"))
async def maintainers(bot, m):
    await bot.send_message(
        chat_id=m.chat.id,
        text="This bot was created and maintained by the Developer.",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("👨‍💻 Developer Contact", url="https://t.me/Your_Developer_Username")
            ],
            [
                InlineKeyboardButton("💬 Support Chat", url="https://t.me/YourSupportGroup")
            ]
        ]),
        disable_web_page_preview=True
    )


# ───────────────────────────────────────────────────────────────
# Handler: Channel Command Triggered By "Channel❤️"
# Sends a message with a button to join the official channel
@StreamBot.on_message(filters.regex("Channel❤️"))
async def follow_user(bot, m):
    await bot.send_message(
        chat_id=m.chat.id,
        text="<b>Join our official channel for updates and more!</b>",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📢 Join Our Channel", url="https://t.me/Your_Channel_Link")
            ]
        ]),
        disable_web_page_preview=True
    )


# ───────────────────────────────────────────────────────────────
# Handler: DC Info Triggered By "DC"
# Displays the user's Telegram data center (dc_id)
@StreamBot.on_message(filters.regex("DC"))
async def dc_info(bot, m):
    dc_id = getattr(m.from_user, "dc_id", "Unavailable")
    text = START_TEXT.format(dc_id)
    await m.reply_text(
        text=text,
        disable_web_page_preview=True,
        quote=True
    )


# ───────────────────────────────────────────────────────────────
# Handler: Command List (/list)
# Lists all commands supported by the bot
@StreamBot.on_message(filters.command("list"))
async def command_list(bot, m):
    mention = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
    LIST_MSG = f"Hi {mention}, here is a list of available commands:\n\n" \
               "1. `start⚡️` – Start the bot\n" \
               "2. `help📚` – Show help menu\n" \
               "3. `login🔑` – Login system\n" \
               "4. `Channel❤️` – Join our channel\n" \
               "5. `ping📡` – Ping bot response time\n" \
               "6. `status📊` – Show bot/server status\n" \
               "7. `DC` – Show your Telegram DC ID\n" \
               "8. `Owner😎` – Contact the developer"
    
    await m.reply_text(text=LIST_MSG, parse_mode="Markdown")


# ───────────────────────────────────────────────────────────────
# Handler: Ping Command Triggered by "ping📡"
# Responds with bot response time (latency)
@StreamBot.on_message(filters.regex("ping📡"))
async def ping(bot, m):
    start = time.time()
    response = await m.reply_text("Pinging...")
    latency = (time.time() - start) * 1000
    await response.edit(f"🏓 Pong!\nResponse Time: `{latency:.3f} ms`", parse_mode="Markdown")


# ───────────────────────────────────────────────────────────────
# Handler: Status Command Triggered by "status📊"
# Shows system and bot stats like uptime, CPU, RAM, disk, etc.
@StreamBot.on_message(filters.private & filters.regex("status📊"))
async def stats(bot, m):
    try:
        uptime = readable_time((time.time() - StartTime))
        total, used, free = shutil.disk_usage('.')
        total = get_readable_file_size(total)
        used = get_readable_file_size(used)
        free = get_readable_file_size(free)
        sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
        recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        msg = (
            f"<b>🤖 Bot Uptime:</b> {uptime}\n"
            f"<b>💾 Disk:</b> Total: {total} | Used: {used} | Free: {free}\n\n"
            f"<b>📡 Data Usage:</b>\n"
            f"Upload: {sent} | Download: {recv}\n\n"
            f"<b>📊 System Load:</b>\n"
            f"CPU: {cpu}% | RAM: {ram}% | Disk: {disk}%"
        )

        await m.reply_text(msg)
    except Exception as e:
        await m.reply_text(f"❌ Error occurred:\n`{str(e)}`", parse_mode="Markdown")
