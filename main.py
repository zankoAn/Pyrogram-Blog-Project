from pyrogram import Client


bot = Client(
    session_name="new_client_bot",
    config_file="config.ini",
)

bot.run()
