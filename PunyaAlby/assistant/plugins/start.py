import time

from pyrogram import filters, Client
from pyrogram.types import Message




@Client.bot.on_message(filters.command("start"), group=-1)
async def send_response(_, m: Message):
    await m.reply("How can i help you ?")



@Client.bot.on_message(filters.new_chat_members & filters.group, group=1)
async def added_to_group_msg(_, m: Message):
    if m.new_chat_members[0].is_self:
        try:
            await Client.bot.send_message(
                m.chat.id,
                "Thank You for adding me in this group !\nUse /help to know my features."
            )
        except Exception as e:
            await Client.error(m, e)
    else:
        return
