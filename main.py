import asyncio
import sys
import copy
from flask import Flask
from threading import Thread
import os
from pyrogram import Client, filters, idle
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# Loopni yaratish
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Flask server
flask_app = Flask("")
@flask_app.route("/")
def home(): return "Bot 24/7 rejimida!"
Thread(target=lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080))), daemon=True).start()

# Userbot
app = Client(
    "render_userbot", 
    api_id=int(os.environ.get("API_ID", 31041560)), 
    api_hash=os.environ.get("API_HASH", "9a19946a1c73f1d1652636804903e176"), 
    session_string=os.environ.get("SESSION_STRING", "")
)

# ================= LINKLARNI ALMASHTIRISH FUNKSIYASI =================
def get_edited_message(message: Message):
    text = message.caption or message.text
    if not text: return None, None
    
    # Textni almashtirish
    new_text = text.replace("https://t.me/eltuzar_live", "https://t.me/eltuzaar_uz")
    
    # Entitiesni nusxalash
    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            start = entity.offset
            end = entity.offset + entity.length
            word = text[start:end].upper()
            
            # Linklarni o'zgartirish
            if "LIVE" in word or "MEDIA" in word:
                entity.url = "https://t.me/eltuzaar_uz"
    
    return new_text, entities

# ================= XABARNI USHLASH VA TAHRIRLASH =================
@app.on_message(filters.chat("@tuztuzttt"))
async def forward_and_edit(client: Client, message: Message):
    new_text, new_entities = get_edited_message(message)
    
    try:
        if message.photo:
            await client.send_photo("@eltuzaar_uz", photo=message.photo.file_id, caption=new_text, caption_entities=new_entities)
        elif message.video:
            await client.send_video("@eltuzaar_uz", video=message.video.file_id, caption=new_text, caption_entities=new_entities)
        elif message.text:
            await client.send_message("@eltuzaar_uz", text=new_text, entities=new_entities)
        print("✅ Post muvaffaqiyatli tahrirlanib, yuborildi!")
    except Exception as e:
        print(f"❌ Yuborishda xato: {e}")

async def main():
    await app.start()
    print("🚀 Bot ishga tushdi va linklarni almashtirmoqda!")
    await idle()

if __name__ == "__main__":
    loop.run_until_complete(main())
