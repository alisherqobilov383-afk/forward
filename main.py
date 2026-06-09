import copy
import os
import asyncio
import time

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
    return "Bot 24/7 rejimida muvaffaqiyatli ishlayapti!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

Thread(target=run_flask, daemon=True).start()
print("🌐 Web-server Render uchun muvaffaqiyatli ishga tushdi...")


# ================= USERBOT SOZLAMALARI =================
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

SOURCE_CHANNEL = "@eltuzar_live"
TARGET_CHANNEL = "@eltuzar_livee"

app = Client("render_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# ================= GIPERSILKALARNI O'ZGARTIRISH =================
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


# ================= XABARLARNI USHLASH =================
# filters.chat ni olib tashladik, chunki u Peer id invalid xatosini beryapti
@app.on_message() 
async def forward_and_edit(client: Client, message: Message):
    # Kanal username'ini to'g'ri formatga keltiramiz
    chat_identifier = f"@{message.chat.username}" if message.chat.username else str(message.chat.id)
    
    # SOURCE_CHANNELS ro'yxatida bormi yoki yo'qligini tekshiramiz
    if chat_identifier in SOURCE_CHANNELS:
        try:
            # Qaysi targetga yuborishni aniqlab olamiz
            idx = SOURCE_CHANNELS.index(chat_identifier)
            target = TARGET_CHANNELS[idx]
            
            # Matn va entitylarni ishlash
            new_text, new_entities = edit_caption_text(message)
            if not new_text: return

            # Yuborish
            if message.photo:
                await client.send_photo(chat_id=target, photo=message.photo.file_id, caption=new_text, caption_entities=new_entities)
            elif message.video:
                await client.send_video(chat_id=target, video=message.video.file_id, caption=new_text, caption_entities=new_entities)
            elif message.audio or message.voice:
                file_id = message.audio.file_id if message.audio else message.voice.file_id
                await client.send_audio(chat_id=target, audio=file_id, caption=new_text, caption_entities=new_entities)
            elif message.text:
                await client.send_message(chat_id=target, text=new_text, entities=new_entities)
                
            print(f"✅ Xabar {chat_identifier} dan {target} ga muvaffaqiyatli yuborildi!")
            
        except Exception as e:
            print(f"❌ Xabar uzatishda xatolik: {e}")


# ================= BOTNI 24/7 ISHLATISH VA AVTO-RESTART =================
async def main():
    while True:
        try:
            print("🚀 Bot ishga tushirilmoqda...")
            await app.start()
            print("✅ Bot onlayn!")
            await asyncio.Future()  # Botni to'xtamasdan ushlab turadi
        except Exception as e:
            print(f"⚠️ Xatolik yuz berdi: {e}. 5 soniyadan so'ng qayta ishga tushiriladi...")
            await asyncio.sleep(5)
        finally:
            await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
