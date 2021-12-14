# By < @xditya >
# // @BotzHub //
from .. import BotzHub
from telethon import events, Button
import string
from random import choice

from . import *


@BotzHub.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    await event.reply("Hello!",
                    buttons=[
                        [Button.url("ButtonUrl", url="https://t.me/xditya")],
                        [Button.inline("Inline Button",data="example")]
                    ])

@BotzHub.on(events.callbackquery.CallbackQuery(data="example"))
async def ex(event):
    await event.edit("You clicked a button!")
    


LOG_CHANNEL = int(udB.get("LOG_CHANNEL"))
KEY = "FILESHARE_DB"


def random_text(len=16):
    list_ = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
    return "".join(choice(list_) for _ in range(len))


async def get_file_id(message_id):
    message = await asst.get_messages(
        LOG_CHANNEL, ids=message_id,
    )
    file_id = message.file.id
    caption = message.text or ""
    msg_link = message.message_link
    rnd = str(random_text(16))
    dict_item = [file_id, caption, msg_link]
    get_db = udB.get(KEY)
    if get_db in [None, "None"]:
        udB.set(KEY, str({rnd: dict_item}))
    else:
        _dict = eval(get_db)
        _dict[rnd] = dict_item
        udB.set(KEY, str(_dict))

    return f"https://t.me/{asst.me.username}?start={rnd}"


@ultroid_cmd(pattern="/share")
async def shareable_link_gen(e):
    reply = await e.get_reply_message()
    if not (reply and reply.media):
        await eor(e, "`Reply to any Media, to generate a Shareable Link`")
        return

    eris = await eor(e, "...")
    try:
        fwd_media = await reply.forward_to(LOG_CHANNEL)
    except Exception as fx:
        await eris.edit(f"Error While forwarding media.\n `{fx}`")
        return

    message_ = await get_file_id(fwd_media.id)
    await eris.edit(f"__Here's your Shareable Link for this File!__ \n\n>> {message_}")


@asst.on(events.NewMessage(
    pattern=f"^/start (.*)",
    func=lambda c: c.is_private,
    incoming=True,
))
async def start_get_file(e):
    args = e.pattern_match.group(1)
    get_db = udB.get(KEY)
    if not (args and get_db):
        return

    get_db = eval(get_db)
    if get_db.get(args) is None:
        await eod(e, "Not a Valid Key!")
        return

    file_id, caption, msglink = get_db.get(args)
    await e.reply(caption, file=file_id)
    if udB.get("FILESHARE_LOGGER") == "True":
        txt = f"#FileShare_Logs !! \n\n • User {inline_mention(e.sender)} Opened [this file!]({msglink})"
        await asst.send_message(LOG_CHANNEL, txt)  
