import sys
import copy
import os
import asyncio

# 1. PYROGRAM SYNC NI O'CHIRAMIZ (Bu qism qolishi shart)
class FakeSync:
    def __getattr__(self, name): return None
sys.modules["pyrogram.sync"] = FakeSync()

from flask import Flask
from threading import Thread
from pyrogram import Client, filters, idle
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# ================= SERVER =================
flask_app = Flask("")
@flask_app.route("/")
def home(): return "Bot 24/7 ishlamoqda!"
Thread(target=lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080))), daemon=True).start()

# ================= USERBOT SOZLAMALARI =================
SOURCE_CHANNEL = "@tuztuzttt"
TARGET_CHANNEL = "@eltuzaar_uz"

# Client'ni global yaratamiz, lekin start() ni loop ichida qilamiz
app = Client(
    "render_userbot", 
    api_id=int(os.environ.get("API_ID", 31041560)), 
    api_hash=os.environ.get("API_HASH", "9a19946a1c73f1d1652636804903e176"), 
    session_string=os.environ.get("SESSION_STRING", "")
)

# ================= MANTIQ =================
def edit_caption_text(message: Message):
    text = message.caption or message.text
    if not text: return "", []

    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    
    # Linklarni o'zgartirish
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            # Matnni qismini olib, katta harflarga o'tkazamiz (tekshirish uchun)
            word = text[entity.offset : entity.offset + entity.length].upper()

            if any(x in word for x in ["ХАБАРИНГИЗНИ", "ЮБОРМОҚЧИ", "УШБУ"]):
                entity.url = "https://t.me/eltuzar_uz_bot"
            elif "LIVE" in word or "MEDIA" in word:
                entity.url = "https://t.me/eltuzaar_uz"
            elif "X" in word and len(word) == 1:
                entity.url = "https://x.com/eltuzar_uz"
            elif "INSTAGRAM" in word:
                entity.url = "https://www.instagram.com/eltuzar_uz"
            elif "FACEBOOK" in word:
                entity.url = "https://www.facebook.com/profile.php?id=61585818251235"
                
    return text, entities

@app.on_message(filters.chat(SOURCE_CHANNEL))
async def forward_and_edit(client: Client, message: Message):
    new_text, new_entities = edit_caption_text(message)
    try:
        if message.photo: await client.send_photo(TARGET_CHANNEL, photo=message.photo.file_id, caption=new_text, caption_entities=new_entities)
        elif message.video: await client.send_video(TARGET_CHANNEL, video=message.video.file_id, caption=new_text, caption_entities=new_entities)
        elif message.text: await client.send_message(TARGET_CHANNEL, text=new_text, entities=new_entities)
    except Exception as e: print(f"❌ Xatolik: {e}")

async def start_bot():
    await app.start()
    print("✅ Bot ishga tushdi!")
    await idle() # Bu yerda to'g'ri ishlaydi
    await app.stop()

if __name__ == "__main__":
    asyncio.run(start_bot())
