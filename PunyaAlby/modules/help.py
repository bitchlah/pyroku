import asyncio
from prettytable import PrettyTable
from pyrogram import Client, filters
from pyrogram.types import Message

from PunyaAlby import CMD_HELP
from PunyaAlby.helpers.basic import edit_or_reply
from PunyaAlby.helpers.utility import split_list

heading = "──「 **{0}** 」──\n"
ALIVE_LOGO = "https://telegra.ph/file/cbe826936d4de9ec1838a.jpg"


@Client.on_message(filters.command("help", [".", "-", "^", "!", "?"]) & filters.me)
async def module_help(client: Client, message: Message):
    cmd = message.command

    help_arg = ""
    if len(cmd) > 1:
        help_arg = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        help_arg = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        all_commands = ""
        all_commands += "Silakan tentukan modul mana yang Anda inginkan bantuannya!! \nPenggunaan: `.help [module_name]`\n\n"

        ac = PrettyTable()
        ac.header = False
        ac.title = "🤡 ALBY-Ubot 🤡"
        ac.align = "l"

        for x in split_list(sorted(CMD_HELP.keys()), 2):
            ac.add_row([x[0], x[1] if len(x) >= 2 else None])

            
        text = "🗂️ ALBY-Modules \n\n"
        text += "⚡ Ubot: -⋟ `kit` -⋟ `alive` -⋟ `heroku` -⋟ `system` -⋟ `updater` \n\n"
        text += "⚙️ Tolls: -⋟ `profile` -⋟ `gcast` -⋟ `info` -⋟ `locks` -⋟ `tools` -⋟ `vctools` -⋟ `purge` \n\n"
        text += "💥 Fun : -⋟ `asupan` -⋟ `animasi` -⋟ `nulis -⋟ `salam` -⋟ `toxic` \n\n"
        text += "🧰 Other: -⋟ `admin` -⋟ `afk` -⋟ `globals` -⋟ `gcast` -⋟ `groups` -⋟ `join` -⋟ `misc` -⋟ `nulis` -⋟ `spam` -⋟ `sticker` -⋟ `translate` -⋟ `pmpermit` \n\n\n"
        text += "📮 Prefix -⋟ `[. - ^ ! ?]`\n"
        text += "    `.help` `[module_name]`\n"
        
        await message.reply_photo(
           photo=ALIVE_LOGO,
           caption=text,
        )     
           
    if help_arg:
        if help_arg in CMD_HELP:
            commands: dict = CMD_HELP[help_arg]
            this_command = "**📚 Bantuan Perintah**\n"
            this_command += heading.format(str(help_arg)).upper()

            for x in commands:
                this_command += f"-⋟ `{str(x)}`\n```{str(commands[x])}```\n\n"

            await message.edit(this_command, parse_mode="markdown")
        else:
            await message.edit(
                "`Harap tentukan nama modul yang valid.`", parse_mode="markdown"
            )
    


def add_command_help(module_name, commands):

    if module_name in CMD_HELP.keys():
        command_dict = CMD_HELP[module_name]
    else:
        command_dict = {}

    for x in commands:
        for y in x:
            if y is not x:
                command_dict[x[0]] = x[1]

    CMD_HELP[module_name] = command_dict
