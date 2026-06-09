import sys
import os
import asyncio
import copy

# Render muhitida Pyrogram sync xatosini oldini olish
import pyrogram
sys.modules["pyrogram.sync"] = None

from flask import Flask
from threading import Thread
from pyrogram import Client
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# ================= SERVER (UPTIME) =================
flask_app = Flask("")
@flask_app.route("/")
def home(): return "Bot 24/7 ishlamoqda!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

Thread(target=run_flask, daemon=True).start()

# ================= MANTIQ FUNKSIYALARI =================

def edit_caption_ch1(message: Message):
    text = message.caption or message.text or ""
    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            word = text[entity.offset : entity.offset + entity.length].upper()
            if any(x in word for x in ["ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ", "ЮБОРМОҚЧИ", "УШБУ"]):
                entity.url = "https://t.me/eltuzar_uz_bot"
            elif "LIVE" in word: entity.url = "https://t.me/eltuzar_livee"
            elif "MEDIA" in word: entity.url = "https://t.me/eltuzar_mediaa"
            elif "X" in word and len(word) == 1: entity.url = "https://x.com/eltuzar_uz"
            elif "INSTAGRAM" in word: entity.url = "https://www.instagram.com/eltuzaar_uz"
            elif "FACEBOOK" in word: entity.url = "https://www.facebook.com/profile.php?id=61585818251235"
    return text, entities

def edit_caption_ch2(message: Message):
    text = message.caption or message.text or ""
    footer = "\n\n[ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ 👈](https://t.me/eltuzar_uz_bot)"
    return f"{text}{footer}", []

def edit_caption_ch3(message: Message):
    text = message.caption or message.text or ""
    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    # 3-kanal uchun maxsus o'zgartirishlar (agar kerak bo'lsa)
    return text, entities

# ================= ASOSIY BOT =================
async def start_bot():
    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_HASH")
    session_string = os.environ.get("SESSION_STRING")

    S1, T1 = os.environ.get("SOURCE_1", "@eltuzar_live"), os.environ.get("TARGET_1", "@eltuzar_livee")
    S2, T2 = os.environ.get("SOURCE_2", "@eltuzar_media"), os.environ.get("TARGET_2", "@eltuzar_mediaa")
    S3, T3 = os.environ.get("SOURCE_3", "@kanal3"), os.environ.get("TARGET_3", "@target3")

    app = Client("render_userbot", api_id=int(api_id), api_hash=api_hash, session_string=session_string)

    @app.on_message()
    async def forward_and_edit(client: Client, message: Message):
        if not message.chat: return
        chat = f"@{message.chat.username}" if message.chat.username else str(message.chat.id)
        
        # 1-KANAL
        if chat == S1:
            txt, ent = edit_caption_ch1(message)
            try:
                if message.photo: await client.send_photo(T1, photo=message.photo.file_id, caption=txt, caption_entities=ent)
                elif message.text: await client.send_message(T1, text=txt, entities=ent)
            except Exception as e: print(f"Error 1: {e}")

        # 2-KANAL
        if chat == S2:
            txt, _ = edit_caption_ch2(message)
            try:
                if message.photo: await client.send_photo(T2, photo=message.photo.file_id, caption=txt)
                elif message.text: await client.send_message(T2, text=txt)
            except Exception as e: print(f"Error 2: {e}")

        # 3-KANAL
        if chat == S3:
            txt, ent = edit_caption_ch3(message)
            try:
                if message.photo: await client.send_photo(T3, photo=message.photo.file_id, caption=txt, caption_entities=ent)
                elif message.text: await client.send_message(T3, text=txt, entities=ent)
            except Exception as e: print(f"Error 3: {e}")

    await app.start()
    print("🚀 Bot ishga tushdi va 3 ta kanalni alohida kuzatmoqda!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot())
