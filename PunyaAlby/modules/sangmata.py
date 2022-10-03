# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio

from pyrogram import *
from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.types import *

from PunyaAlby.helpers.basic import edit_or_reply

from PunyaAlby.modules.help import *


@Client.on_message(filters.command(["sg", "sa", "sangmata"], [".", "-", "^", "!", "?"]) & filters.me)
async def sg(client: Client, message: Message):
    lol = await message.reply("💈 `Harap Tunggu, kontol!`")
    if not message.reply_to_message:
        await lol.edit("reply to any message")
    reply = message.reply_to_message
    if not reply.text:
        await lol.edit("reply to any text message")
    chat = message.chat.id
    try:
        await client.send_message("@SangMataInfo_bot", "/start")
    except RPCError:
        await lol.edit("Please unblock @SangMataInfo_bot and try again")
        return
    await reply.forward("@SangMataInfo_bot")
    await asyncio.sleep(2)
    async for opt in client.iter_history("@SangMataInfo_bot", limit=2):
        hmm = opt.text
        if hmm.startswith("Forward"):
            await lol.edit("Bisakah Anda menonaktifkan pengaturan privasi Anda untuk selamanya?")
            return
        else:
            await lol.delete()
            await opt.copy(chat)


add_command_help(
    "sangmata",
    [
        [".sg", "Balas ke pengguna untuk menemukan riwayat nama."],
    ],
)
