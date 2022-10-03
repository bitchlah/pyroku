import asyncio
import random
from asyncio import sleep                                                                                               
from pyrogram import Client, filters
from pyrogram.types import *
from pyrogram.errors import RPCError
from pyrogram.errors import PeerIdInvalid 
from PunyaAlby.helpers.tools import get_arg


@Client.on_message(filters.command("tt", [".", "-", "^", "!", "?"]) & filters.me)
async def tiktok(client: Client, message: Message):
    Cilik = await message.reply("`📥 Downloading...`")
    link = get_arg(message)
    chat = message.chat.id
    idk = message.from_user.first_name
    to = message.from_user.id
    bot = "SaveAsbot" 
    if Cilik:
        try:
            await client.send_message(bot, link)
            await asyncio.sleep(5)
        except RPCError:  
            return await Cilik.edit("`Silahkan buka blockir @SaveAsbot lalu coba lagi`")
    async for kontol in client.search_messages(bot, filter="video", limit=1):
        await client.send_video(chat, video=kontol.video.file_id, caption=f"📌 **Uploaded by:** [{idk}](tg://user?id={to})")
        await Cilik.delete()
        await kontol.delete()
