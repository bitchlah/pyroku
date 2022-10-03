import struct
import base64

from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid


from pyrogram.types import (
	InlineKeyboardButton,
	InlineKeyboardMarkup,
	InputMediaPhoto,
	CallbackQuery
)

"""
This page gives inline anime quotes.
"""

@Client.bot.on_callback_query(filters.regex("animequote-tab"))
async def _anime_quotes(_, cb: CallbackQuery):
    await cb.edit_message_text(
        Client.quote(),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="More",
                        callback_data="animequote-tab",
                    )
                ]
            ]
        ),
    )

"""
Inline assistant page for help menu.
"""

@Client.bot.on_callback_query(filters.regex("assistant-tab"))
@Client.alert_user
async def _assistant(_, cb: CallbackQuery):
    await cb.edit_message_media(
        media=InputMediaPhoto(
            media="main/core/resources/images/nora.png", 
            caption=Client.assistant_tab_string()
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                Client.bot.BuildKeyboard(
                    (
                        ["Home", "close-tab"],
                        ["Back", "home-tab"]
                    )
                )
            ]
        )
    )

"""
This file is for closed page inline help menu.
"""

@Client.bot.on_callback_query(filters.regex("close-tab"))
@Client.alert_user
async def _close(_, cb: CallbackQuery):
    await cb.edit_message_media(
        media=InputMediaPhoto(
            media="main/core/resources/images/tron-vertical.png", 
            caption=Client.close_tab_string()
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Open",
                        callback_data="home-tab"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Delete",
                        callback_data="delete-tab"
                    )
                ]
            ]
        )
    )

"""
This file is for deleting the inline help menu.
"""

@Client.bot.on_callback_query(filters.regex("delete-tab"))
@Client.alert_user
async def delete_helpdex(_, cb: CallbackQuery):
    """ delete helpdex handler for help plugin """

    try:
        if cb.inline_message_id:
            dc_id, message_id, chat_id, query_id = struct.unpack(
                "<iiiq",
                base64.urlsafe_b64decode(
                    cb.inline_message_id + '=' * (len(cb.inline_message_id) % 4)
                )
            )

            await Client.delete_messages(
                chat_id=int(str(-100) + str(chat_id)[1:]),
                message_ids=message_id
            )
        elif not cb.inline_message_id:
            if cb.message:
                await cb.message.delete()
        else:
            await cb.answer(
                "Message Expired !",
                show_alert=True
            )

    except (PeerIdInvalid, KeyError, ValueError):
        await Client.delete_messages(
            chat_id=chat_id,
            message_ids=message_id
        )
        print(chat_id, message_id)
    except Exception as e:
        await Client.error(e)

"""
This file creates extra page tab menu in helpdex
"""

@Client.bot.on_callback_query(filters.regex("extra-tab"))
@Client.alert_user
async def _extra(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=Client.extra_tab_string(),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="• Public commands •",
                        callback_data="ubpublic-commands-tab"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Home",
                        callback_data="close-tab"
                    ),
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="home-tab"
                    )
                ]
            ]
        )
    )
    print(cb)

""".
This file creates home page of helpmenu.
"""

@Client.bot.on_callback_query(filters.regex("home-tab"))
@Client.alert_user
async def _start(_, cb: CallbackQuery):
    await cb.edit_message_media(
        media=InputMediaPhoto(media=Client.ALIVE_LOGO(), caption=Client.home_tab_string()),
        reply_markup=InlineKeyboardMarkup([
                Client.BuildKeyboard(
                    (
                        ["• Settings •", "settings-tab"],
                        ["• Plugins •", "plugins-tab"]
                    )
                ),
                Client.BuildKeyboard(
                    (
                        ["• Extra •", "extra-tab"],
                        ["• Stats •", "stats-tab"]
                    )
                ),
                Client.BuildKeyboard(([["About", "about-tab"]])),
                Client.BuildKeyboard(([["Close", "close-tab"]]))
        ]
        ),
    )

"""
This file creates the plugins page in help menu.
"""

# plugins dex
@Client.bot.on_callback_query(filters.regex("plugins-tab"))
@Client.alert_user
async def plugins_page(_, cb: CallbackQuery):
    btn = Client.HelpDex(0, Client.CMD_HELP, "navigate")
    await cb.edit_message_text(
        text=Client.plugin_tab_string(),
        reply_markup=InlineKeyboardMarkup(btn)
    )


# next page
@Client.bot.on_callback_query(filters.regex(pattern="navigate-next\((.+?)\)"))
@Client.alert_user
async def give_next_page(_, cb: CallbackQuery):
    current_page_number = int(cb.matches[0].group(1))
    btn = Client.HelpDex(current_page_number + 1, Client.CMD_HELP, "navigate")
    print(cb.matches[0])
    print(dir(cb.matches[0]))
    await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))


# previous page
@Client.bot.on_callback_query(filters.regex(pattern="navigate-prev\((.+?)\)"))
@Client.alert_user
async def give_old_page(_, cb: CallbackQuery):
    current_page_number = int(cb.matches[0].group(1))
    btn = Client.HelpDex(current_page_number - 1, Client.CMD_HELP, "navigate")
    await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))


# back from plugin dex to home
@Client.bot.on_callback_query(filters.regex(pattern="back-to-plugins-page-(.*)"))
@Client.alert_user
async def get_back(_, cb: CallbackQuery):
    page_number = int(cb.matches[0].group(1))
    btn = Client.HelpDex(page_number, Client.CMD_HELP, "navigate")
    await cb.edit_message_text(text=Client.plugin_tab_string(), reply_markup=InlineKeyboardMarkup(btn))


