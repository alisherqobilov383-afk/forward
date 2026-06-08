import sys
import os
import asyncio
import copy

# 1. PYROGRAM SYNC MODULINI O'CHIRAMIZ (Python 3.14 xatosi uchun)
sys.modules["pyrogram.sync"] = None

# 2. LOOPNI BIRINCHI BO'LIB YARATAMIZ
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# ================= SERVER (UPTIME) =================
flask_app = Flask(__name__)
@flask_app.route("/")
def home(): return "Bot 24/7 ishlamoqda!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

Thread(target=run_flask, daemon=True).start()

# ================= BOT CONFIG =================
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# Botni ishga tushirish
app = Client(
    "render_userbot", 
    api_id=int(API_ID) if API_ID else 0, 
    api_hash=API_HASH, 
    session_string=SESSION_STRING
)

# ================= MANTIQ =================
def edit_logic(message: Message):
    text = message.caption or message.text
    if not text: return None, []
    
    # Linklarni almashtirish
    new_text = text.replace("https://t.me/eltuzar_live", "https://t.me/eltuzaar_uz")
    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            start = entity.offset
            end = entity.offset + entity.length
            word = text[start:end].upper()
            if "LIVE" in word or "MEDIA" in word:
                entity.url = "https://t.me/eltuzaar_uz"
    return new_text, entities

@app.on_message(filters.chat("@tuztuzttt"))
async def forwarder(client: Client, message: Message):
    new_text, new_entities = edit_logic(message)
    try:
        if message.photo:
            await client.send_photo("@eltuzaar_uz", photo=message.photo.file_id, caption=new_text, caption_entities=new_entities)
        elif message.video:
            await client.send_video("@eltuzaar_uz", video=message.video.file_id, caption=new_text, caption_entities=new_entities)
        elif message.text:
            await client.send_message("@eltuzaar_uz", text=new_text, entities=new_entities)
    except Exception as e:
        print(f"Xabar uzatishda xato: {e}")

# ================= ISHGA TUSHIRISH =================
async def main():
    await app.start()
    print("🚀 Bot muvaffaqiyatli ishga tushdi!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop.run_until_complete(main())
