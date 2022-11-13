from pyrogram import filters

from pyrogram.types import (
    InlineKeyboardMarkup, 
    Message,
)

from PunyaAlby.userbot import app



emoji = app.HelpEmoji() or "•"

settings = app.BuildKeyboard(([[f"{emoji} Modules {emoji}", "plugins-tab"]]))
close = app.BuildKeyboard(([["Close", "close-tab"]]))





# /help command for bot
@app.bot.on_message(filters.command("help"), group=-1)
async def start(_, m: Message):
    if m.from_user:
        if m.from_user.id == app.id:
            # bot pic
            buttons=InlineKeyboardMarkup(
                [ settings, close ]
            )
            botpic = app.ALIVE_LOGO().split(".")[-1] # extension of media
            if botpic in ("jpg", "png", "jpeg"):
                info = await app.bot.send_photo(
                    m.chat.id,
                    app.BotPic(),
                    app.BotBio(m),
                    reply_markup=buttons
                )
            elif botpic in ("mp4", "gif"):
                info = await app.bot.send_video(
                    m.chat.id,
                    app.BotPic(),
                    app.BotBio(m),
                    reply_markup=buttons
                )
            else:
                info = await app.bot.send_message(
                    m.chat.id,
                    app.BotBio(m),
                    reply_markup=buttons
                )

        elif m.from_user.id != app.id:
            info = await app.bot.send_photo(
                m.chat.id,
                "PunyaAlby/helpers/PYROBY.jpg",
                f"Hey {m.from_user.mention} You are eligible to use me. There are some commands you can use, check below.",
                reply_markup=InlineKeyboardMarkup(
                    [public]
                ),
            )
        app.message_ids.update({info.chat.id : info.id})

