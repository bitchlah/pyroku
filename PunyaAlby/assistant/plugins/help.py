from pyrogram import filters, Client

from pyrogram.types import (
    InlineKeyboardMarkup, 
    Message,
)


emoji = Client.HelpEmoji() or "•"

settings = Client.BuildKeyboard(([f"{emoji} Settings {emoji}", "settings-tab"], [f"{emoji} Modules {emoji}", "plugins-tab"]))
extra = Client.BuildKeyboard(([f"{emoji} Extra {emoji}", "extra-tab"], [f"{emoji} Stats {emoji}", "stats-tab"]))
about = Client.BuildKeyboard(([["Assistant", "assistant-tab"]]))
close = Client.BuildKeyboard(([["Close", "close-tab"]]))
public = Client.BuildKeyboard(([[f"{emoji} Public Commands {emoji}", "public-commands-tab"]]))





# /help command for bot
@Client.bot.on_message(filters.command("help"), group=-1)
async def start(_, m: Message):
    if m.from_user:
        if m.from_user.id == Client.id:
            # bot pic
            buttons=InlineKeyboardMarkup(
                [ settings, extra, about, close ]
            )
            botpic = Client.ALIVE_LOGO().split(".")[-1] # extension of media
            if botpic in ("jpg", "png", "jpeg"):
                info = await Client.bot.send_photo(
                    m.chat.id,
                    Client.BotPic(),
                    Client.BotBio(m),
                    reply_markup=buttons
                )
            elif botpic in ("mp4", "gif"):
                info = await Client.bot.send_video(
                    m.chat.id,
                    Client.BotPic(),
                    Client.BotBio(m),
                    reply_markup=buttons
                )
            else:
                info = await Client.bot.send_message(
                    m.chat.id,
                    Client.BotBio(m),
                    reply_markup=buttons
                )

        elif m.from_user.id != Client.id:
            info = await Client.bot.send_photo(
                m.chat.id,
                "main/core/resources/images/tron-square.png",
                f"Hey {m.from_user.mention} You are eligible to use me. There are some commands you can use, check below.",
                reply_markup=InlineKeyboardMarkup(
                    [public]
                ),
            )
        Client.message_ids.update({info.chat.id : info.id})

