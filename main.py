from pyrogram import Client

api_id = your_api_id
api_hash = your_api_hash

plugins = dict(root="plugins")

bot = Client(
  name="new_client_bot",
  api_id=api_id,
  api_hash=api_hash,
  plugins=plugins)

bot.run()
