
from pyrogram import filters, Client
from pyrogram.types import Message

from PunyaAlby import CMD_HELP

@Client.on_message(filters.command("help"))
async def helpmenu_handler(_, m: Message):
    """ helpmenu handler for help plugin """

    args = m.command if Client.long() > 1 else None

    try:
        if not args:
            await Client.send_edit(". . .", text_type=["mono"])
            result = await Client.get_inline_bot_results(
                Client.bot.username,
                "#helpmenu"
            )
            if result:
                await m.delete()
                info = await Client.send_inline_bot_result(
                    m.chat.id,
                    query_id=result.query_id,
                    result_id=result.results[0].id,
                    disable_notification=True,
                )

            else:
                await Client.send_edit(
                    "Please check your bots inline mode is on or not . . .",
                    delme=3,
                    text_type=["mono"]
                )
        elif args:

            module_help = await Client.PluginData(args[1])
            if not module_help:
                await Client.send_edit(
                    f"Invalid plugin name specified, use `{Client.Trigger()[0]}uplugs` to get list of plugins",
                    delme=3
                )
            else:
                await Client.send_edit(f"**MODULE:** {args[1]}\n\n" + "".join(module_help))
        else:
            await Client.send_edit("Try again later !", text_type=["mono"], delme=3)
    except BotInlineDisabled:
        await Client.toggle_inline()
        await helpmenu_handler(_, m)
    except Exception as e:
        await Client.error(e)

@Client.on_message(filters.command("inline"))
async def toggleinline_handler(_, m: Message):
    """ toggleinline handler for help plugin """
    return await Client.toggle_inline()
