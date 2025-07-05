# (c) adarsh-goel 
from Adarsh.bot import StreamBot
from Adarsh.vars import Var
import logging
logger = logging.getLogger(name)
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

@StreamBot.on_message((filters.command("start") | filters.regex('start⚡️')) & filters.private)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ: \n\nMʏ Nᴇᴡ Fʀɪᴇɴᴅ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await b.send_message(
                    chat_id=m.chat.id,
                    text="𝓢𝓞𝓡𝓡𝓨, 𝓨𝓞𝓤 𝓐𝓡𝓔 𝓐𝓡𝓔 𝓑𝓐𝓝𝓝𝓔𝓓 𝓕𝓡𝓞𝓜 𝓤𝓢𝓘𝓝𝓖 𝓜𝓔. 𝓒ᴏɴᴛᴀᴄᴛ ᴛʜᴇ 𝓓ᴇᴠᴇʟᴏᴘᴇʀ\n\n  𝙃𝙚 𝙬𝙞𝙡𝙡 𝙝𝙚𝙡𝙥 𝙮𝙤𝙪",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await StreamBot.send_photo(
                chat_id=m.chat.id,
                photo="https://graph.org/file/4b8bf6ec079dbe5aac0cf.jpg",
                caption="<i>𝙹𝙾𝙸𝙽 𝚃𝙷𝙸𝚂 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 𝚃𝙾 𝚄𝚂𝙴 𝙼𝙴🔐</i>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
            )
            return
        except Exception:
            await b.send_message(
                chat_id=m.chat.id,
                text="<i>𝓢𝓸𝓶𝓮𝓽𝓱𝓲𝓷𝓰 𝔀𝓮𝓷𝓽 𝔀𝓻𝓸𝓷𝓰</i> <b> <a href='https://t.me/SAM_DUB_LEZHa'>CLICK HERE FOR SUPPORT </a></b>",
                disable_web_page_preview=True
            )
            return
    await StreamBot.send_photo(
        chat_id=m.chat.id,
            photo="https://graph.org/file/4b8bf6ec079dbe5aac0cf.jpg",
        caption=f'𝐇𝐢𝐢 {m.from_user.mention(style="md")}...!,\n𝐈 𝐀𝐦 𝐒𝐌𝐃 𝐅𝐢𝐥𝐞 𝐓𝐨 𝐋𝐢𝐧𝐤 𝐑𝐨𝐁𝐨𝐭 𝐅𝐨𝐫 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 𝐎𝐰𝐧𝐞𝐫𝐬 𝐨𝐧𝐥𝐲.\n𝐒𝐞𝐧𝐝 𝐌𝐞 𝐚𝐧𝐲 𝐅𝐢𝐥𝐞 𝐚𝐧𝐝 𝐠𝐞𝐭 𝐚 𝐃𝐢𝐫𝐞𝐜𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐋𝐢𝐧𝐤 𝐚𝐧𝐝 𝐒𝐭𝐫𝐞𝐚𝐦𝐛𝐥𝐞 𝐋𝐢𝐧𝐤.!',
        reply_markup=buttonz
    )


@StreamBot.on_message((filters.command("help") | filters.regex('help📚')) & filters.private)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ \n\nMʏ Nᴇᴡ Fʀɪᴇɴᴅ [{message.from_user.first_name}](tg://user?id={message.from_user.id}) Started Your Bot !!"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="<i>Sᴏʀʀʏ Sɪʀ, Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ FROM USING ᴍᴇ. Cᴏɴᴛᴀᴄᴛ ᴛʜᴇ Dᴇᴠᴇʟᴏᴘᴇʀ</i>",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await StreamBot.send_photo(
                chat_id=message.chat.id,
                photo="https://graph.org/file/4b8bf6ec079dbe5aac0cf.jpg",
                caption="𝙹𝙾𝙸𝙽 𝚂𝚄𝙿𝙿𝙾𝚁𝚃 𝙶𝚁𝙾𝚄𝙿 𝚃𝙾 𝚄𝚂𝙴 ᴛʜɪs Bᴏᴛ!\n\nDᴜᴇ ᴛᴏ Oᴠᴇʀʟᴏᴀᴅ, Oɴʟʏ Cʜᴀɴɴᴇʟ Sᴜʙsᴄʀɪʙᴇʀs ᴄᴀɴ ᴜsᴇ ᴛʜᴇ Bᴏᴛ!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🍁𝐉𝐨𝐢𝐧 𝐔𝐩𝐝𝐚𝐭𝐞 𝐂𝐡𝐚𝐧𝐧𝐞𝐥🦋", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ Wʀᴏɴɢ. Cᴏɴᴛᴀᴄᴛ ᴍᴇ [🦋𝐒𝐌𝐃_𝐎𝐰𝐧𝐞𝐫🍁](https://t.me/SMD_Owner).",
                disable_web_page_preview=True
            )
            return
    await message.reply_text(
        text=(
            "<b>Send me any file or video and I will give you streamable and download links.</b>\n"
            "<b>I also support Channels! Add me to your Channel and send media files to see magic ✨. Use /list to see all commands.</b>"
        ),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🦋𝐒𝐌𝐃_𝐎𝐰𝐧𝐞𝐫🍁", url="https://t.me/SMD_Owner")
                ],
                [
                    InlineKeyboardButton("🦋𝐒𝐨𝐮𝐫𝐜𝐞 𝐂𝐨𝐝𝐞🍁", url="https://t.me/SMD_BOTz")
                ]
            ]
        ),
            )