# plugin page information
@Client.bot.on_callback_query(filters.regex(pattern="pluginlist-(.*)"))
@Client.alert_user
async def give_plugin_cmds(_, cb: CallbackQuery):
    plugin_name, page_number = cb.matches[0].group(1).split("|", 1)
    plugs = await Client.PluginData(plugin_name)
    cmd_string = f"**PLUGIN:** {plugin_name}\n\n" + "".join(plugs)
    await cb.edit_message_text(
        cmd_string,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Back",
                        callback_data=f"back-to-plugins-page-{page_number}",
                    )
                ]
            ]
        ),
        )

"""
This file creates global commands for public users.
"""

@Client.bot.on_callback_query(filters.regex("ubpublic-commands-tab"))
@Client.alert_user
async def _public_commands(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=Client.public_tab_string(),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="extra-tab"
                    )
                ]
            ]
        )
    )





@Client.bot.on_callback_query(filters.regex("public-commands-tab"))
async def _global_commands(_, cb):
    await cb.edit_message_text(
        text=Client.public_tab_string(),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="back-to-public"
                    )
                ]
            ]
        )
    )


@Client.bot.on_callback_query(filters.regex("back-to-public"))
async def _back_to_info(_, cb):
    await cb.edit_message_text(
        text="You can use these public commands, check below.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="• View commands •",
                        callback_data="public-commands-tab"
                    )
                ]
            ]
        )
    )

"""
This file creates userbot restarting page.
"""

@Client.bot.on_callback_query(filters.regex("restart-tab"))
@Client.alert_user
async def _restart_userbot(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=Client.restart_tab_string("`Press confirm to restart.`"),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Confirm",
                        callback_data="confirm-restart-tab"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Home",
                        callback_data="close-tab"
                    ),
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="settings-tab"
                    )
                ]
            ]
        ),
    )


@Client.bot.on_callback_query(filters.regex("confirm-restart-tab"))
@Client.alert_user
async def _confirm_restart(_, cb: CallbackQuery):
    try:
        back_button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="settings-tab"
                    )
                ]
            ]
        )

        await cb.edit_message_text(
            text=Client.restart_tab_string("`Trying to restart userbot . . .`"),
            reply_markup=back_button
        )
        if not Client.heroku_app():
            await cb.edit_message_text(
                text=Client.restart_tab_string("`Heroku requirements missing (heroku - key, app name), restart manually . . .`"),
                reply_markup=back_button
            )
        else:
            res = Client.heroku_app().restart()
            text = "`Please wait 2-3 minutes to restart userbot . . .`"
            final_text = text if res else "`Failed to restart userbot, do it manually . . .`"
            await cb.edit_message_text(
                text=Client.restart_tab_string(final_text),
                reply_markup=back_button
            )
    except Exception as e:
        print(e)
        await Client.error(e)

"""
This file creates pages for settings in help menu.
"""

@Client.bot.on_callback_query(filters.regex("settings-tab"))
@Client.alert_user
async def _settings(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=Client.settings_tab_string(),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Restart bot", callback_data="restart-tab",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Shutdown bot", callback_data="shutdown-tab",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Update bot", callback_data="update-tab",
                    )
                ],
                Client.BuildKeyboard((["Home", "close-tab"], ["Back", "home-tab"])),
            ]
        ),
    )

"""
This file creates pages for userbot shutdown>
"""

@Client.bot.on_callback_query(filters.regex("shutdown-tab"))
@Client.alert_user
async def _shutdown_tron(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=Client.shutdown_tab_string("`Press confirm to shutdown userbot.`"),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Confirm",
                        callback_data="confirm-shutdown"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Home",
                        callback_data="close-tab"
                    ),
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="settings-tab"
                    )
                ]
            ]
        )
    )


@Client.bot.on_callback_query(filters.regex("confirm-shutdown"))
@Client.alert_user
async def _shutdown_core(_, cb):
    back_button=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Back",
                    callback_data="settings-tab"
                )
            ]
        ]
    )

    await cb.edit_message_text(
        text=Client.shutdown_tab_string("`Trying to shutdown userbot . . .`"),
        reply_markup=back_button
    )

    if not Client.heroku_app():
        await cb.edit_message_text(
            text=Client.shutdown_tab_string("`Failed to shutdown userbot . . .`"),
            reply_markup=back_button
        )
    else:
        res = Client.heroku_app().process_formation()["worker"].scale(0)
        process = "Successfully" if res else "Unsuccessfully"
        await cb.edit_message_text(
            text=Client.shutdown_tab_string(f"`Shutdown {process} . . .`"),
            reply_markup=back_button
        )

"""
This file creates stats page in help menu.
"""

@Client.bot.on_callback_query(filters.regex("stats-tab"))
@Client.alert_user
async def _stats(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=Client.stats_tab_string(),
        reply_markup=InlineKeyboardMarkup(
            [
                Client.BuildKeyboard((["Home", "close-tab"], ["Back", "home-tab"]))
            ]
        ),
    )

""""
This file creates pages for updating the userbot to latet versions
"""

@Client.bot.on_callback_query(filters.regex("update-tab"))
@Client.alert_user
async def _update_callback(_, cb: CallbackQuery):
    await cb.answer(
            text="This feature is not implemented yet.",
            show_alert=True
        )
