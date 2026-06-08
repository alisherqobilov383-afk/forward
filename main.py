import sys
import copy
import os
import asyncio

# 1. PYTHON 3.14 UCHUN PYROGRAM SYNC XATOSINI BUTUNLAY TO'SISh
class FakeSync:
    def __getattr__(self, name):
        return None
sys.modules["pyrogram.sync"] = FakeSync()

from flask import Flask
from threading import Thread
from pyrogram import Client, filters, idle
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# ================= RENDER UCHUN VEB SERVER =================
flask_app = Flask("")

@flask_app.route("/")
def home():
    return "Bot 24/7 rejimida muvaffaqiyatli ishlamoqda!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

# Veb-serverni alohida oqimda zudlik bilan yurgizamiz
Thread(target=run_flask, daemon=True).start()
print("🌐 Web-server Render uchun muvaffaqiyatli ishga tushdi...")


# ================= USERBOT SOZLAMALARI (100% XAVFSIZ) =================
API_ID = int(os.environ.get("API_ID", 0))  
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

SOURCE_CHANNEL = "@tuztuzttt"     # Kuzatiladigan begona kanal
TARGET_CHANNEL = "@eltuzaar_uz"    # Post tashlanadigan o'zingizning kanaliz

if SESSION_STRING:
    app = Client("render_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
else:
    app = Client("render_userbot", api_id=API_ID if API_ID != 0 else 31041560, 
                  api_hash=API_HASH if API_HASH != "" else "9a19946a1c73f1d1652636804903e176")


# ================= GIPERSILKALARNI O'ZGARTIRISH FUNKSIYASI =================
def edit_caption_text(message: Message):
    text = message.caption if message.caption else message.text
    
    # Agar postda umuman matn bo'lmasa, bo'sh joy qaytaramiz (lekin return qilib bloklamaymiz)
    if not text:
        return None, []

    entities = copy.deepcopy(message.caption_entities or message.entities or [])

    MY_BOT_LINK = "https://t.me/eltuzar_uz_bot"  
    MY_LIVE_LINK = "https://t.me/eltuzaar_uz"  
    MY_MEDIA_LINK = "https://t.me/eltuzaar_uz"  
    MY_X_LINK = "https://x.com/eltuzar_uz"  
    MY_INSTA_LINK = "https://www.instagram.com/eltuzar_uz"  
    MY_FB_LINK = "https://www.facebook.com/profile.php?id=61585818251235"  

    # 1. Matn ichidagi oddiy yozilgan linklarni (t.me/eltuzar_live) to'g'ridan-to'g'ri almashtirish
    text = text.replace("https://t.me/eltuzar_live", "https://t.me/eltuzaar_uz")
    text = text.replace("@eltuzar_live", "@eltuzaar_uz")

    # 2. Yashirin gipersilkalarni (TEXT_LINK) tahrirlash
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            start = entity.offset
            end = entity.offset + entity.length
            word = text[start:end].upper() # Katta-kichik harflarga sezgirlikni yo'qotamiz

            if "ХАБАРИНГИЗНИ" in word or "ЮБОРМОҚЧИ" in word or "УШБУ" in word:
                entity.url = MY_BOT_LINK
            elif "LIVE" in word:
                entity.url = MY_LIVE_LINK
            elif "MEDIA" in word:
                entity.url = MY_MEDIA_LINK
            elif "X" in word:
                entity.url = MY_X_LINK
            elif "INSTAGRAM" in word:
                entity.url = MY_INSTA_LINK
            elif "FACEBOOK" in word:
                entity.url = MY_FB_LINK

    return text, entities


# ================= XABARLARNI USHLASH VA YUBORISH =================
@app.on_message(filters.chat(SOURCE_CHANNEL))
async def forward_and_edit(client: Client, message: Message):
    try:
        new_text, new_entities = edit_caption_text(message)

        # Agar matn bo'lsa `new_text` yuboriladi, bo'lmasa `None` (matnsiz rasm/video o'taveradi)
        if message.photo:
            await client.send_photo(chat_id=TARGET_CHANNEL, photo=message.photo.file_id, caption=new_text, caption_entities=new_entities)
            print("📸 Rasm muvaffaqiyatli o'tkazildi!")
        elif message.video:
            await client.send_video(chat_id=TARGET_CHANNEL, video=message.video.file_id, caption=new_text, caption_entities=new_entities)
            print("🎥 Video muvaffaqiyatli o'tkazildi!")
        elif message.audio or message.voice:
            file_id = message.audio.file_id if message.audio else message.voice.file_id
            await client.send_audio(chat_id=TARGET_CHANNEL, audio=file_id, caption=new_text, caption_entities=new_entities)
            print("🎵 Audio muvaffaqiyatli o'tkazildi!")
        elif message.text and new_text:
            await client.send_message(chat_id=TARGET_CHANNEL, text=new_text, entities=new_entities)
            print("📝 Matnli xabar muvaffaqiyatli o'tkazildi!")
            
    except Exception as e:
        print(f"❌ Xatolik postni o'tkazishda: {e}")


# ================= BOTNI ISHGA TUSHIRISH (MUTLAQO XAVFSIZ) =================
async def start_bot():
    print("🚀 Bot serverda ishga tushmoqda...")
    try:
        await app.start()
        print("✅ Bot muvaffaqiyatli Telegramga ulandi va jonli rejimda tinglamoqda!")
        
        # Oqimni to'xtatmaydigan eng xavfsiz Pyrogram rejimini yoqamiz
        await idle()
        
    except Exception as xato:
        print(f"❌ XATOLIK: {xato}")
    finally:
        if app.is_connected:
            await app.stop()

if __name__ == "__main__":
    asyncio.run(start_bot())
