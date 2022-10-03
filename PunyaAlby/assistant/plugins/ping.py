from datetime import datetime

from pyrogram import filters, Client
from pyrogram.types import Message



@Client.bot.on_message(filters.command("ping"), group=-1)
async def bot_ping(_, m: Message):
        start = datetime.now()
        msg = await Client.bot.send_message(
            m.chat.id,
            "ping"
        )
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        await msg.edit(f"Pöng !\n`{ms}`\nUptime: `{Client.uptime()}`")
