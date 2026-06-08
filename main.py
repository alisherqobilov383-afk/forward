import sys
import copy
import os
import asyncio

# 1. PYTHON 3.14 UCHUN PYROGRAM SYNC XATOSINI TO'SISh
class FakeSync:
    def __getattr__(self, name): return None
sys.modules["pyrogram.sync"] = FakeSync()

from flask import Flask
from threading import Thread
from pyrogram import Client, filters, idle
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# ================= RENDER UCHUN VEB SERVER =================
flask_app = Flask("")
@flask_app.route("/")
def home(): return "Bot 24/7 rejimida ishlamoqda!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

Thread(target=run_flask, daemon=True).start()

# ================= GIPERSILKALARNI O'ZGARTIRISH =================
def edit_caption_text(message: Message):
    text = message.caption or message.text
    if not text: return "", []

    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            # Matnni katta harfga o'tkazib tekshiramiz
            word = text[entity.offset : entity.offset + entity.length].upper()

            if any(x in word for x in ["ХАБАРИНГИЗНИ", "ЮБОРМОҚЧИ", "УШБУ"]):
                entity.url = "https://t.me/eltuzar_uz_bot"
            elif "LIVE" in word:
                entity.url = "https://t.me/eltuzaar_uz"
            elif "MEDIA" in word:
                entity.url = "https://t.me/eltuzaar_uz"
            elif "X" in word and len(word) == 1:
                entity.url = "https://x.com/eltuzar_uz"
            elif "INSTAGRAM" in word:
                entity.url = "https://www.instagram.com/eltuzaar_uz"
            elif "FACEBOOK" in word:
                entity.url = "https://www.facebook.com/profile.php?id=61585818251235"
    return text, entities

# ================= ASOSIY BOT QISMI =================
async def start_bot():
    # Sozlamalarni Environment'dan o'qiymiz
    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_HASH")
    session_string = os.environ.get("SESSION_STRING")
    source_channel = os.environ.get("SOURCE_CHANNEL", "@tuztuzttt")
    target_channel = os.environ.get("TARGET_CHANNEL", "@eltuzaar_uz")

    if not api_id or not api_hash:
        print("❌ XATOLIK: API_ID yoki API_HASH topilmadi!")
        return

    # Client'ni loop ichida yaratamiz (Python 3.14 uchun shart)
    app = Client("render_userbot", api_id=int(api_id), api_hash=api_hash, session_string=session_string)

    @app.on_message(filters.chat(source_channel))
    async def forward_and_edit(client: Client, message: Message):
        new_text, new_entities = edit_caption_text(message)
        try:
            if message.photo:
                await client.send_photo(target_channel, photo=message.photo.file_id, caption=new_text, caption_entities=new_entities)
            elif message.video:
                await client.send_video(target_channel, video=message.video.file_id, caption=new_text, caption_entities=new_entities)
            elif message.audio or message.voice:
                await client.send_audio(target_channel, audio=(message.audio or message.voice).file_id, caption=new_text, caption_entities=new_entities)
            elif message.text:
                await client.send_message(target_channel, text=new_text, entities=new_entities)
        except Exception as e:
            print(f"❌ Xatolik: {e}")

    await app.start()
    print(f"✅ Bot {source_channel} kanalini kuzatmoqda!")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(start_bot())
