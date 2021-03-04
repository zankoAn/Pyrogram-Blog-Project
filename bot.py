from pyrogram import Client, filters
import redis

r = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=1,
    decode_responses=True
) 

bot = Client(
    session_name="new_client_bot",
    config_file="config.ini",
)

admin = your_id

@bot.on_message(filters.private & ~filters.user(admin))
def GetPM(c, m):
    c.send_message(m.chat.id, "salam")

bot.run()
    
    
