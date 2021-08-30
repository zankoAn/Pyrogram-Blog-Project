from pyrogram import Client, filters, errors

from plugins import r, admin

import asyncio




async def chat_action(c, chat_id):
    await c.send_chat_action(chat_id, 'typing')
    await asyncio.sleep(0.15)




@Client.on_message(filters.private & filters.user(admin) & filters.command("join_msg"))
async def get_join_msg(c, m):

    chat_id = m.chat.id 

    await asyncio.create_task(chat_action(c, chat_id))
    await c.send_message(chat_id=chat_id, text="پیام مورد نظر خود را ارسال کنید")
    
    r.setbit("join:msg:status", 0, 1)




@Client.on_message(filters.private & filters.user(admin), group=6)
async def set_join_msg(c, m):
    
    msg = m.text

    if r.getbit("join:msg:status", 0) == 1 and msg and not msg.startswith("/"):
        chat_id = m.chat.id

        await asyncio.create_task(chat_action(c, chat_id))
        
        r.set("join:msg", msg)
        
        await c.send_message(chat_id=chat_id, text="پیام شما با موفقیت ذخیره شد ✅")

        r.setbit("join:msg:status", 0, 0)




@Client.on_message(filters.private & filters.user(admin) & filters.command("join_chat"))
async def get_link_chat(c, m):
    
    chat_id = m.chat.id 

    await asyncio.create_task(chat_action(c, chat_id))

    await c.send_message(chat_id=chat_id, text="لینک گروه مدنظر خود را ارسال کنید")
    
    r.setbit("join:chat:status", 0, 1)
    



@Client.on_message(filters.private & filters.user(admin), group=7)
async def join_chat(c, m):

    msg = m.text

    if r.getbit("join:chat:status", 0) == 1 and msg and not msg.startswith("/"):
        chat_id = m.chat.id

        await asyncio.create_task(chat_action(c, chat_id))

        try:
            if "joinchat" in msg:
                resp = await c.join_chat(chat_id=m.text)

            else:
                resp = await c.join_chat(chat_id=msg.split("/")[-1])
            
            await c.send_message(chat_id=chat_id, text="شما با موفقیت به گروه پیوستید ✅")
        
            if r.get("join:msg"):
                try:
                    await asyncio.create_task(chat_action(c, resp.id))
                    await c.send_message(chat_id=resp.id, text=r.get("join:msg"))

                except errors.ChatAdminRequired:
                    pass
                
        except errors.UserAlreadyParticipant:
            await c.send_message(chat_id=chat_id, text="❌ .شما قبلا در این گروه عضو شده اید ❌")

        except errors.UsernameInvalid:            
            await c.send_message(chat_id=chat_id, text="❌ لطفا لینک صحیح را ارسال کنید. ❌")
        
        except errors.ChannelInvalid:            
            await c.send_message(chat_id=chat_id, text="❌ لینک ارسال شده نام+عتبر است  ❌")

        except errors.InviteHashExpired:            
            await c.send_message(chat_id=chat_id, text="❌ لینک شما منقضی شده است. ❌")

        except errors.UsernameNotOccupied:
            await c.send_message(chat_id=chat_id, text="❌ هیچ گروهی با این لینک وجود ندارد ❌")

        except errors.FloodWait as wait:
            await c.send_message(chat_id=chat_id, 
                text=f"❌ شماره به مدت {wait.x} ثانیه محدوده شده اید لطفا بعد از زمان محدودیت دوباره تلاش کنید ❌")

        finally:
            r.setbit("join:chat:status", 0, 0)

