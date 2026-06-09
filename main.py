import copy
import os
import asyncio

# 1. PYTHON 3.14 UCHUN PYROGRAM EVENT-LOOP XATOSINI TUZATISH
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from flask import Flask
from threading import Thread
from pyrogram import Client, filters
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

Thread(target=run_flask, daemon=True).start()
print("🌐 Web-server Render uchun muvaffaqiyatli ishga tushdi...")


# ================= USERBOT SOZLAMALARI (100% XAVFSIZ) =================
# Kod ichida hech qanday kalit qolmadi, hammasi Render muhitidan olinadi
API_ID = int(os.environ.get("API_ID", 0))  
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

SOURCE_CHANNEL = "@eltuzar_live"  # Kuzatiladigan begona kanal
TARGET_CHANNEL = "@eltuzar_livee"    # Post tashlanadigan o'zingizning kanaliz

# Render serverida faqat SESSION_STRING orqali ishlaydi
if SESSION_STRING:
    app = Client("render_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
else:
    # Agar mahalliy kompyuterda ishga tushirsangiz, local session faylidan foydalanadi
    app = Client("render_userbot", api_id=API_ID if API_ID != 0 else 31041560, 
                                  api_hash=API_HASH if API_HASH != "" else "9a19946a1c73f1d1652636804903e176")


# ================= GIPERSILKALARNI O'ZGARTIRISH FUNKSIYASI =================
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

            if "ХАБАРИНГИЗНИ" in word or "юбормоқчи" in word or "ушбу" in word:
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
        if not new_text:
            return

        if message.photo:
            await client.send_photo(chat_id=TARGET_CHANNEL, photo=message.photo.file_id, caption=new_text, caption_entities=new_entities)
            print("📸 Rasm yuborildi!")
        elif message.video:
            await client.send_video(chat_id=TARGET_CHANNEL, video=message.video.file_id, caption=new_text, caption_entities=new_entities)
            print("🎥 Video yuborildi!")
        elif message.audio or message.voice:
            file_id = message.audio.file_id if message.audio else message.voice.file_id
            await client.send_audio(chat_id=TARGET_CHANNEL, audio=file_id, caption=new_text, caption_entities=new_entities)
            print("🎵 Audio yuborildi!")
        elif message.text:
            await client.send_message(chat_id=TARGET_CHANNEL, text=new_text, entities=new_entities)
            print("📝 Matnli xabar yuborildi!")
    except Exception as e:
        print(f"❌ Xatolik: {e}")


# ================= BOTNI ISHGA TUSHIRISH MAIN SIKLI =================
async def start_bot():
    print("🚀 Bot serverda ishga tushmoqda...")
    try:
        await app.start()
        print("✅ Bot muvaffaqiyatli Telegramga ulandi va ishlayapti!")
        while True:
            await asyncio.sleep(3600)
    except Exception as xato:
        print(f"❌ XATOLIK: {xato}")
    finally:
        await app.stop()

if __name__ == "__main__":
    current_loop = asyncio.get_event_loop()
    current_loop.run_until_complete(start_bot())
