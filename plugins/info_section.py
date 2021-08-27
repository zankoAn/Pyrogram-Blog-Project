from pyrogram import Client, filters, raw

from plugins import r, admin

import asyncio



@Client.on_message(filters.private & filters.user(admin) & filters.command("status"))
async def get_status(c, m):
    
    chat_id = m.chat.id

    response = await c.send(
        raw.functions.messages.StartBot(
            bot=await c.resolve_peer('SpamBot'),
            peer=await c.resolve_peer('SpamBot'),
            random_id= c.rnd_id(),
            start_param='start'
        )
    )

    message = "در حال برسی اطلاعات لطفا صبور باشید... ⏳"
    await c.send_chat_action(chat_id=chat_id, action='typing')
    wait_msg = await c.send_message(chat_id=chat_id, text=message)
    
    await asyncio.sleep(1)

    spambot_msg = response.updates[1].message.id+1

    status = await c.get_messages(chat_id="SpamBot", message_ids=spambot_msg)
    await c.delete_messages(chat_id=chat_id, message_ids=wait_msg.message_id)
    await c.send_message(chat_id=chat_id, text=f"`{status.text}`")




@Client.on_message(filters.private & filters.user(admin) & filters.command("info"))
async def show_info(c, m):

    chat_id = m.chat.id

    groups = 0
    private_chats = 0

    message = "در حال برسی اطلاعات لطفا صبور باشید... ⏳"

    await c.send_chat_action(chat_id=chat_id, action='typing')
    wait_msg = await c.send_message(chat_id=chat_id, text=message)

    async for dialog in c.iter_dialogs():
        if dialog.chat.type in ["supergroup", "group"]:
            groups += 1
        
        if dialog.chat.type == "private":
            private_chats += 1



    message = f"""〽️ **اطلاعات ربات** 〽️
        \n{"➖" * 20}
        \n🔘• `تعداد گروه ها :` **{groups}**
        \n🔘• `تعداد کاربران :` **{private_chats}**
        \n🔘• `مدیران :`  <a href="tg://user?id={admin}">admin</a>\n{"➖" * 20}

    """

    await c.delete_messages(chat_id=chat_id, message_ids=wait_msg.message_id)    
    await c.send_chat_action(chat_id=chat_id, action='typing')
    await c.send_message(chat_id=chat_id, text=message)
