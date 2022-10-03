# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import os

import asyncio
import random
from asyncio import sleep
from datetime import datetime

from pyrogram import Client, filters, raw
from pyrogram.types import Message

from PunyaAlby import *
from PunyaAlby.helpers.basic import edit_or_reply

from PunyaAlby.modules.help import *


@Client.on_message(filters.command("limit", [".", "-", "^", "!", "?"]) & filters.me)
async def spamban(client: Client, m: Message):
    await client.unblock_user("SpamBot")
    response = await client.send(
        raw.functions.messages.StartBot(
            bot=await client.resolve_peer("SpamBot"),
            peer=await client.resolve_peer("SpamBot"),
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    wait_msg = await m.reply("💈 `Memproses!`")
    await asyncio.sleep(1)
    spambot_msg = response.updates[1].message.id + 1
    status = await client.get_messages(chat_id="SpamBot", message_ids=spambot_msg)
    await wait_msg.edit_text(f"-⋟ {status.text}")


@Client.on_message(filters.command("stats", [".", "-", "^", "!", "?"]) & filters.me)
async def stats(client: Client, message: Message):
    yanto = await message.reply_text("📊 `Mengumpulkan statistik`")
    start = datetime.now()
    u = 0
    g = 0
    sg = 0
    c = 0
    b = 0
    a_chat = 0
    Meh=await client.get_me()
    group = ["supergroup", "group"]
    async for dialog in client.iter_dialogs():
        if dialog.chat.type == "private":
            u += 1
        elif dialog.chat.type == "bot":
            b += 1
        elif dialog.chat.type == "group":
            g += 1
        elif dialog.chat.type == "supergroup":
            sg += 1
            user_s = await dialog.chat.get_member(int(Meh.id))
            if user_s.status in ("creator", "administrator"):
                a_chat += 1
        elif dialog.chat.type == "channel":
            c += 1

    end = datetime.now()
    ms = (end - start).seconds
    await yanto.edit_text(
        """📊 **Statistik Saya**
**Obrolan Pribadi :** `{}`
**Grup:** `{}`
**Grup Publik:** `{}`
**Channel:** `{}`
**Admin:** `{}`
**Bot:** `{}`
**⏱ Butuh:** `{}`""".format(
            u, g, sg, c, a_chat, b, ms
        )
    )



add_command_help(
    "limit",
    [
        [".limit", "Check Limit akun Telegram anda."],
    ],
)

add_command_help(
    "stats",
    [
        [".stats", "To Check Your Account Status, how Joined Chats."],
    ],
)
