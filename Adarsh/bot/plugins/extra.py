from Adarsh.bot import StreamBot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters
import time
import shutil, psutil
from utils_bot import *
from Adarsh import StartTime

START_TEXT = """Hi {}, welcome! Choose an option from below."""

# Inline keyboard buttons for main menu
MAIN_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("Owner😎", callback_data="owner")],
    [InlineKeyboardButton("Channel❤️", callback_data="channel")],
    [InlineKeyboardButton("DC", callback_data="dc")],
    [InlineKeyboardButton("ping📡", callback_data="ping")],
    [InlineKeyboardButton("status📊", callback_data="status")],
    [InlineKeyboardButton("List Commands", callback_data="list")]
])

@StreamBot.on_message(filters.command("start") & filters.private)
async def start_handler(bot, message):
    await message.reply_text(
        START_TEXT.format(message.from_user.first_name),
        reply_markup=MAIN_MENU
    )

@StreamBot.on_callback_query()
async def callback_handler(bot, callback_query):
    data = callback_query.data
    chat_id = callback_query.message.chat.id
    user = callback_query.from_user

    if data == "owner":
        await callback_query.answer()
        await bot.send_message(
            chat_id,
            text="I am Coded By [SMD Admin](https://t.me/SMD_Owner)",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🦋𝐒𝐌𝐃_𝐎𝐰𝐧𝐞𝐫🍁", url="https://t.me/SMD_Owner")]]
            )
        )

    elif data == "channel":
        await callback_query.answer()
        await bot.send_message(
            chat_id,
            text="<b>𝐇𝐄𝐑𝐄'𝐒 𝐓𝐇𝐄 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝐋𝐈𝐍𝐊</b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🍁𝐉𝐎𝐈𝐍 𝐇𝐄𝐑𝐄🦋", url="https://t.me/SAM_DUB_LEZHa")]]
            )
        )

    elif data == "dc":
        await callback_query.answer()
        dc_text = f"Your Telegram DC Is : {user.dc_id}"
        await bot.send_message(chat_id, text=dc_text, parse_mode="markdown")

    elif data == "ping":
        await callback_query.answer()
        start_t = time.time()
        sent_msg = await bot.send_message(chat_id, "Pinging...")
        end_t = time.time()
        ping_time = (end_t - start_t) * 1000
        await sent_msg.edit(f"Pong!\n{ping_time:.3f} ms")

    elif data == "status":
        await callback_query.answer()
        currentTime = readable_time(time.time() - StartTime)
        total, used, free = shutil.disk_usage('.')
        total = get_readable_file_size(total)
        used = get_readable_file_size(used)
        free = get_readable_file_size(free)
        sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
        recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
        cpuUsage = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        botstats = (
            f'<b>Bot Uptime:</b> {currentTime}\n'
            f'<b>Total disk space:</b> {total}\n'
            f'<b>Used:</b> {used}  <b>Free:</b> {free}\n\n'
            f'📊Data Usage📊\n<b>Upload:</b> {sent}\n'
            f'<b>Down:</b> {recv}\n\n'
            f'<b>CPU:</b> {cpuUsage}% <b>RAM:</b> {memory}% <b>Disk:</b> {disk}%'
        )
        await bot.send_message(chat_id, text=botstats)

    elif data == "list":
        await callback_query.answer()
        list_msg = (
            "Hi! {} Here is a list of all my commands:\n\n"
            "1. start⚡️\n"
            "2. help📚\n"
            "3. login🔑\n"
            "4. Channel❤️\n"
            "5. ping📡\n"
            "6. status📊\n"
            "7. DC (your telegram datacenter info)\n"
            "8. Owner😎"
        ).format(user.mention(style="md"))
        await bot.send_message(chat_id, text=list_msg)

    else:
        await callback_query.answer("Unknown command!", show_alert=True)
