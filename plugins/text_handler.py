from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from database.database import db
from helper_func import user_edit_state

async def is_editing_filter(_, __, message):
    return message.from_user and message.from_user.id in user_edit_state

editing_state = filters.create(is_editing_filter)

@Bot.on_message(filters.private & editing_state & filters.text)
async def handle_text_settings(client: Client, message: Message):
    user_id = message.from_user.id
    key = user_edit_state[user_id]

    if message.text.startswith("/cancel"):
        del user_edit_state[user_id]
        await message.reply("❌ Editing cancelled.", quote=True)
        return

    # Use raw text to allow users to write their own HTML tags.
    # If they use telegram formatting, they should copy-paste raw html or write tags.
    text_to_save = message.text

    # Validate format string
    try:
        text_to_save.format(
            first="Firstname",
            last="Lastname",
            username="@username",
            mention="User",
            id=123456789
        )
    except Exception as e:
        await message.reply(
            f"<b>❌ Invalid Format!</b>\n\n"
            f"Your text contains invalid placeholders or syntax.\n"
            f"Allowed placeholders: <code>{{first}}</code>, <code>{{last}}</code>, <code>{{username}}</code>, <code>{{mention}}</code>, <code>{{id}}</code>\n\n"
            f"Error: <code>{e}</code>",
            quote=True
        )
        return

    # Enforce collapsible quotes
    if not text_to_save.startswith("<blockquote expandable>"):
        text_to_save = f"<blockquote expandable><b>{text_to_save}</b></blockquote>"

    try:
        await db.set_config_text(key, text_to_save)
        del user_edit_state[user_id]

        await message.reply(
            f"<b>✅ {key} updated successfully!</b>\n\nNew value:\n<code>{text_to_save}</code>",
            quote=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("‹ Bᴀᴄᴋ ᴛᴏ Sᴇᴛᴛɪɴɢs", callback_data="text_settings")]
            ])
        )
    except Exception as e:
        await message.reply(f"<b>Error saving text:</b> {e}")
