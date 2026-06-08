import asyncio
import sys
import copy
from flask import Flask
from threading import Thread
import os
from pyrogram import Client, filters, idle
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# ================= KANAL SOZLAMALARI =================
# Kanal nomlarini shu yerdan o'zgartiring:
SOURCE_CHANNEL = "@tuztuzttt"    # Kuzatiladigan kanal
TARGET_CHANNEL = "@wergfdgsdfsfwerw"  # Xabar tashlanadigan kanal

# ================= ASOSIY SOZLAMALAR =================
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Flask server (Render uchun)
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
    # Matn yoki sarlavhani olish
    text = message.caption or message.text
    if not text: return None, []
    
    # Matnni o'zgartirish
    new_text = text.replace("https://t.me/eltuzar_live", "https://t.me/eltuzaar_uz")
    
    # Linklarni tahrirlash uchun eski entitylarni nusxalash
    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            start = entity.offset
            end = entity.offset + entity.length
            word = text[start:end].upper()
            
            # Agar so'z "LIVE" yoki "MEDIA" bo'lsa, linkni o'zgartirish
            if "LIVE" in word or "MEDIA" in word:
                entity.url = "https://t.me/eltuzaar_uz"
    
    return new_text, entities

# ================= XABARNI USHLASH VA YUBORISH =================
@app.on_message(filters.chat(SOURCE_CHANNEL))
async def forward_and_edit(client: Client, message: Message):
    new_text, new_entities = get_edited_message(message)
    
    try:
        if message.photo:
            await client.send_photo(TARGET_CHANNEL, photo=message.photo.file_id, caption=new_text, caption_entities=new_entities)
        elif message.video:
            await client.send_video(TARGET_CHANNEL, video=message.video.file_id, caption=new_text, caption_entities=new_entities)
        elif message.text:
            await client.send_message(TARGET_CHANNEL, text=new_text, entities=new_entities)
        print(f"✅ Xabar muvaffaqiyatli yuborildi: {TARGET_CHANNEL}")
    except Exception as e:
        print(f"❌ Yuborishda xato: {e}")

# ================= BOTNI ISHGA TUSHIRISH =================
async def main():
    await app.start()
    print("🚀 Bot ishga tushdi va linklarni almashtirmoqda!")
    
    # Kanallarni tekshirish
    try:
        await app.get_chat(SOURCE_CHANNEL)
        await app.get_chat(TARGET_CHANNEL)
        print("✅ Kanallar topildi!")
    except Exception as e:
        print(f"⚠️ Kanallarni tekshirishda xato: {e}")
        
    await idle()

if __name__ == "__main__":
    loop.run_until_complete(main())
