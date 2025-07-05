# (c) Adarsh-Goel
import os
import asyncio
from asyncio import TimeoutError
from urllib.parse import quote_plus

from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Adarsh.bot import StreamBot
from Adarsh.utils.database import Database
from Adarsh.utils.human_readable import humanbytes
from Adarsh.vars import Var
from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size

db = Database(Var.DATABASE_URL, Var.name)
pass_db = Database(Var.DATABASE_URL, "ag_passwords")

MY_PASS = os.environ.get("MY_PASS", None)


async def wait_for_password(client: Client, chat_id: int, timeout=90):
    """
    Wait for the next text message from the user as a password.
    Times out after `timeout` seconds.
    """
    try:
        # Wait for the next text message in the same chat
        response: Message = await client.listen(chat_id, filters=filters.text, timeout=timeout)
        return response.text if response else None
    except TimeoutError:
        return None


@StreamBot.on_message(filters.command("login") | filters.regex("login🔑"), group=4)
async def login_handler(c: Client, m: Message):
    try:
        prompt = (
            "Now send me password.\n\n"
            "𝚃𝚑𝚒𝚜 𝚒𝚜 ᴏᴜʀ ᴏғғɪᴄɪᴀʟ (TDM) 𝚙𝚛𝚒𝚟𝚊𝚝𝚎 Aᴅᴍɪɴ's 𝚋𝚘ᴛ. "
            "Fᴏʀ 𝙾𝚝𝚑𝚎𝚛 𝚞𝚜𝚎𝚛𝚜 ᴋɪɴᴅʟʏ ᴜsᴇ ᴛʜɪs Fʀᴇᴇ Bᴏᴛ 🤖👉  @TDM_PUB_Files_Streaming_bot 🥰.\n\n"
            "(You can use /cancel command to cancel the process)"
        )
        ag = await m.reply_text(prompt)

        # Wait for password message or cancel
        try:
            password_msg: Message = await c.listen(m.chat.id, filters=filters.text, timeout=90)
        except TimeoutError:
            await ag.edit("⏰ Timeout: You didn't send the password in time. Please try /login again.")
            return

        textp = password_msg.text

        if textp == "/cancel":
            await ag.edit("❌ Process Cancelled Successfully.")
            return

        if textp == MY_PASS:
            await pass_db.add_user_pass(m.chat.id, textp)
            await ag.edit("✅ Password accepted! You are now logged in.")
        else:
            await ag.edit("❌ Wrong password, try again.")
    except Exception as e:
        print(f"Login Handler Exception: {e}")


@StreamBot.on_message(
    filters.private & (filters.document | filters.video | filters.audio | filters.photo),
    group=4,
)
async def private_receive_handler(c: Client, m: Message):
    try:
        # Password protection check
        if MY_PASS:
            check_pass = await pass_db.get_user_pass(m.chat.id)
            if check_pass is None:
                await m.reply_text(
                    "⚠️ You must /login first.\nDon't know the password? Request it from the Developer."
                )
                return
            if check_pass != MY_PASS:
                await pass_db.delete_user(m.chat.id)
                return

        # Add new user to DB if not exists
        if not await db.is_user_exist(m.from_user.id):
            await db.add_user(m.from_user.id)
            await c.send_message(
                Var.BIN_CHANNEL,
                f"New User Joined! : \n\n"
                f"Name : [{m.from_user.first_name}](tg://user?id={m.from_user.id}) started your bot!"
            )

        # Check subscription to updates channel if set
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await c.send_message(
                        m.chat.id,
                        "🚫 You are banned!\n\n"
                        "**Contact Developer [TDM Admin](https://t.me/Sagastae) for help**",
                        disable_web_page_preview=True,
                    )
                    return
            except UserNotParticipant:
                await c.send_message(
                    m.chat.id,
                    "<i>🔐 Join the updates channel to use me.</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Join Now 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")]]
                    ),
                )
                return
            except Exception as e:
                await m.reply_text(f"An error occurred: {e}")
                await c.send_message(
                    m.chat.id,
                    "**Something went wrong. Contact my boss** "
                    "[🦋𝐒𝐌𝐃_𝐎𝐰𝐧𝐞𝐫🍁](https://t.me/SMD_Owner)",
                    disable_web_page_preview=True,
                )
                return

        # Forward media to bin channel
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)

        # Generate links
        file_name = quote_plus(get_name(log_msg))
        file_hash = get_hash(log_msg)
        stream_link = f"{Var.URL}watch/{log_msg.id}/{file_name}?hash={file_hash}"
        online_link = f"{Var.URL}{log_msg.id}/{file_name}?hash={file_hash}"

        msg_text = (
            "<i><u>Your Link Generated</u></i>\n\n"
            "<b>📂 File Name:</b> <i>{}</i>\n\n"
            "<b>📦 File Size:</b> <i>{}</i>\n\n"
            "<b>🦋 Download Link 🔗:</b> <i>{}</i>\n\n"
            "<b>🦋 Stream Link 🔗:</b> <i>{}</i>\n\n"
            "<b>🚸 Note: Link won't expire until I delete it.</b>"
        ).format(
            get_name(log_msg),
            humanbytes(get_media_file_size(m)),
            online_link,
            stream_link,
        )

        await log_msg.reply_text(
            text=f"**Requested by:** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n"
                 f"**User ID:** `{m.from_user.id}`\n"
                 f"**Stream Link:** {stream_link}",
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
                        InlineKeyboardButton("🦋 Download Link 📥", url=online_link),
                    ]
                ]
            ),
        )

    except FloodWait as e:
        print(f"Sleeping for {e.x} seconds due to FloodWait")
        await asyncio.sleep(e.x)
        await c.send_message(
            Var.BIN_CHANNEL,
            text=(
                f"GOT FLOODWAIT OF {e.x}s FROM [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n"
                f"User ID: `{m.from_user.id}`"
            ),
            disable_web_page_preview=True,
        )
    except Exception as e:
        print(f"Private Receive Handler Exception: {e}")


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
                    "⚠️ Login first using /login command.\nDon't know the password? Request it from developer!"
                )
                return
            if check_pass != MY_PASS:
                await broadcast.reply_text("❌ Wrong password, login again.")
                await pass_db.delete_user(broadcast.chat.id)
                return

        if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
            await bot.leave_chat(broadcast.chat.id)
            return

        # Forward media to bin channel
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)

        file_name = quote_plus(get_name(log_msg))
        file_hash = get_hash(log_msg)
        stream_link = f"{Var.URL}watch/{log_msg.id}/{file_name}?hash={file_hash}"
        online_link = f"{Var.URL}{log_msg.id}/{file_name}?hash={file_hash}"

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
                        InlineKeyboardButton("🦋 Download Link 📥", url=online_link),
                    ]
                ]
            ),
        )

    except FloodWait as e:
        print(f"Sleeping for {e.x} seconds due to FloodWait")
        await asyncio.sleep(e.x)
        await bot.send_message(
            Var.BIN_CHANNEL,
            text=(
                f"GOT FLOODWAIT OF {e.x}s FROM {broadcast.chat.title}\n\n"
                f"CHANNEL ID: `{broadcast.chat.id}`"
            ),
            disable_web_page_preview=True,
        )
    except Exception as e:
        await bot.send_message(
            Var.BIN_CHANNEL,
            text=f"**#ERROR_TRACEBACK:** `{e}`",
            disable_web_page_preview=True,
        )
        print(f"Can't edit broadcast message! Error: {e}\nMake sure bot has edit permissions in updates and bin channels.")
