import asyncio
import os
import copy
from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from flask import Flask
from threading import Thread

# 1. Flask server (Render uchun)
app_flask = Flask(__name__)
@app_flask.route("/")
def home():
    return "Bot 24/7 ishlamoqda"

def run_flask():
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# 2. Userbot sozlamalari
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# 3. Linklarni almashtirish funksiyasi (Siz so'ragandek o'zgarishsiz)
def edit_caption_text(message: Message):
    text = message.caption if message.caption else message.text
    if not text:
        return "", []

    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    MY_BOT_LINK = "https://t.me/eltuzar_uz_bot"
    MY_LIVE_LINK = "https://t.me/eltuzar_livee"
    MY_MEDIA_LINK = "https://t.me/eltuzar_mediaa"
    MY_X_LINK = "https://x.com/eltuzar_uz"
    MY_INSTA_LINK = "https://www.instagram.com/eltuzar_uz"
    MY_FB_LINK = "https://www.facebook.com/profile.php?id=61585818251235"

    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            start = entity.offset
            end = entity.offset + entity.length
            word = text[start:end]
            if any(x in word.upper() for x in ["ХАБАРИНГИЗНИ", "ЮБОРМОҚЧИ", "УШБУ"]):
                entity.url = MY_BOT_LINK
            elif "LIVE" in word.upper():
                entity.url = MY_LIVE_LINK
            elif "MEDIA" in word.upper():
                entity.url = MY_MEDIA_LINK
            elif "X" in word.upper() and len(word) == 1:
                entity.url = MY_X_LINK
            elif "INSTAGRAM" in word.upper():
                entity.url = MY_INSTA_LINK
            elif "FACEBOOK" in word.upper():
                entity.url = MY_FB_LINK
    return text, entities

# 4. Handler
@app.on_message()
async def forward_handler(client, message):
    # Bu yerda kanal ID yoki username'ni o'zingizga moslang
    if message.chat and message.chat.username == "eltuzar_live":
        try:
            new_text, new_entities = edit_caption_text(message)
            target = "@eltuzar_livee"
            
            if message.photo:
                await client.send_photo(target, message.photo.file_id, caption=new_text, caption_entities=new_entities)
            elif message.video:
                await client.send_video(target, message.video.file_id, caption=new_text, caption_entities=new_entities)
            elif message.text:
                await client.send_message(target, new_text, entities=new_entities)
            print("Xabar uzatildi.")
        except Exception as e:
            print(f"Xatolik: {e}")

# 5. Asosiy qism (Toza asyncio)
async def main():
    await app.start()
    print("Bot ishga tushdi...")
    await asyncio.Future()

if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    asyncio.run(main())
