from plugins import query, admin

from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ParseMode



@Client.on_message(filters.private & filters.user(admin) & filters.command("help"))
async def help_message(client, message):
    chat_id = message.chat.id

    help_message = """⚡️ **اپشن های موجود** ⚡️
        \n☔️ اضافه کردن پیام به ربات با کامند     /add_msg
        \n☔️ حذف کردن پیام از ربات با کامند       /del_msg
        \n☔️ نمایش جمسملات موجود با کامند       /show_msg
        \n☔️ نمایش وضعیت ربات     /info
        \n☔️ چک کردن وضعیت ربات با کامند      /status
        \n☔️ فوروارد کردن پیام       /forward
        \b☔️ جوین شدن داخل گروه مورد نظر     /join_chat
        \n☔️ ست کردن پیام بعد از جوین شدن ربات در گروه       /join_msg
        \n.
    """

    await client.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    await message.reply(text=help_message,parse_mode=ParseMode.HTML)


@Client.on_message(filters.private & filters.user(admin) & filters.command("add_msg"))
async def add_msg(client, message):
    chat_id = message.chat.id
    messages = """⚡️ **اضافه کردن پیام** ⚡️
        \nلطفا جمله یا جملات خود را ارسال کنید و در انتها کامند زیر را ارسال کنید:
        \n/save
    """
    
    await client.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    await message.reply(text=messages)

    query.setbit("add:msg", 0, 1)


@Client.on_message(filters.private & filters.user(admin), group=1)
async def get_input(client, message):
    msg = message.text

    if query.getbit("add:msg", 0) == 1 and msg and not msg.startswith("/"):
        msg_counter = query.incr("New:Msg")
        query.sadd("Messages", f"{msg_counter}:{msg}")

    elif msg == "/save":
        chat_id = message.chat.id
        await client.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        await message.reply("""⚡️ **اضافه کردن پیام** ⚡️
            \n✅ جمله های شما با موفقیت ذخیره شد
            \n.
        """)

        query.setbit("add:msg", 0, 0)


@Client.on_message(filters.private & filters.user(admin) & filters.command("show_msg"))
async def show_msg(client, message):
    chat_id = message.chat.id

    await client.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    if query.exists("Messages"):
        messages = "⚡️ **نمایش جمله ها** ⚡️\n"
        data = sorted(query.smembers("Messages"), key=lambda x: x.split(":")[0])

        for item in data:
            item = item.split(":", 1)
            separator = "➖" * 12
            messages += f"`{item[0]}`:{item[1]}\n{separator}\n"
        await message.reply(messages)

    else:
        await message.reply("❌جمله ای یافت نشد❌")


# @Client.on_message(filters.private & filters.user(admin) & filters.command("del_msg"))
# async def del_msg(c, m):
#     chat_id = m.chat.id 

#     await c.send_chat_action(chat_id=chat_id, action="typing")

#     if r.exists("Messages"):

#         message = """⚡️ **حذف کردن جمه ها** ⚡️            
#             \nلطفا شماره جمله مورد نظر خود ارسال کنید. 🗑            
#             \nو یا برای حذف همه جمله ها  `*` را ارسال نمایید
#             \n.
#         """

#         await c.send_message(chat_id=chat_id, text=message)

#         r.setbit("del:msg", 0, 1)

#     else:
#         await c.send_message(chat_id=chat_id, text="❌جمله ای یافت نشد❌")




# @Client.on_message(filters.private & filters.user(admin), group=2)
# async def get_message_id(c, m):

#     msg = m.text

#     if r.getbit("del:msg", 0) == 1 and msg and not msg.startswith("/"):
#         chat_id = m.chat.id 
#         await c.send_chat_action(chat_id=chat_id, action="typing")

#         if msg == "*":
#             r.delete("Messages")
#             r.setbit("del:msg", 0, 0)
#             await c.send_message(chat_id=chat_id, text="""⚡️ **حذف همه پیام ها** ⚡️\n
#                 \nتمامی جملات شما با موفقیت حذف شد ✅"""
#             )

#         else:
#             msg_number = r.sscan("Messages", match=f"{msg}:*")[1]

#             if msg_number:
#                 r.srem("Messages", msg_number[0])
#                 r.setbit("del:msg", 0, 0)
#                 await c.send_message(chat_id=chat_id, text="""⚡️ **حذف پیام** ⚡️\n
#                     \n جمله شما با موفقیت حذف شد ✅""" 
#                 )

#             else:
#                 messages = "⚡️ **حذف پیام** ⚡️\n\n❌جمله ای یافت نشد❌"

#                 await c.send_message(chat_id=chat_id, text=messages)
