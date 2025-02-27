import os
from pyrogram import Client, filters

# Credentials (Replace with your own API details)
API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"

# Initialize Bot
app = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start Command
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Hello! Send me a file and I will rename it. 📂")

# Handle Files
@app.on_message(filters.document | filters.video | filters.audio)
def file_handler(client, message):
    file = message.document or message.video or message.audio
    file_name = file.file_name

    msg = message.reply_text(f"Current File Name: `{file_name}`\n\nSend me the new name without extension.")
    
    @app.on_message(filters.text & filters.reply)
    def rename_file(client, reply_message):
        new_name = reply_message.text
        file_ext = os.path.splitext(file_name)[1]  # Get original extension
        new_file_name = new_name + file_ext  # Append extension

        reply_message.reply_text(f"Renaming `{file_name}` to `{new_file_name}`...")

        file_path = client.download_media(message)
        new_path = os.path.join(os.path.dirname(file_path), new_file_name)

        os.rename(file_path, new_path)
        client.send_document(message.chat.id, new_path, caption=f"Here is your renamed file: `{new_file_name}`")

        os.remove(new_path)  # Delete the renamed file after sending

app.run()