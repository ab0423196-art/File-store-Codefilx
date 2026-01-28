from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot import Bot
from database.database import db
from helper_func import admin

@Bot.on_message(filters.command("extralink") & filters.private & admin)
async def add_extralink_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("<b>Usage:</b> <code>/extralink https://example.com</code>")

    url = message.command[1]

    if not url.startswith("http"):
        return await message.reply("<b>❌ Invalid URL. Must start with http or https.</b>")

    await db.add_extralink(url)
    await message.reply(f"<b>✅ Added External Link:</b>\n{url}")


@Bot.on_message(filters.command("myextralink") & filters.private & admin)
async def list_extralinks_cmd(client: Client, message: Message):
    links = await db.get_extralinks()

    if not links:
        return await message.reply("<b>❌ No external links found.</b>")

    buttons = []
    for i, url in enumerate(links):
        # Truncate url for button text
        display_url = url if len(url) < 30 else url[:27] + "..."
        buttons.append([InlineKeyboardButton(f"🗑️ {display_url}", callback_data=f"del_elink_{i}")])

    buttons.append([InlineKeyboardButton("✖️ Close", callback_data="close")])

    await message.reply(
        "<b>🔗 External Links Management</b>\n\nClick to delete:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Bot.on_callback_query(filters.regex(r"^del_elink_"), group=-1)
async def delete_extralink_cb(client: Client, callback_query: CallbackQuery):
    try:
        index = int(callback_query.data.split("_")[-1])
        links = await db.get_extralinks()

        if index < 0 or index >= len(links):
            return await callback_query.answer("❌ Link not found or already deleted.", show_alert=True)

        url_to_delete = links[index]
        await db.del_extralink(url_to_delete)

        # Refresh the list
        new_links = await db.get_extralinks()
        if not new_links:
            await callback_query.message.edit(
                "<b>🔗 External Links Management</b>\n\n❌ No external links left.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ Close", callback_data="close")]])
            )
            return await callback_query.answer("Deleted!")

        buttons = []
        for i, url in enumerate(new_links):
            display_url = url if len(url) < 30 else url[:27] + "..."
            buttons.append([InlineKeyboardButton(f"🗑️ {display_url}", callback_data=f"del_elink_{i}")])

        buttons.append([InlineKeyboardButton("✖️ Close", callback_data="close")])

        await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
        await callback_query.answer(f"Deleted: {url_to_delete}")

    except Exception as e:
        print(f"Error in delete_extralink_cb: {e}")
        await callback_query.answer("❌ Error occurred.", show_alert=True)
