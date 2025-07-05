from pyrogram import Client
from convopyro import Conversation
from ..vars import Var  # Make sure your Var.py is in the parent directory

StreamBot = Client(
    name='Web Streamer',
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
    bot_token=Var.BOT_TOKEN,
    sleep_threshold=Var.SLEEP_THRESHOLD,
    workers=Var.WORKERS
)

Conversation(StreamBot)

multi_clients = {}
work_loads = {}
