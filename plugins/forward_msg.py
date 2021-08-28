from pyrogram import Client, filters

from plugins import r, admin

import asyncio




@Client.on_message(filters.private & filters.user(admin) & filters.command("forward"))
async def forward_msg_S1(c, m):

    message = """⚡️ **Forward Msg** ⚡️
        \n☔️ برای ارسال پیام به تعداد مشخصی از یوزر ها  یک `عدد` را ارسال کنید
        \n☔️ برای ارسال فوروارد به همه یوزر ها  علامت  `*` را ارسال کنید
        \n.    
    """
    
    chat_id = m.chat.id 

    await c.send_chat_action(chat_id=chat_id, action="typing")
    await asyncio.sleep(0.15)
  
    await c.send_message(chat_id=chat_id, text=message)
    
    # First Step
    r.setbit("forward:msg", 0, 1)

    # Second Step
    r.setbit("forward:msg", 1, 0)




@Client.on_message(filters.private & filters.user(admin) , group=4)
async def forward_msg_S2(c, m):

    chat_id = m.chat.id

    msg = m.text

    if r.getbit("forward:msg", 0) == 1 and msg and not msg.startswith("/"):
        try:
            if msg == "*" or int(msg):
                await c.send_chat_action(chat_id=chat_id, action="typing")
                await asyncio.sleep(0.15)

                resp = await c.send_message(chat_id=chat_id, 
                    text="""⚡️ **Forward Msg** ⚡️
                        \nپیام مورد نظر خود را برای فوروارد کردن ارسال نمایید
                        \n.
                    """
                )
                
                r.set("Msg:Number", msg)
                r.set("Previous:Msg:ID", resp.message_id)
                r.setbit("forward:msg", 0, 0)
                r.setbit("forward:msg", 1, 1)

        except ValueError:
            await c.send_chat_action(chat_id=chat_id, action='typing')
            await asyncio.sleep(0.10)

            await c.send_message(chat_id=chat_id, 
                text="""⚡️ **Forward Msg** ⚡️
                    \nورودی صحیح نمیباشد! ❌
                    \nلطفا فرمت مشخص شده را رعایت کنید.                    
                    \n.
                """
            )





@Client.on_message(filters.private & filters.user(admin)&~ filters.me, group=5)
async def forward_msg_S3(c, m):

    chat_id = m.chat.id 
    
    if r.getbit("forward:msg", 1) == 1:

        previous_msg = int(r.get("Previous:Msg:ID"))

        if m.message_id == int(previous_msg)+1:                
            counter = 1
            current_user = await c.get_me()

            for user_id in r.smembers(f"users:{current_user.id}"):
                await c.send_chat_action(chat_id=chat_id, action='typing')
                await asyncio.sleep(0.10)

                await c.forward_messages(
                    chat_id = user_id,
                    from_chat_id = chat_id,
                    message_ids = m.message_id
                )

                if r.get("Msg:Number") != "*" and counter == int(r.get("Msg:Number")):
                    break

                else:
                    counter += 1

            await c.send_chat_action(chat_id=chat_id, action='typing')
            await asyncio.sleep(0.10)
            await c.send_message(chat_id=chat_id, text="پیام شما با موفقت ارسال شد ✅")

            r.setbit("forward:msg", 1, 0)

