# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import importlib

from pyrogram import idle
from uvloop import install

from config import BOT_VER, CMD_HANDLER
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
    if bot1 and bot1.bot:
        print("Activating assistant.\n")
        response = await bot1.bot.start()
        if response:
            print("Assistant activated.\n")
            botcmd = [
                ["start", "check whether bot is on or not."],
                ["help", "Get your helpdex."],
                ["ping", "Get server response speed & uptime."],
            ]
            cmds = [x.command for x in await bot1.bot.get_bot_commands()]
            botcmdkeys = [y[0] for y in botcmd]

            if cmds != botcmdkeys:
                print("Setting bot commands.\n")
                await bot1.bot.set_bot_commands([BotCommand(y[0], y[1]) for y in botcmd])
                print("Added bot commands.\n")
        else:
            print("Assistant is not activated.\n")
    else:
        print("Assistant start unsuccessful, please check that you have given the bot token.\n")
        print("skipping assistant start !")

async def main():
    for bot in bots:
        try:
            await bot.start()
            bot.me = await bot.get_me()
            await bot.join_chat("ruangdiskusikami")
            await bot.join_chat("ruangprojects")
            try:
                await bot.send_message(
                    BOTLOG_CHATID, MSG_ON.format(BOT_VER, CMD_HANDLER)
                )
            except BaseException:
                pass
            LOGGER("PunyaAlby").info(
                f"Logged in as {bot.me.first_name} | [ {bot.me.id} ]"
            )
        except Exception as a:
            LOGGER("main").warning(a)
    LOGGER("PunyaAlby").info(f"ALBY-PYROBOT v{BOT_VER} [🔥 BERHASIL DIAKTIFKAN! 🔥]")
    if bot1 and not str(BOTLOG_CHATID).startswith("-100"):
        await create_botlog(bot1)
    if bot1 and str(BOTLOG_CHATID).startswith("-100"):
        bot1.me = await bot1.get_me()
        chat = await bot1.get_chat(BOTLOG_CHATID)
        desc = "GROUP LOGS UNTUK ALBY-PYROBOT.\n\nHARAP JANGAN KELUAR DARI GROUP INI.\n\n✨ Powered By ~ @ruangdiskusikami ✨"
        lolo = f"LOGS FOR {bot1.me.first_name}"
        if chat.description != desc:
            await bot1.set_chat_description(BOTLOG_CHATID, desc)
        if chat.title != lolo:
            await bot1.set_chat_title(BOTLOG_CHATID, lolo)
        await bot1.set_chat_photo(BOTLOG_CHATID, photo="PunyaAlby/helpers/homepage.png")
    await idle()
    await aiosession.close()


async def send_logmessage():
    await bot1.bot.send_message(
        bot1.LOG_CHAT,
        "The userbot is online now.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Support Group",
                        url="t.me/tronubsupport"
                    )
                ]
            ]
        )
    )


if __name__ == "__main__":
    LOGGER("PunyaAlby").info("Starting ALBY-PYROBOT")
    install()
    git()
    heroku()
    LOOP.run_until_complete(main())
