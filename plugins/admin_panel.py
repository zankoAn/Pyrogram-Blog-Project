from pyrogram import Client, filters
from plugins import r, admin


@Client.on_message(filters.private & filters.user(admin) & filters.command("help"))
def help_message(c, m):
    help_message = """
     ⚡️اپشن های موجود⚡️
    
☔️ اضافه کردن پیام به ربات با کامند                     `add_msg/`
☔️ حذف کردن پیام از ربات با کامند                       `del_msg/`
☔️ نمایش جملات موجود با کامند                        `show_msg/`
☔️ نمایش وضعیت ربات                                              `info/`
☔️ چک کردن وضعیت ربات با کامند                          `status/`
فوروارد کردن پیام                                                   `forward/`
جوین شدن داخل گروه مورد نظر                         `join_chat/`
ست کردن پیام بعد از جوین شدن ربات در گروه      `join_msg/`
.
    """

    c.send_message(chat_id=m.chat.id, text=help_message)


@Client.on_message(filters.private & filters.user(admin) & filters.command("add_msg"))
def add_msg(c, m):
    message_0 = """
        لطفا جمله یا جملات خود را ارسال کنید و در انتها کامند زیر را ارسال کنید:
`/save`
    """

    c.send_message(chat_id=m.chat.id, text=message_0)
    r.set("add_msg", "True")


@Client.on_message(filters.private & filters.user(admin), group=1)
def get_input(c, m):
    text_msg = m.text
    chat_id = m.chat.id

    if text_msg == "/save":
        c.send_message(chat_id=chat_id,
                       text="✅ جمله های شما با موفقیت ذخیره شد")
        r.set("add_msg", "False")

    if r.get("add_msg") == "True" and text_msg != "/add_msg":
        r.rpush("messages", text_msg)

    if r.get("del_msg") == "True" and text_msg != '/del_msg':
        try:
            if text_msg == "*":
                r.delete("messages")

            else:
                msg_number = r.lrange("messages", 0, -1)[int(text_msg)]
                r.lrem("messages", 0, msg_number)

            c.send_message(chat_id=chat_id,
                           text="جمله/جملات  شما با موفقیت حذف شد ✅")
            r.set("del_msg", "False")

        except ValueError:
            c.send_message(chat_id=chat_id,
                           text="❌لطفا عدد مربوط به جمله ها را ارسال کنید❌")

        except IndexError:
            c.send_message(chat_id=chat_id,
                           text="❌عدد وارد شده بیشتر از تعداد پیام ها میباشد❌")


@Client.on_message(filters.private & filters.user(admin) & filters.command("show_msg"))
def show_msg(c, m):
    chat_id = m.chat.id
    if r.exists("messages"):
        messages = ""
        for k, v in dict(enumerate(r.lrange("messages", 0, -1))).items():
            messages += str(k) + ": " + v + "\n" + "_"*30 + "\n"

        c.send_message(chat_id=chat_id, text=messages, parse_mode="html")

    else:
        c.send_message(chat_id=chat_id, text="❌جمله ای یافت نشد❌")


@Client.on_message(filters.private & filters.user(admin) & filters.command("del_msg"))
def del_msg(c, m):
    chat_id = m.chat.id
    if r.exists("messages"):
        message = "لطفا `شماره` جمله مورد نظر خود ارسال کنید.🗑"

        c.send_message(chat_id=chat_id, text=message)

        r.set("del_msg", "True")

    else:
        c.send_message(chat_id=chat_id, text="❌جمله ای یافت نشد❌")
