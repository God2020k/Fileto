import asyncio
import logging
from pyrogram import Client
from ..vars import Var
from Adarsh.utils.config_parser import TokenParser
from . import multi_clients, work_loads, StreamBot


async def initialize_clients():
    multi_clients[0] = StreamBot
    work_loads[0] = 0

    all_tokens = TokenParser().parse_from_env()
    if not all_tokens:
        logging.info("No additional clients found, using default client")
        return

    async def start_client(client_id, token):
        try:
            logging.info(f"Starting - Client {client_id}")
            if client_id == len(all_tokens):
                await asyncio.sleep(2)
                logging.info("This will take some time, please wait...")
            client = await Client(
                name=str(client_id),
                api_id=Var.API_ID,
                api_hash=Var.API_HASH,
                bot_token=token,
                sleep_threshold=Var.SLEEP_THRESHOLD,
                no_updates=True,
                in_memory=True
            ).start()
            work_loads[client_id] = 0
            return client_id, client
        except Exception:
            logging.error(f"Failed starting Client - {client_id}", exc_info=True)
            return None

    results = await asyncio.gather(*[start_client(i, token) for i, token in all_tokens.items()])

    # Filter out failed clients (None)
    clients = {client_id: client for client_id, client in results if client is not None}
    multi_clients.update(clients)

    if len(multi_clients) > 1:
        Var.MULTI_CLIENT = True
        logging.info("Multi-Client Mode Enabled")
    else:
        logging.info("No additional clients were initialized, using default client")
