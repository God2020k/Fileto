import os
import asyncio
from asyncio import TimeoutError
from urllib.parse import quote_plus

from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from yourbot.bot import StreamBot  # Adjust import paths accordingly
from yourbot.utils.database import Database
from yourbot.utils.human_readable import humanbytes
from yourbot.vars import Var
from yourbot.utils.file_properties import get_name, get_hash, get_media_file_size

db = Database(Var.DATABASE_URL, Var.name)
pass_db = Database(Var.DATABASE_URL, "ag_passwords")

MY_PASS = os.environ.get("MY_PASS", None)


async def wait_for_password(client: Client, chat_id: int, timeout=90):
    """Wait for a text message from user as password or cancel command."""
    try:
        response: Message = await client.listen(chat_id, filters=filters.text, timeout=timeout)
        return response.text if response else None
    except TimeoutError:
        return None


@StreamBot.on_message(filters.command("login") | filters.regex("login🔑"), group=4)
async def login_handler(c: Client, m: Message):
    try:
        prompt = (
            "Send me the password to login.\n\n"
            "(You can cancel anytime by sending /cancel)"
        )
        ag = await m.reply_text(prompt)

        # Wait for password or cancel
        password_msg: Message = await c.listen(m.chat.id, filters=filters.text, timeout=90)
        textp = password_msg.text.strip()

        if textp == "/cancel":
            await ag.edit("❌ Process Cancelled Successfully.")
            return

        if textp == MY_PASS:
            await pass_db.add_user_pass(m.chat.id, textp)
            await ag.edit("✅ Password accepted! You are now logged in.")
        else:
            await ag.edit("❌ Wrong password, try again.")
    except TimeoutError:
        await m.reply_text("⏰ Timeout: You didn't send the password in time. Please try /login again.")
    except Exception as e:
        print(f"Login Handler Exception: {e}")
        await m.reply_text("⚠️ An error occurred during login. Please try again later.")


