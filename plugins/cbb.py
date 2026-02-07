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
from helper_func import get_message, user_edit_state, check_admin

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data

    if data == "help":
        msg_text = await get_message("HELP_TXT")
        text = msg_text.format(
            first=query.from_user.first_name,
            last=query.from_user.last_name,
            username=None if not query.from_user.username else '@' + query.from_user.username,
            mention=query.from_user.mention,
            id=query.from_user.id
        )
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
             InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data='close')]
        ])
        if query.message.media:
            await query.message.edit_caption(caption=text, reply_markup=markup)
        else:
            await query.message.edit_text(text=text, reply_markup=markup)

    elif data == "about":
        msg_text = await get_message("ABOUT_TXT")
        text = msg_text.format(
            first=query.from_user.first_name,
            last=query.from_user.last_name,
            username=None if not query.from_user.username else '@' + query.from_user.username,
            mention=query.from_user.mention,
            id=query.from_user.id
        )
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
             InlineKeyboardButton('ᴄʟᴏꜱᴇ', callback_data='close')]
        ])
        if query.message.media:
            await query.message.edit_caption(caption=text, reply_markup=markup)
        else:
            await query.message.edit_text(text=text, reply_markup=markup)

    elif data == "start":
        msg_text = await get_message("START_MSG")
        text = msg_text.format(
            first=query.from_user.first_name,
            last=query.from_user.last_name,
            username=None if not query.from_user.username else '@' + query.from_user.username,
            mention=query.from_user.mention,
            id=query.from_user.id
        )
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("⛩️ SETTINGS ⛩️", callback_data="settings")],
            [InlineKeyboardButton("📢 MAIN CHANNEL", url="https://t.me/ABANIMEOFFICIAL")],
            [InlineKeyboardButton("🌀 ONGOING ANIME", url="https://t.me/Dub_Anime_ZZ")],
            [InlineKeyboardButton("🫧 ANIME INDEX", url="https://t.me/+cQTJ2UejfY9mY2Q1")],
            [
                InlineKeyboardButton("⚠️ ABOUT ⚠️", callback_data="about"),
                InlineKeyboardButton("💰 PROMO 💰", url="https//t.me/Eren_Yeager_76")
            ]
        ])
        if query.message.media:
            await query.message.edit_caption(caption=text, reply_markup=markup)
        else:
            await query.message.edit_text(text=text, reply_markup=markup)

    elif data == "settings":
        if not await check_admin(None, client, query):
            return await query.answer("⚠️ This menu is for Admins only!", show_alert=True)

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
            f"<blockquote expandable>◈ ᴛᴏᴛᴀʟ ғᴏʀᴄᴇ sᴜʙ ᴄʜᴀɴɴᴇʟ:  {len(channels)}\n"
            f"◈ ᴛᴏᴛᴀʟ ᴀᴅᴍɪɴs:  {len(admins)}\n"
            f"◈ ᴛᴏᴛᴀʟ ʙᴀɴɴᴇᴅ ᴜsᴇʀs:  {len(banned_users)}\n"
            f"◈ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴍᴏᴅᴇ:  {auto_delete_mode}\n"
            f"◈ ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ:  {protect_content}\n"
            f"◈ ʜɪᴅᴇ ᴄᴀᴘᴛɪᴏɴ:  {hide_caption}\n"
            f"◈ ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ:  {channel_button}\n"
            f"◈ ʀᴇǫᴜᴇsᴛ ғsᴜʙ ᴍᴏᴅᴇ: {req_fsub_mode}</blockquote>"
        )

        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 TEXT SETTINGS", callback_data="text_settings")],
            [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="start")]
        ])
        if query.message.media:
            await query.message.edit_caption(caption=stats_text, reply_markup=markup)
        else:
            await query.message.edit_text(text=stats_text, reply_markup=markup)

    elif data == "text_settings":
        if not await check_admin(None, client, query):
            return await query.answer("⚠️ This menu is for Admins only!", show_alert=True)

        text = "<b>📝 Cᴜsᴛᴏᴍ Tᴇxᴛ Sᴇᴛᴛɪɴɢs</b>\n\nSelect the message you want to customize:"
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Start Msg", callback_data="set_txt_START_MSG"),
             InlineKeyboardButton("Force Sub Msg", callback_data="set_txt_FORCE_MSG")],
            [InlineKeyboardButton("About Msg", callback_data="set_txt_ABOUT_TXT"),
             InlineKeyboardButton("Help Msg", callback_data="set_txt_HELP_TXT")],
            [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="settings")]
        ])
        if query.message.media:
            await query.message.edit_caption(caption=text, reply_markup=markup)
        else:
            await query.message.edit_text(text=text, reply_markup=markup)

    elif data.startswith("set_txt_"):
        if not await check_admin(None, client, query):
            return await query.answer("⚠️ This menu is for Admins only!", show_alert=True)

        key = data.split("set_txt_")[1]
        user_id = query.from_user.id
        user_edit_state[user_id] = key

        text = f"<b>Send the new text for {key}...</b>\n\n<i>HTML is supported.</i>\n<i>Send /cancel to cancel.</i>"
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("‹ Cᴀɴᴄᴇʟ", callback_data="cancel_edit")]
        ])
        if query.message.media:
            await query.message.edit_caption(caption=text, reply_markup=markup)
        else:
            await query.message.edit_text(text=text, reply_markup=markup)

    elif data == "cancel_edit":
        user_id = query.from_user.id
        if user_id in user_edit_state:
            del user_edit_state[user_id]
        text = "<b>❌ Eᴅɪᴛɪɴɢ Cᴀɴᴄᴇʟʟᴇᴅ.</b>"
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("‹ Bᴀᴄᴋ ᴛᴏ Sᴇᴛᴛɪɴɢs", callback_data="text_settings")]
        ])
        if query.message.media:
            await query.message.edit_caption(caption=text, reply_markup=markup)
        else:
            await query.message.edit_text(text=text, reply_markup=markup)

    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

    elif data.startswith("rfs_ch_"):
        if not await check_admin(None, client, query):
            return await query.answer("⚠️ This menu is for Admins only!", show_alert=True)

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
