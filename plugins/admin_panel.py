from pyrogram import Client, filters

from plugins import r, admin



@Client.on_message(filters.private & filters.user(admin) & filters.command("help"))
async def help_message(c, m):

	chat_id = m.chat.id 

	help_message = """⚡️ **اپشن های موجود** ⚡️
        \n☔️ اضافه کردن پیام به ربات با کامند     /add_msg        
		\n☔️ حذف کردن پیام از ربات با کامند       /del_msg        
		\n☔️ نمایش جملات موجود با کامند       /show_msg        
		\n☔️ نمایش وضعیت ربات     /info        
		\n☔️ چک کردن وضعیت ربات با کامند      /status        
		\n☔️ فوروارد کردن پیام       /forward        
		\b☔️ جوین شدن داخل گروه مورد نظر     /join_chat        
		\n☔️ ست کردن پیام بعد از جوین شدن ربات در گروه       /join_msg
		\n.
	"""

	await c.send_chat_action(chat_id=chat_id, action="typing")

	await c.send_message(chat_id=chat_id, text=help_message)




@Client.on_message(filters.private & filters.user(admin) & filters.command("add_msg"))
async def add_msg(c, m):
    messages = """⚡️ **اضافه کردن پیام** ⚡️
        \nلطفا جمله یا جملات خود را ارسال کنید و در انتها کامند زیر را ارسال کنید:
        \n/save
    """

    chat_id = m.chat.id 

    await c.send_chat_action(chat_id=chat_id, action="typing")

    await c.send_message(chat_id=chat_id, text=messages)

    r.setbit("add:msg", 0, 1)




@Client.on_message(filters.private & filters.user(admin), group=1)
async def get_input(c, m):

    msg = m.text

    if r.getbit("add:msg", 0) == 1 and not msg.startswith("/"):

        msg_counter = r.incr("New:Msg")

        r.sadd("Messages", f"{msg_counter}:{msg}")

    elif msg == "/save":
        chat_id = m.chat.id

        await c.send_chat_action(chat_id=chat_id, action="typing")

        await c.send_message(chat_id=chat_id, text="""⚡️ **اضافه کردن پیام** ⚡️
            \n✅ جمله های شما با موفقیت ذخیره شد
            \n.
        """)

        r.setbit("add:msg", 0, 0)




@Client.on_message(filters.private & filters.user(admin) & filters.command("show_msg"))
async def show_msg(c, m):

    chat_id = m.chat.id 

    await c.send_chat_action(chat_id=chat_id, action="typing")

    if r.exists("Messages"):
        messages = "⚡️ **نمایش جمله ها** ⚡️\n"

        data = sorted(r.smembers("Messages"), key=lambda x: x.split(":")[0])

        for item in data:

            item = item.split(":", 1)

            separator = "➖" * 12

            messages += f"`{item[0]}`:{item[1]}\n{separator}\n"

        await c.send_message(chat_id=chat_id, text=messages)

    else:
        await c.send_message(chat_id=chat_id, text="❌جمله ای یافت نشد❌")




@Client.on_message(filters.private & filters.user(admin) & filters.command("del_msg"))
async def del_msg(c, m):

    chat_id = m.chat.id 

    await c.send_chat_action(chat_id=chat_id, action="typing")

    if r.exists("Messages"):

        message = """⚡️ **حذف کردن جمه ها** ⚡️            
            \nلطفا شماره جمله مورد نظر خود ارسال کنید. 🗑            
            \nو یا برای حذف همه جمله ها  `*` را ارسال نمایید
            \n.
        """

        await c.send_message(chat_id=chat_id, text=message)

        r.setbit("del:msg", 0, 1)

    else:
        await c.send_message(chat_id=chat_id, text="❌جمله ای یافت نشد❌")




@Client.on_message(filters.private & filters.user(admin), group=2)
async def get_message_id(c, m):

    msg = m.text

    if r.getbit("del:msg", 0) == 1 and not msg.startswith("/"):
        chat_id = m.chat.id 
        await c.send_chat_action(chat_id=chat_id, action="typing")

        if msg == "*":
            r.delete("Messages")
            r.setbit("del:msg", 0, 0)
            await c.send_message(chat_id=chat_id, text="""⚡️ **حذف همه پیام ها** ⚡️\n
                \nتمامی جملات شما با موفقیت حذف شد ✅"""
            )

        else:
            msg_number = r.sscan("Messages", match=f"{msg}:*")[1]

            if msg_number:
                r.srem("Messages", msg_number[0])
                r.setbit("del:msg", 0, 0)
                await c.send_message(chat_id=chat_id, text="""⚡️ **حذف پیام** ⚡️\n
                    \n جمله شما با موفقیت حذف شد ✅""" 
                )

            else:
                messages = "⚡️ **حذف پیام** ⚡️\n\n❌جمله ای یافت نشد❌"

                await c.send_message(chat_id=chat_id, text=messages)
