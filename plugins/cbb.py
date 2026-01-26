#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import Client 
from bot import Bot
from config import *
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import *

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data

    if data == "help":
        await query.message.edit_caption(
            caption=HELP_TXT.format(first=query.from_user.first_name),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                 InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data='close')]
            ])
        )

    elif data == "about":
        await query.message.edit_caption(
            caption=ABOUT_TXT.format(first=query.from_user.first_name),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                 InlineKeyboardButton('ᴄʟᴏꜱᴇ', callback_data='close')]
            ])
        )

    elif data == "start":
        await query.message.edit_caption(
            caption=START_MSG.format(
                first=query.from_user.first_name,
                last=query.from_user.last_name,
                username=None if not query.from_user.username else '@' + query.from_user.username,
                mention=query.from_user.mention,
                id=query.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⛩️ SETTINGS ⛩️", callback_data="settings")],
                [InlineKeyboardButton("📢 MAIN CHANNEL", url="https://t.me/SECRECT_BOT_UPDATES")],
                [InlineKeyboardButton("🌀 ONGOING ANIME", url="https://t.me/SECRECT_BOT_UPDATES")],
                [InlineKeyboardButton("🫧 ANIME INDEX", url="https://t.me/SECRECT_BOT_UPDATES")],
                [
                    InlineKeyboardButton("⚠️ ABOUT ⚠️", callback_data="about"),
                    InlineKeyboardButton("💰 PROMO 💰", url="https://t.me/Lord_Vasudev_Krishna")
                ]
            ])
        )

    elif data == "settings":
        channels = await db.show_channels()
        admins = await db.get_all_admins()
        banned_users = await db.get_ban_users()
        del_timer = await db.get_del_timer()

        auto_delete_mode = "Eɴᴀʙʟᴇᴅ" if del_timer > 0 else "Dɪsᴀʙʟᴇᴅ"
        protect_content = "Eɴᴀʙʟᴇᴅ" if PROTECT_CONTENT else "Dɪsᴀʙʟᴇᴅ"
        hide_caption = "Eɴᴀʙʟᴇᴅ" if CUSTOM_CAPTION else "Dɪsᴀʙʟᴇᴅ"
        channel_button = "Eɴᴀʙʟᴇᴅ" if not DISABLE_CHANNEL_BUTTON else "Dɪsᴀʙʟᴇᴅ"

        req_fsub_mode = "Dɪsᴀʙʟᴇᴅ"
        if channels:
            for cid in channels:
                 mode = await db.get_channel_mode(cid)
                 if mode == 'on':
                     req_fsub_mode = "Eɴᴀʙʟᴇᴅ"
                     break

        stats_text = (
            "<b>⚙️ Cᴏɴғɪɢᴜʀᴀᴛɪᴏɴs</b>\n"
            f"◈ ᴛᴏᴛᴀʟ ғᴏʀᴄᴇ sᴜʙ ᴄʜᴀɴɴᴇʟ:  {len(channels)}\n"
            f"◈ ᴛᴏᴛᴀʟ ᴀᴅᴍɪɴs:  {len(admins)}\n"
            f"◈ ᴛᴏᴛᴀʟ ʙᴀɴɴᴇᴅ ᴜsᴇʀs:  {len(banned_users)}\n"
            f"◈ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴍᴏᴅᴇ:  {auto_delete_mode}\n"
            f"◈ ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ:  {protect_content}\n"
            f"◈ ʜɪᴅᴇ ᴄᴀᴘᴛɪᴏɴ:  {hide_caption}\n"
            f"◈ ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ:  {channel_button}\n"
            f"◈ ʀᴇǫᴜᴇsᴛ ғsᴜʙ ᴍᴏᴅᴇ: {req_fsub_mode}"
        )

        await query.message.edit_caption(
            caption=stats_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="start")]
            ])
        )

    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

    elif data.startswith("rfs_ch_"):
        cid = int(data.split("_")[2])
        try:
            chat = await client.get_chat(cid)
            mode = await db.get_channel_mode(cid)
            status = "🟢 ᴏɴ" if mode == "on" else "🔴 ᴏғғ"
            new_mode = "ᴏғғ" if mode == "on" else "on"
            buttons = [
                [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
                [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
            ]
            await query.message.edit_text(
                f"Channel: {chat.title}\nCurrent Force-Sub Mode: {status}",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception:
            await query.answer("Failed to fetch channel info", show_alert=True)

    elif data.startswith("rfs_toggle_"):
        cid, action = data.split("_")[2:]
        cid = int(cid)
        mode = "on" if action == "on" else "off"

        await db.set_channel_mode(cid, mode)
        await query.answer(f"Force-Sub set to {'ON' if mode == 'on' else 'OFF'}")

        # Refresh the same channel's mode view
        chat = await client.get_chat(cid)
        status = "🟢 ON" if mode == "on" else "🔴 OFF"
        new_mode = "off" if mode == "on" else "on"
        buttons = [
            [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
            [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
        ]
        await query.message.edit_text(
            f"Channel: {chat.title}\nCurrent Force-Sub Mode: {status}",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data == "fsub_back":
        channels = await db.show_channels()
        buttons = []
        for cid in channels:
            try:
                chat = await client.get_chat(cid)
                mode = await db.get_channel_mode(cid)
                status = "🟢" if mode == "on" else "🔴"
                buttons.append([InlineKeyboardButton(f"{status} {chat.title}", callback_data=f"rfs_ch_{cid}")])
            except:
                continue

        await query.message.edit_text(
            "sᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴛᴏɢɢʟᴇ ɪᴛs ғᴏʀᴄᴇ-sᴜʙ ᴍᴏᴅᴇ:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
