# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio
import os
from io import BytesIO

from pyrogram import Client, filters
from pyrogram.errors import StickersetInvalid, YouBlockedUser
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName
from pyrogram.types import Message

from PunyaAlby.helpers.PyroHelpers import ReplyCheck
from PunyaAlby.helpers.tools import convert_to_image, get_text, resize_image

from PunyaAlby.modules.help import *


@Client.on_message(filters.command(["packinfo", "stickerinfo"], [".", "-", "^", "!", "?"]) & filters.me)
async def packinfo(client: Client, message: Message):
    rep = await message.reply_text("💈 `Memproses!`")
    if not message.reply_to_message:
        await rep.edit("Balas pesan ke Sticker...")
        return
    if not message.reply_to_message.sticker:
        await rep.edit("Tolong Balas Ke Stiker...")
        return
    if not message.reply_to_message.sticker.set_name:
        await rep.edit("`Sepertinya Stiker Liar!`")
        return
    stickerset = await client.send(
        GetStickerSet(
            stickerset=InputStickerSetShortName(
                short_name=message.reply_to_message.sticker.set_name
            ),
            hash=0,
        )
    )
    emojis = []
    for stucker in stickerset.packs:
        if stucker.emoticon not in emojis:
            emojis.append(stucker.emoticon)
    output = f"""**Judul Paket Stiker **: `{stickerset.set.title}`
**Nama Singkat Paket Stiker **: `{stickerset.set.short_name}`
**Jumlah Stiker **: `{stickerset.set.count}`
**Diarsipkan **: `{stickerset.set.archived}`
**Resmi **: `{stickerset.set.official}`
**Masker **: `{stickerset.set.masks}`
**Animasi **: `{stickerset.set.animated}`
**Emoji Dalam Paket **: `{' '.join(emojis)}`
"""
    await rep.edit(output)


@Client.on_message(filters.command(["tikel", "kang"], [".", "-", "^", "!", "?"]) & filters.me)
async def kang(client: Client, message: Message):
    rep = await message.reply_text("`Tikel nya aku Colong yah hihihi...`")
    if not message.reply_to_message:
        await rep.edit("Mohon Balas Stiker...")
        return
    Hell = get_text(message)
    pack = 1
    f_name = message.from_user.first_name
    packname = f"Sticker Pack {f_name} Vol.{pack}"
    packshortname = f"Sticker_u{message.from_user.id}_{pack}"
    emoji = "✨"
    try:
        Hell = Hell.strip()
        if not Hell.isalpha():
            if not Hell.isnumeric():
                emoji = Hell
        else:
            emoji = "✨"
    except:
        emoji = "✨"
    exist = None
    is_anim = False
    if message.reply_to_message.sticker:
        if not Hell:
            emoji = message.reply_to_message.sticker.emoji or "✨"
        is_anim = message.reply_to_message.sticker.is_animated
        if is_anim:
            packshortname += "_animated"
            packname += " Animated"
        if message.reply_to_message.sticker.mime_type == "application/x-tgsticker":
            file_name = await message.reply_to_message.download("AnimatedSticker.tgs")
        else:
            cool = await convert_to_image(message, client)
            if not cool:
                await rep.edit("`Balas ke media yang valid terlebih dahulu.`")
                return
            file_name = resize_image(cool)
    elif message.reply_to_message.document:
        if message.reply_to_message.document.mime_type == "application/x-tgsticker":
            is_anim = True
            packshortname += "_animated"
            packname += " Animated"
            file_name = await message.reply_to_message.download("AnimatedSticker.tgs")
    else:
        cool = await convert_to_image(message, client)
        if not cool:
            await rep.edit("`Reply to a valid media first.`")
            return
        file_name = resize_image(cool)
    try:
        exist = await client.send(
            GetStickerSet(
                stickerset=InputStickerSetShortName(short_name=packshortname),
                hash=0,
            )
        )
    except StickersetInvalid:
        pass
    if exist:
        try:
            await client.send_message("stickers", "/addsticker")
        except YouBlockedUser:
            await client.unblock_user("stickers")
            await client.send_message("stickers", "/addsticker")
        await asyncio.sleep(2)
        await client.send_message("stickers", packshortname)
        await asyncio.sleep(2)
        limit = "50" if is_anim else "120"
        messi = (await client.get_history("stickers", 1))[0]
        while limit in messi.text:
            pack += 1
            prev_pack = int(pack) - 1
            await rep.edit(
                f"Kang Pack Vol __{prev_pack}__ is Full! Switching To Vol __{pack}__ Kang Pack"
            )
            f_name = message.from_user.first_name
            packname = f"Sticker Pack {f_name} Vol.{pack}"
            packshortname = f"Sticker_u{message.from_user.id}_{pack}"
            if is_anim:
                packshortname += "_animated"
                packname += " Animated"
            await client.send_message("stickers", packshortname)
            await asyncio.sleep(2)
            messi = (await client.get_history("stickers", 1))[0]
            if messi.text == "Invalid pack selected.":
                if is_anim:
                    await client.send_message("stickers", "/newanimated")
                else:
                    await client.send_message("stickers", "/newpack")
                await asyncio.sleep(2)
                await client.send_message("stickers", packname)
                await asyncio.sleep(2)
                await client.send_document("stickers", file_name)
                await asyncio.sleep(2)
                await client.send_message("stickers", emoji)
                await asyncio.sleep(2)
                await client.send_message("stickers", "/publish")
                if is_anim:
                    await client.send_message("stickers", packname)
                await asyncio.sleep(2)
                await client.send_message("stickers", "/skip")
                await asyncio.sleep(2)
                await client.send_message("stickers", packshortname)
                await rep.edit(
                    f"**Sticker Berhasil Ditambahkan!**\n         🎈 **[KLIK DISINI](https://t.me/addstickers/{packshortname})** 🎈\n**Untuk Menggunakan Stickers**"
                )
                return
        await client.send_document("stickers", file_name)
        await asyncio.sleep(2)
        await client.send_message("stickers", emoji)
        await asyncio.sleep(2)
        await client.send_message("stickers", "/done")
        await rep.edit(
            f"**Sticker Berhasil Ditambahkan!**\n         🎭 **[KLIK DISINI](https://t.me/addstickers/{packshortname})** 🎭\n**Untuk Menggunakan Stickers**"
        )
    else:
        if is_anim:
            await client.send_message("stickers", "/newanimated")
        else:
            await client.send_message("stickers", "/newpack")
        await asyncio.sleep(2)
        await client.send_message("stickers", packname)
        await asyncio.sleep(2)
        await client.send_document("stickers", file_name)
        await asyncio.sleep(2)
        await client.send_message("stickers", emoji)
        await asyncio.sleep(2)
        await client.send_message("stickers", "/publish")
        await asyncio.sleep(2)
        if is_anim:
            await client.send_message("stickers", packname)
        await asyncio.sleep(2)
        await client.send_message("stickers", "/skip")
        await asyncio.sleep(2)
        await client.send_message("stickers", packshortname)
        await rep.edit(
            f"**Sticker Berhasil Ditambahkan!**\n         ⚡ **[KLIK DISINI](https://t.me/addstickers/{packshortname})** ⚡\n**Untuk Menggunakan Stickers**"
        )
        if os.path.exists(file_name):
            os.remove(file_name)


