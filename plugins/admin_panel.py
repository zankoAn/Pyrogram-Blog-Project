from pyrogram import Client, filters
import redis


r = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=1,
    decode_responses=True
) 

admin = your_id

@Client.on_message(filters.private & filters.user(admin) & filters.command("help"))
def help_message(c, m):
    help_message = """
    ⚡️اپشن های موجود⚡️
☔️ اضافه کردن پیام به ربات با کامند     `add_msg/`
☔️ نمایش جملات موجود با کامند         `show_msg/`
☔️ حذف کردن پیام از ربات با کامند      `del_msg/`
☔️ چک کردن وضعیت ربات با کامند        `status/`    
.
    """

    c.send_message(chat_id=m.chat.id, text=help_message)


@Client.on_message(filters.private & filters.user(admin) & filters.command("add_msg"))
def add_msg(c , m):
    message_0 = """
        لطفا جمله یا جملات خود را ارسال کنید و در انتها کامند زیر را ارسال کنید:
`/save`
    """

    c.send_message(chat_id=m.chat.id, text=message_0)

    r.set("add_msg", "True")


@Client.on_message(filters.private & filters.user(admin), group=1)
def get_input(c , m):
    text_msg = m.text
    chat_id = m.chat.id

    if text_msg == "/save":
        c.send_message(chat_id=chat_id, text="✅ جمله های شما با موفقیت ذخیره شد")
        r.set("add_msg", "False")   

    if r.get("add_msg") == "True":
        r.rpush("messages", text_msg)
        

@Client.on_message(filters.private & filters.user(admin) & filters.command("show_msg"))
def show_msg(c , m):
    messages=""
    for k,v in dict(enumerate(r.lrange("messages", 0, -1))).items():
        messages += str(k) + ": " + v + "\n" + "_"*30 +"\n"

    c.send_message(chat_id=m.chat.id, text=messages, parse_mode="html" )
    