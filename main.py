import os
import asyncio
from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import Message

# ================= SERVER (UPTIME) =================
flask_app = Flask("")
@flask_app.route("/")
def home(): return "Bot 24/7 ishlamoqda!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

Thread(target=run_flask, daemon=True).start()

# ================= ASOSIY BOT =================
async def start_bot():
    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_HASH")
    session_string = os.environ.get("SESSION_STRING")
    source_channel = os.environ.get("SOURCE_CHANNEL")
    target_channel = os.environ.get("TARGET_CHANNEL")

    if not all([api_id, api_hash, session_string, source_channel, target_channel]):
        print("❌ Xatolik: Kerakli muhit o'zgaruvchilari (ENV) topilmadi!")
        return

    app = Client("render_userbot", api_id=int(api_id), api_hash=api_hash, session_string=session_string)

    @app.on_message(filters.chat(source_channel))
    async def forwarder(client, message: Message):
        text = message.caption or message.text or ""
        
        # 1. Jami matn uzunligi 1024 dan kam bo'lsa (Media + Matn birga)
        if len(text) <= 1024:
            if message.photo: 
                await client.send_photo(target_channel, message.photo.file_id, caption=text)
            elif message.video: 
                await client.send_video(target_channel, message.video.file_id, caption=text)
            else: 
                await client.send_message(target_channel, text)
            
        # 2. Jami matn uzunligi 1024 dan oshsa (Media + Matnni ajratish)
        else:
            # Media qismi (faqat media)
            if message.photo: 
                await client.send_photo(target_channel, message.photo.file_id)
            elif message.video: 
                await client.send_video(target_channel, message.video.file_id)
            
            # Matn qismi (4096 belgidan bo'lib yuborish)
            for i in range(0, len(text), 4096):
                await client.send_message(target_channel, text[i:i+4096])

    await app.start()
    print(f"🚀 Bot ishga tushdi! Kuzatilmoqda: {source_channel}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start_bot())
