from aiohttp import web
from plugins import web_server
import asyncio
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import BotCommand
import sys
from datetime import datetime
#rohit_1888 on Tg
from config import *


name ="""
 BY CODEFLIX BOTS
"""


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id = db_channel.id, text = "Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/SECRECT_BOT_UPDATES for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/SECRECT_BOT_UPDATES")
        self.LOGGER(__name__).info(f"""BOT DEPLOYED BY @Lord_Vasudev_Krishna""")

        self.set_parse_mode(ParseMode.HTML)
        self.username = usr_bot_me.username
        self.LOGGER(__name__).info(f"Bot Running..! Made by @Lord_Vasudev_Krishna")   

        try:
            await self.set_bot_commands([
                BotCommand("start", "Start the bot or get posts"),
                BotCommand("batch", "Create link for more than one posts"),
                BotCommand("custom_batch", "Create custom batch from channel/group"),
                BotCommand("genlink", "Create link for one post"),
                BotCommand("users", "View bot statistics"),
                BotCommand("broadcast", "Broadcast any messages to bot users"),
                BotCommand("dbroadcast", "Broadcast any messages with auto delete"),
                BotCommand("stats", "Check your bot uptime"),
                BotCommand("dlt_time", "Set auto delete time for files"),
                BotCommand("check_dlt_time", "Check current delete time setting"),
                BotCommand("ban", "Ban a user from using the bot"),
                BotCommand("unban", "Unban a previously banned user"),
                BotCommand("banlist", "Get list of banned users"),
                BotCommand("addchnl", "Add a channel for force subscription"),
                BotCommand("delchnl", "Remove a force subscribe channel"),
                BotCommand("listchnl", "View all added force subscribe channels"),
                BotCommand("fsub_mode", "Toggle force subscribe on or off"),
                BotCommand("pbroadcast", "Pin a broadcast to all user's chat"),
                BotCommand("add_admin", "Add a new admin"),
                BotCommand("deladmin", "Remove an admin"),
                BotCommand("admins", "List all current admins"),
                BotCommand("delreq", "Removed users that left chnl and not getting request fsub"),
                BotCommand("extralink", "Add an external link for force sub"),
                BotCommand("myextralink", "Manage external links")
            ])
            self.LOGGER(__name__).info("Bot Commands Set Successfully")
        except Exception as e:
            self.LOGGER(__name__).warning(f"Failed to set bot commands: {e}")

        # Start Web Server
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()


        try: await self.send_message(OWNER_ID, text = f"<b><blockquote> Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ by @Lord_Vasudev_Krishna</blockquote></b>")
        except: pass

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

    def run(self):
        """Run the bot."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
        self.LOGGER(__name__).info("Bot is now running. Thanks to @Lord_Vasudev_Krishna")
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            self.LOGGER(__name__).info("Shutting down...")
        finally:
            loop.run_until_complete(self.stop())

#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
