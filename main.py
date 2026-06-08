import sys
import os
import asyncio
import copy

# 1. PYROGRAM SYNC MODULINI O'CHIRAMIZ
class FakeSync:
    def __getattr__(self, name): return None
sys.modules["pyrogram.sync"] = FakeSync()

from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# ================= SERVER (UPTIME) =================
flask_app = Flask("")
@flask_app.route("/")
def home(): return "Bot 24/7 ishlamoqda!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

Thread(target=run_flask, daemon=True).start()

# ================= MANTIQ FUNKSIYASI =================
def edit_caption_text(message: Message):
    text = message.caption or message.text
    if not text: return "", []
    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            word = text[entity.offset : entity.offset + entity.length].upper()
            if any(x in word for x in ["ХАБАРИНГИЗНИ", "ЮБОРМОҚЧИ", "УШБУ"]):
                entity.url = "https://t.me/eltuzar_uz_bot"
            elif "LIVE" in word or "MEDIA" in word:
                entity.url = "https://t.me/eltuzaar_uz"
            elif "X" in word and len(word) == 1:
                entity.url = "https://x.com/eltuzar_uz"
            elif "INSTAGRAM" in word:
                entity.url = "https://www.instagram.com/eltuzaar_uz"
            elif "FACEBOOK" in word:
                entity.url = "https://www.facebook.com/profile.php?id=61585818251235"
    return text, entities

# ================= ASOSIY BOT =================
async def start_bot():
    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_HASH")
    session_string = os.environ.get("SESSION_STRING")
    source_channel = os.environ.get("SOURCE_CHANNEL", "@tuztuzttt")
    target_channel = os.environ.get("TARGET_CHANNEL", "@eltuzaar_uz")

    app = Client("render_userbot", api_id=int(api_id), api_hash=api_hash, session_string=session_string)

    footer = (
        "\n\n👇 Давоми\n\n"
        "Расмий саҳифаларимизга обуна бўлинг:\n"
        "RASMIY | LIVE | MEDIA  | MUHOKAMALR UCHUN !!!"
    )

    @app.on_message(filters.chat(source_channel))
    async def forward_and_edit(client: Client, message: Message):
        text, entities = edit_caption_text(message)
        
        # SHART: Agar media bor va matn 1024 dan oshsa
        if (message.photo or message.video) and len(text or "") > 1024:
            try:
                # 1. Medianing o'zini faqat footer bilan yuborish
                if message.photo:
                    await client.send_photo(target_channel, photo=message.photo.file_id, caption=footer)
                elif message.video:
                    await client.send_video(target_channel, video=message.video.file_id, caption=footer)
                
                # 2. Matn qismini alohida xabar qilib yuborish
                await client.send_message(target_channel, text=text, entities=entities)
            except Exception as e: print(f"❌ Xatolik (ajratib yuborish): {e}")
        
        else:
            # Oddiy holat (1024 dan oshmasa)
            try:
                if message.photo: await client.send_photo(target_channel, photo=message.photo.file_id, caption=text + footer, caption_entities=entities)
                elif message.video: await client.send_video(target_channel, video=message.video.file_id, caption=text + footer, caption_entities=entities)
                elif message.audio or message.voice: await client.send_audio(target_channel, audio=(message.audio or message.voice).file_id, caption=text + footer, caption_entities=entities)
                elif message.text: await client.send_message(target_channel, text=text + footer, entities=entities)
            except Exception as e: print(f"❌ Xatolik: {e}")

    await app.start()
    print(f"🚀 Bot ishga tushdi!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start_bot())
