from pyrogram import Client, filters, errors
from plugins import r, admin

import time


def chat_action(c, chat_id):
    c.send_chat_action(chat_id, 'typing')
    time.sleep(0.15)


@Client.on_message(filters.private & filters.user(admin) & filters.command("join_chat"))
def get_link_chat(c, m):
    chat_action(c, m.chat.id)
    c.send_message(chat_id=m.chat.id, text="لینک گروه مدنظر خود را ارسال کنید")
    
    r.set("join_chat_status", "True")
    

@Client.on_message(filters.private & filters.user(admin) & filters.command("join_msg"))
def get_join_msg(c, m):
    chat_action(c, m.chat.id)
    c.send_message(chat_id=m.chat.id, text="پیام مورد نظر خود را ارسال کنید")
    
    r.set("join_msg_status", "True")


@Client.on_message(filters.private & filters.user(admin), group=4)
def join_chat(c, m):
    if r.get("join_chat_status") == "True" and m.text != "/join_chat":
        chat_id = m.chat.id

        try:
            if "joinchat" in m.text:
                resp = c.join_chat(chat_id=m.text)
            else:
                resp = c.join_chat(chat_id=m.text.split("/")[-1])
            
            chat_action(c, chat_id)
            c.send_message(chat_id=chat_id, text="شما با موفقیت به گروه پیوستید ✅")
        
            if r.get("join_msg"):
                try:
                    chat_action(c, resp.id)
                    c.send_message(chat_id=resp.id, text=r.get("join_msg"))
                except errors.ChatAdminRequired:
                    pass
                
        except errors.UserAlreadyParticipant:
            chat_action(c, m.chat.id)
            c.send_message(chat_id=chat_id, text="❌ .شما قبلا در این گروه عضو شده اید ❌")

        except errors.UsernameInvalid:
            chat_action(c, m.chat.id)
            c.send_message(chat_id=chat_id, text="❌ لطفا لینک صحیح را ارسال کنید. ❌")
        
        except errors.ChannelInvalid:
            chat_action(c, m.chat.id)
            c.send_message(chat_id=chat_id, text="❌ لینک ارسال شده نامعتبر است  ❌")

        except errors.InviteHashExpired:
            chat_action(c, m.chat.id)
            c.send_message(chat_id=chat_id, text="❌ لینک شما منقضی شده است. ❌")

        except errors.UsernameNotOccupied:
            chat_action(c, m.chat.id)
            c.send_message(chat_id=chat_id, text="❌ هیچ گروهی با این لینک وجود ندارد ❌")

        except errors.FloodWait as wait:
            chat_action(c, m.chat.id)
            c.send_message(chat_id=chat_id, text=f"❌ شماره به مدت {wait.x} ثانیه محدوده شده اید لطفا بعد از زمان محدودیت دوباره تلاش کنید ❌")

        finally:
            r.set("join_chat_status", "False")


    elif r.get("join_msg_status") == "True" and m.text != "/join_msg":
        r.set("join_msg", m.text)
        chat_action(c, m.chat.id)
        c.send_message(chat_id=m.chat.id, text="پیام شما با موفقیت ذخیره شد ✅")

        r.set("join_msg_status", "False")

