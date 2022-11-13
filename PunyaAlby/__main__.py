# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import importlib
import os 
import sys
import asyncio
import warnings
from pyrogram import idle, Client
from pyrogram.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from pyrogram.errors import (
    PeerIdInvalid,
    ChannelInvalid
)

from config import BOT_VER, CMD_HANDLER
from PunyaAlby.userbot.client import app
from PunyaAlby import BOTLOG_CHATID, LOGGER, LOOP, aiosession, bot1, bots
from PunyaAlby.helpers.misc import create_botlog, git, heroku

MSG_ON = """
**ALBY-PYROBOT DIAKTIFKAN**📍
      (\︵/) 
　⫺( •ᆺ•)⫹ 
┏━∪ ━━━━━━━
➠ **Userbot Version -** `{}`
➠ **Ketik** `{}alby` **untuk Mengecheck Bot**
┗━━━━━━━━━
"""

async def start_assistant():
    """ this function starts the pyrogram bot client. """
    if app and app.bot:
        print("Activating assistant.\n")
        response = await app.bot.start()
        if response:
            print("Assistant activated.\n")
            botcmd = [
                ["start", "check whether bot is on or not."],
                ["help", "Get your helpdex."],
                ["ping", "Get server response speed & uptime."],
            ]
            cmds = [x.command for x in await app.bot.get_bot_commands()]
            botcmdkeys = [y[0] for y in botcmd]

            if cmds != botcmdkeys:
                print("Setting bot commands.\n")
                await app.bot.set_bot_commands([BotCommand(y[0], y[1]) for y in botcmd])
                print("Added bot commands.\n")
        else:
            print("Assistant is not activated.\n")
    else:
        print("Assistant start unsuccessful, please check that you have given the bot token.\n")
        print("skipping assistant start !")



async def start_userbot():
    """ this function starts the pyrogram userbot client. """
    if app:
        print("Activating userbot.\n")
        response = await app.start()
        if response:
            print("Userbot activated.\n")
        else:
            print("Userbot is not activated.\n")
    else:
        print("Userbot startup unsuccessful, please check everything again ...")
        print("Quiting ...")
        sys.exit()


async def main():
    for bot in bots:
        try:
            await bot.start()
            bot.me = await bot.get_me()
            await bot.join_chat("ruangdiskusikami")
            await bot.join_chat("ruangprojects")
            await bot.join_chat("PYROALBY")
            await bot.send_message(BOTLOG_CHATID, MSG_ON.format(BOT_VER, CMD_HANDLER))
            LOGGER("PunyaAlby").info(
                f"Logged in as {bot.me.first_name} | [ {bot.me.id} ]"
            )
        except Exception as a:
            LOGGER("main").warning(a)
    LOGGER("PunyaAlby").info(f"ALBY-PYROBOT v{BOT_VER} [🔥 BERHASIL DIAKTIFKAN! 🔥]")
    await idle()
    await aiosession.close()


async def send_logmessage():
    await app.bot.send_message(
        app.BOTLOG_CHATID,
        "The userbot is online now.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Support Group",
                        url="t.me/ruangdiskusikami"
                    )
                ]
            ]
        )
    )



async def start_bot():
    """ This is the main startup function to start both clients i.e assistant & userbot.
    It also imports modules & plugins for assistant bot & userbot. """

    print(20*"_" + ". Welcome to ALBY PYROBOT." + "_"*20 + "\n\n\n")
    print("PLUGINS: Installing.\n\n")
    botplugins = app.import_module("punyaalby/assistant/modules/plugins/", exclude=app.NoLoad())
    app.import_module("punyaalby/assistant/modules/callbacks/", display_module=False)
    app.import_module("punyaalby/assistant/modules/inlinequeries/", display_module=False)
    print(f"\n\n{botplugins} plugins Loaded\n\n")
    print("MODULES: Installing.\n\n")
    plugins = app.import_module("punyaalby/modules/", exclude=app.NoLoad())
    print(f"\n\n{plugins} modules Loaded\n\n")
    await start_assistant()
    await start_userbot()
    print("You successfully deployed ALBY PYROBOT, try .ping or .alive commands to test it.")

    try:
        await send_logmessage()
    except (ChannelInvalid, PeerIdInvalid):
        try:
            await app.get_chat(app.BOTLOG_CHATID)
            await app.send_message(
                app.BOTLOG_CHATID,
                "The userbot is online now."
            )
        except PeerIdInvalid:
            pass

    await idle() # block execution

if __name__ == "__main__":
    LOGGER("PunyaAlby").info("Starting ALBY-PYROBOT")
    with warnings.catch_warnings(): # suppress DeprecationWarning
        warnings.simplefilter("ignore")
        loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
    LOOP.run_until_complete(main())
