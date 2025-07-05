# (c) adarsh-goel
import os
import sys
import glob
import asyncio
import logging
import importlib
from pathlib import Path

from pyrogram import idle
from aiohttp import web

from .bot import StreamBot
from .vars import Var
from .server import web_server
from .utils.keepalive import ping_server
from Adarsh.bot.clients import initialize_clients

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

PLUGIN_PATH = "Adarsh/bot/plugins/*.py"
plugin_files = glob.glob(PLUGIN_PATH)

StreamBot.start()
loop = asyncio.get_event_loop()


async def start_services():
    print("\n------------------- Initializing Telegram Bot -------------------")
    bot_info = await StreamBot.get_me()
    StreamBot.username = bot_info.username
    print("------------------------------ DONE ------------------------------\n")

    print("---------------------- Initializing Clients ----------------------")
    await initialize_clients()
    print("------------------------------ DONE ------------------------------\n")

    print("--------------------------- Importing Plugins ---------------------------")
    for plugin_path in plugin_files:
        path_obj = Path(plugin_path)
        plugin_name = path_obj.stem
        module_path = Path(f"Adarsh/bot/plugins/{plugin_name}.py")
        import_path = f".plugins.{plugin_name}"

        spec = importlib.util.spec_from_file_location(import_path, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        sys.modules[f"Adarsh.bot.plugins.{plugin_name}"] = module
        print(f"Imported => {plugin_name}")

    if Var.ON_HEROKU:
        print("\n------------------ Starting Keep Alive Service ------------------\n")
        asyncio.create_task(ping_server())

    print("-------------------- Initializing Web Server -------------------------")
    app = web.AppRunner(await web_server())
    await app.setup()

    bind_address = "0.0.0.0" if Var.ON_HEROKU else Var.BIND_ADRESS
    site = web.TCPSite(app, bind_address, Var.PORT)
    await site.start()

    print("----------------------------- DONE ------------------------------------\n")
    print("---------------------------------------------------------------------------------------------------------")
    print("---------------------------------------------------------------------------------------------------------")
    print(" Follow me for more such exciting bots! https://github.com/adarsh-goel")
    print("---------------------------------------------------------------------------------------------------------\n")
    print("----------------------- Service Started -----------------------------------------------------------------")
    print(f"                        Bot =>> {bot_info.first_name}")
    print(f"                        Server IP =>> {bind_address}:{Var.PORT}")
    print(f"                        Owner =>> {Var.OWNER_USERNAME}")
    if Var.ON_HEROKU:
        print(f"                        App running on =>> {Var.FQDN}")
    print("---------------------------------------------------------------------------------------------------------")
    print("Give a star to my repo https://github.com/adarsh-goel/filestreambot-pro  also follow me for new bots")
    print("---------------------------------------------------------------------------------------------------------")

    await idle()


if __name__ == "__main__":
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        logging.info("----------------------- Service Stopped -----------------------")