@StreamBot.on_message(
    filters.private & (filters.document | filters.video | filters.audio | filters.photo),
    group=4,
)
async def private_receive_handler(c: Client, m: Message):
    try:
        # Password protection
        if MY_PASS:
            check_pass = await pass_db.get_user_pass(m.chat.id)
            if check_pass is None:
                await m.reply_text(
                    "⚠️ You must /login first.\nContact developer if you don't know the password."
                )
                return
            if check_pass != MY_PASS:
                await pass_db.delete_user(m.chat.id)
                return

        # Register new user
        if not await db.is_user_exist(m.from_user.id):
            await db.add_user(m.from_user.id)
            await c.send_message(
                Var.BIN_CHANNEL,
                f"New User Joined:\nName: [{m.from_user.first_name}](tg://user?id={m.from_user.id})",
            )

        # Check updates channel subscription
        if Var.UPDATES_CHANNEL != "None":
            try:
                member = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if member.status == "kicked":
                    await c.send_message(
                        m.chat.id,
                        "🚫 You are banned! Contact Developer for help.",
                        disable_web_page_preview=True,
                    )
                    return
            except UserNotParticipant:
                await c.send_message(
                    m.chat.id,
                    "🔐 Join the updates channel to use this bot.",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Join Now 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")]]
                    ),
                )
                return
            except Exception as e:
                await m.reply_text(f"An error occurred: {e}")
                await c.send_message(
                    m.chat.id,
                    "Something went wrong. Contact the developer.",
                    disable_web_page_preview=True,
                )
                return

        # Forward media to bin channel
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)

        # Generate streaming and download links
        file_name = quote_plus(get_name(log_msg))
        file_hash = get_hash(log_msg)
        stream_link = f"{Var.URL}watch/{log_msg.id}/{file_name}?hash={file_hash}"
        download_link = f"{Var.URL}{log_msg.id}/{file_name}?hash={file_hash}"

        # Message to user
        msg_text = (
            "<i><u>Your Link Generated</u></i>\n\n"
            "<b>📂 File Name:</b> <i>{}</i>\n"
            "<b>📦 File Size:</b> <i>{}</i>\n"
            "<b>🦋 Download Link 🔗:</b> <i>{}</i>\n"
            "<b>🦋 Stream Link 🔗:</b> <i>{}</i>\n"
            "<b>🚸 Note: Links won't expire until deleted.</b>"
        ).format(
            get_name(log_msg),
            humanbytes(get_media_file_size(m)),
            download_link,
            stream_link,
        )

        await log_msg.reply_text(
            text=(
                f"**Requested by:** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n"
                f"**User ID:** `{m.from_user.id}`\n"
                f"**Stream Link:** {stream_link}"
            ),
            disable_web_page_preview=True,
            quote=True,
        )

        await m.reply_text(
            text=msg_text,
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🦋 Stream Link 🖥", url=stream_link),
                        InlineKeyboardButton("🦋 Download Link 📥", url=download_link),
                    ],
                    [
                        InlineKeyboardButton('🧿 Watch on Telegram 🖥', web_app=WebAppInfo(url=stream_link))
                    ],
                ]
            ),
        )

        # Optional: If you want link expiry after 6 hours, uncomment below:
        # await asyncio.sleep(21600)
        # try:
        #     await log_msg.delete()
        #     await m.delete()
        # except Exception as e:
        #     print(f"Error deleting messages after expiry: {e}")

        # Optionally delete original user message immediately after processing
        await m.delete()

    except FloodWait as e:
        print(f"Sleeping for {e.x} seconds due to FloodWait")
        await asyncio.sleep(e.x)
        await c.send_message(
            Var.BIN_CHANNEL,
            text=(
                f"FloodWait of {e.x}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n"
                f"User ID: `{m.from_user.id}`"
            ),
            disable_web_page_preview=True,
        )
    except Exception as e:
        print(f"Private receive handler exception: {e}")


@StreamBot.on_message(
    filters.channel & ~filters.group & (filters.document | filters.video | filters.photo) & ~filters.forwarded,
    group=-1,
)
async def channel_receive_handler(bot: Client, broadcast: Message):
    try:
        if MY_PASS:
            check_pass = await pass_db.get_user_pass(broadcast.chat.id)
            if check_pass is None:
                await broadcast.reply_text(
                    "⚠️ Login first using /login command.\nContact developer if you don't know the password."
                )
                return
            if check_pass != MY_PASS:
                await broadcast.reply_text("❌ Wrong password, login again.")
                await pass_db.delete_user(broadcast.chat.id)
                return

        if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
            await bot.leave_chat(broadcast.chat.id)
            return

        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)

        file_name = quote_plus(get_name(log_msg))
        file_hash = get_hash(log_msg)
        stream_link = f"{Var.URL}watch/{log_msg.id}/{file_name}?hash={file_hash}"
        download_link = f"{Var.URL}{log_msg.id}/{file_name}?hash={file_hash}"

        await log_msg.reply_text(
            text=(
                f"**Channel Name:** `{broadcast.chat.title}`\n"
                f"**Channel ID:** `{broadcast.chat.id}`\n"
                f"**Request URL:** {stream_link}"
            ),
            quote=True,
        )

        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🦋 Stream Link 🖥", url=stream_link),
                        InlineKeyboardButton("🦋 Download Link 📥", url=download_link),
                    ],
                    [
                        InlineKeyboardButton('🧿 Watch on Telegram 🖥', web_app=WebAppInfo(url=stream_link))
                    ],
                ]
            ),
        )

        # Optionally delete original message after processing if you want
        # await broadcast.delete()

    except FloodWait as e:
        print(f"Sleeping for {e.x} seconds due to FloodWait")
        await asyncio.sleep(e.x)
    except Exception as e:
        print(f"Channel receive handler exception: {e}")

