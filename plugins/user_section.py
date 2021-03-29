from pyrogram import Client, filters
from plugins import r, admin

import time



@Client.on_message(filters.private &~ filters.user([admin, "SpamBot"]), group=1)
def PrivateUserChat(c, m):
    c.send_chat_action(m.chat.id, 'typing')
    time.sleep(0.15)

    for message in r.lrange("messages", 0, -1):
        c.send_message(chat_id=m.chat.id, text=message)
        
    r.sadd("users", m.from_user.id)


