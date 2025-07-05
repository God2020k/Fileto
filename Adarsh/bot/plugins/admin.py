# (c) @adarsh-goel
import os
import time
import string
import random
import asyncio
import aiofiles
import datetime
from Adarsh.utils.broadcast_helper import send_msg
from Adarsh.utils.database import Database
from Adarsh.bot import StreamBot
from Adarsh.vars import Var
from pyrogram import filters, Client
from pyrogram.types import Message

db = Database(Var.DATABASE_URL, Var.name)
Broadcast_IDs = {}

@StreamBot.on_message(filters.command("users") & filters.private)
async def users_count_handler(c: Client, m: Message):
    user_id = m.from_user.id
    if user_id in Var.OWNER_ID:
        total_users = await db.total_users_count()
        await m.reply_text(f"Total Users in DB: {total_users}", quote=True)

@StreamBot.on_message(filters.command("broadcast") & filters.private & filters.user(list(Var.OWNER_ID)))
async def broadcast_handler(c: Client, m: Message):
    if not m.reply_to_message:
        return await m.reply_text("Please reply to the message you want to broadcast.", quote=True)

    out = await m.reply_text(
        "Broadcast initiated! You will be notified with log file when all users are notified."
    )
    
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message

    # Generate unique broadcast ID
    while True:
        broadcast_id = ''.join(random.choice(string.ascii_letters) for _ in range(6))
        if broadcast_id not in Broadcast_IDs:
            break

    start_time = time.time()
    total_users = await db.total_users_count()
    done = success = failed = 0

    Broadcast_IDs[broadcast_id] = {
        'total': total_users,
        'current': done,
        'failed': failed,
        'success': success
    }

    log_filename = f'broadcast_{broadcast_id}.txt'
    async with aiofiles.open(log_filename, 'w') as broadcast_log_file:
        async for user in all_users:
            try:
                status_code, msg = await send_msg(
                    user_id=int(user['id']),
                    message=broadcast_msg
                )
                if msg:
                    await broadcast_log_file.write(msg)
                    await broadcast_log_file.flush()  # Flush periodically

                if status_code == 200:
                    success += 1
                else:
                    failed += 1
                    if status_code == 400:
                        await db.delete_user(user['id'])
                done += 1
            except Exception as e:
                failed += 1
                done += 1
                await broadcast_log_file.write(f"Failed to send to {user['id']}: {str(e)}\n")
                await broadcast_log_file.flush()

            if broadcast_id not in Broadcast_IDs:
                # Broadcast cancelled
                break
            else:
                Broadcast_IDs[broadcast_id].update({
                    'current': done,
                    'failed': failed,
                    'success': success
                })

    # Remove broadcast ID from active list
    Broadcast_IDs.pop(broadcast_id, None)

    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    await out.delete()

    caption = (
        f"Broadcast completed in `{completed_in}`\n\n"
        f"Total users: {total_users}\n"
        f"Total done: {done}, Success: {success}, Failed: {failed}."
    )

    if failed == 0:
        await m.reply_text(caption, quote=True)
    else:
        await m.reply_document(document=log_filename, caption=caption, quote=True)

    os.remove(log_filename)
