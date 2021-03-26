from pyrogram import Client, filters

import redis
import time

r = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=1,
    decode_responses=True
) 

admin = your_id


@Client.on_message(filters.private &~ filters.user([admin, "SpamBot"]), group=1)
def PrivateUserChat(c, m):
    c.send_chat_action(m.chat.id, 'typing')
    time.sleep(0.15)

    for message in r.lrange("messages", 0, -1):
        c.send_message(chat_id=m.chat.id, text=message)
        
    r.sadd("users", m.from_user.id)


