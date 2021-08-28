from pyrogram import Client, filters

from plugins import r, admin

import asyncio



@Client.on_message(filters.private &~ filters.user([admin, "SpamBot"]), group=3)
async def PrivateUserChat(c, m):

    chat_id = m.chat.id
    
    if r.exists("Messages"):
        data = sorted(r.smembers("Messages"), key=lambda x: x.split(":")[0])

        for message in data: 
            await c.send_chat_action(chat_id=chat_id, action='typing')
            await asyncio.sleep(0.17)

            await c.send_message(chat_id=m.chat.id, text=message.split(":", 1)[1])

            await asyncio.sleep(3)

    else:
        await c.send_chat_action(chat_id=chat_id, action='typing')
        await asyncio.sleep(0.15)

        message=f"سلام {m.from_user.first_name} ✋"

        await c.send_message(chat_id=m.chat.id, text=message)

    current_user = await c.get_me()
    r.sadd(f"users:{current_user.id}", m.from_user.id)



