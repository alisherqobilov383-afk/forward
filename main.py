import os
import asyncio
from flask import Flask
from threading import Thread
from pyrogram import Client, filters, idle
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
import copy

# ================= RENDER UCHUN VEB SERVER =================
flask_app = Flask("")

@flask_app.route("/")
def home():
    return "Bot 24/7 rejimida muvaffaqiyatli ishlamoqda!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

Thread(target=run_flask, daemon=True).start()

# ================= USERBOT SOZLAMALARI =================
API_ID = int(os.environ.get("API_ID", 31041560))  
API_HASH = os.environ.get("API_HASH", "9a19946a1c73f1d1652636804903e176")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

SOURCE_CHANNEL = "@tuztuzttt"
TARGET_CHANNEL = "@eltuzaar_uz"

# Pyrogram clientini yaratamiz
app = Client(
    "render_userbot", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    session_string=SESSION_STRING if SESSION_STRING else None
)

# ================= TAYYORLASH FUNKSIYASI =================
def edit_caption_text(message: Message):
    text = message.caption or message.text
    if not text: return None, []
    
    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    
    # Linklarni almashtirish
    text = text.replace("https://t.me/eltuzar_live", "https://t.me/eltuzaar_uz")
    
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            start = entity.offset
            end = entity.offset + entity.length
            word = text[start:end].upper()
            
            if "LIVE" in word or "MEDIA" in word:
                entity.url = "https://t.me/eltuzaar_uz"
    
    return text, entities

# ================= XABARNI USHLASH =================
@app.on_message(filters.chat(SOURCE_CHANNEL))
async def forward_and_edit(client: Client, message: Message):
    try:
        new_text, new_entities = edit_caption_text(message)
        
        if message.photo:
            await client.send_photo(TARGET_CHANNEL, photo=message.photo.file_id, caption=new_text, caption_entities=new_entities)
        elif message.video:
            await client.send_video(TARGET_CHANNEL, video=message.video.file_id, caption=new_text, caption_entities=new_entities)
        elif message.text:
            await client.send_message(TARGET_CHANNEL, text=new_text, entities=new_entities)
    except Exception as e:
        print(f"Xatolik: {e}")

# ================= ASOSIY ISHGA TUSHIRISH =================
async def main():
    print("🚀 Bot ishga tushmoqda...")
    await app.start()
    print("✅ Bot jonli rejimda!")
    await idle()
    await app.stop()

if __name__ == "__main__":
    # Python 3.14 uchun eng toza usul
    asyncio.run(main())