@Client.on_message(filters.command(["get", "getsticker"], [".", "-", "^", "!", "?"]) & filters.me)
async def stick2png(client: Client, message: Message):
    try:
        cilik = await message.reply("<b>Downloading...</b>")

        path = await message.reply_to_message.download()
        with open(path, "rb") as f:
            content = f.read()
        os.remove(path)

        file_io = BytesIO(content)
        file_io.name = "sticker.png"

        await client.send_photo(
            message.chat.id, file_io, reply_to_message_id=ReplyCheck(message)
        )
    except Exception as e:
        await cilik.edit(f"{e}")
    else:
        await cilik.delete()


@Client.on_message(filters.me & filters.command(["q", "quotly"], [".", "-", "^", "!", "?"]))
async def quotly(bot: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("`Balas ke pengguna mana pun!`")
    Cilik = await message.reply("```Membuat Kutipan!```")
    await message.reply_to_message.forward("@QuotLyBot")
    is_sticker = False
    progress = 0
    while not is_sticker:
        try:
            await sleep(4)
            msg = await bot.get_history("@QuotLyBot", 1)
            is_sticker = True
        except:
            await sleep(1)
            progress += random.randint(0, 5)
            if progress > 100:
                await Cilik.edit("Kesalahan!")
                return
            try:
                await Cilik.edit("```Membuat Kutipan..\nMemproses! {}%```".format(progress))
            except:
                await Cilik.edit("GAGAL")

    if msg_id := msg[0]["message_id"]:
        await asyncio.gather(
            Cilik.delete(),
            bot.copy_message(message.chat.id, "@QuotLyBot", msg_id),
        )


add_command_help(
    "sticker",
    [
        [
            ".q or .quote",
            "Membuat Stiker",
        ],
        [
            ".kang atau .tikel",
            "Balas .kang Ke Sticker Atau Gambar Untuk Menambahkan Ke Sticker Pack.",
        ],
        [
            ".kang [emoji] atau .tikel [emoji]",
            "Untuk Menambahkan dan costum emoji sticker Ke Sticker Pack Mu.\n\n`  •  **NOTE:** Untuk Membuat Sticker Pack baru Gunakan angka dibelakang {cmd}kang\n  •  **CONTOH:** {cmd}kang 2 untuk membuat dan menyimpan ke sticker pack ke 2`",
        ],
        [
            ".packinfo atau .stickerinfo",
            "Untuk Mendapatkan informasi Sticker Pack.",
        ],
        [".get", "Balas ke sticker untuk mendapatkan foto sticker."],
    ],
)
