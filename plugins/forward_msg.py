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

@Client.on_message(filters.private & filters.user(admin) & filters.command("forward"))
def forward_msg_S1(c, m):
    c.send_chat_action(m.chat.id, 'typing')
    time.sleep(0.15)
    c.send_message(m.chat.id, """
    ☔️ برای ارسال پیام به تعداد مشخصی از یوزر ها  یک `عدد` را ارسال کنید.
☔️ برای ارسال فوروارد به همه یوزر ها  علامت  `*` را ارسال کنید.
    .
    """)
    
    r.set("forward_msg", "step1")


@Client.on_message(filters.private & filters.user(admin), group=2)
def forward_msg_S2(c, m):
    chat_id = m.chat.id 
    message = m.text

    if r.get("forward_msg") == "step1" and message != "/forward":
        try:
            if message == "*" or isinstance(int(message), int):
                c.send_chat_action(chat_id=chat_id, action='typing')
                time.sleep(0.15)

                resp = c.send_message(chat_id=chat_id, text="پیام مورد نظر خود را برای فوروارد کردن ارسال نمایید.")
                
                r.set("next_msg", resp.message_id)
                r.set("count", message)
                r.set("forward_msg", "step2")

        except ValueError:
            c.send_chat_action(chat_id=chat_id, action='typing')
            time.sleep(0.10)
            c.send_message(chat_id=chat_id, text="❌ ورودی شما اشتباه است\nلطفا فرمت مشخص شده را رعایت کنید.\n.")


@Client.on_message(filters.private & filters.user(admin), group=3)
def forward_msg_S3(c, m):
    chat_id = m.chat.id 
    
    if r.get("forward_msg") == "step2" and int(m.message_id) == int(r.get("next_msg")) + 1:
        counter = 1

        for user_id in r.smembers("users"):
            c.send_chat_action(chat_id=chat_id, action='typing')
            time.sleep(0.10)

            c.forward_messages(
                chat_id = user_id,
                from_chat_id = chat_id,
                message_ids = m.message_id
            )

            if r.get("count") != "*" and counter == int(r.get("count")):
                break

            else:
                counter += 1

        c.send_chat_action(chat_id=chat_id, action='typing')
        time.sleep(0.10)
        c.send_message(chat_id=chat_id, text="پیام شما با موفقت ارسال شد ✅")

        r.set("forward_msg", "step3")
