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
