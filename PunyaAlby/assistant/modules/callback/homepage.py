""".
This file creates home page of helpmenu.
"""

from pyrogram import Client, filters

from pyrogram.types import (
    InlineKeyboardMarkup,
    InputMediaPhoto,
    CallbackQuery,
)






@Client.bot.on_callback_query(filters.regex("home-tab"))
@Client.alert_user
async def _start(_, cb: CallbackQuery):
    await cb.edit_message_media(
        media=InputMediaPhoto(media=Client.BotPic(), caption=Client.home_tab_string()),
        reply_markup=InlineKeyboardMarkup([
                Client.BuildKeyboard(
                    (
                        ["• Plugins •", "plugins-tab"]
                    )
                ),
                Client.BuildKeyboard(([["Close", "close-tab"]]))
        ]
        ),
    )
