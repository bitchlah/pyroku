import os
from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.types import Message

from PunyaAlby.modules.help import *

profile_photo = "PunyaAlby/modules/cache/pfp.jpg"


@Client.on_message(filters.me & filters.command(["setpfp"], [".", "-", "^", "!", "?"]))
async def set_pfp(client: Client, message: Message):
    replied = message.reply_to_message
    if (
        replied
        and replied.media
        and (
            replied.photo
            or (replied.document and "image" in replied.document.mime_type)
        )
    ):
        await client.download_media(message=replied, file_name=profile_photo)
        await client.set_profile_photo(photo=profile_photo)
        if os.path.exists(profile_photo):
            os.remove(profile_photo)
        xx = await message.reply("<code>Profile picture changed.</code>", parse_mode="html")
    else:
        await message.reply("```Balas ke foto apa pun untuk ditetapkan sebagai pfp```")
        await sleep(3)
        await xx.delete()


@Client.on_message(filters.me & filters.command(["vpfp"], [".", "-", "^", "!", "?"]))
async def view_pfp(client: Client, message: Message):
    replied = message.reply_to_message
    if replied:
        user = await client.get_users(replied.from_user.id)
    else:
        user = await client.get_me()
    if not user.photo:
        await message.reply("Foto profil tidak ditemukan!")
        return
    await client.download_media(user.photo.big_file_id, file_name=profile_photo)
    await client.send_photo(message.chat.id, profile_photo)
    if os.path.exists(profile_photo):
        os.remove(profile_photo)

        
@Client.on_message(filters.command(["setbio"], [".", "-", "^", "!", "?"]) & filters.me)
async def set_bio(client, message):
    Cilik = await message.reply("💈 `Harap Tunggu...`")
    if len(message.command) == 1:
        return await Man.edit("Berikan beberapa teks untuk ditetapkan sebagai bio.")
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
        try:
            await client.update_profile(bio=bio)
            await Cilik.edit("Changed Bio.")
        except Exception as e:
            await Cilik.edit(f"**ERROR:** `{e}`")
    else:
        return await Cilik.edit("Berikan beberapa teks untuk ditetapkan sebagai bio.")
    
    
add_command_help(
    "profile",
    [
        [".setpfp", "Balas ke foto apa pun untuk ditetapkan sebagai pfp/photoprofil."],
        [".vpfp", "Lihat photo profil pengguna saat ini."],
        [".setbio", "untuk set bio kamu."],

    ],
)
