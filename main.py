import os
import asyncio
import sys
import copy
import threading

# 1. Pyrogram sync xatosini bloklash (Importlardan oldin)
sys.modules["pyrogram.sync"] = None

from flask import Flask
from pyrogram import Client
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# ================= SERVER (UPTIME) =================
flask_app = Flask("")
@flask_app.route("/")
def home(): return "Bot 24/7 ishlamoqda!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Flaskni alohida oqimda ishga tushirish
threading.Thread(target=run_flask, daemon=True).start()

# ================= ALOHIDA MANTIQ FUNKSIYALARI =================

def process_channel_1(message: Message):
    text = message.caption or message.text or ""
    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            word = text[entity.offset : entity.offset + entity.length].upper()
            if any(x in word for x in ["ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ", "ЮБОРМОҚЧИ", "УШБУ"]):
                entity.url = "https://t.me/eltuzar_uz_bot"
            elif "LIVE" in word: entity.url = "https://t.me/eltuzar_livee"
            elif "MEDIA" in word: entity.url = "https://t.me/eltuzar_mediaa"
    return text, entities

def process_channel_2(message: Message):
    text = message.caption or message.text or ""
    footer = "\n\n[ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ 👈](https://t.me/eltuzar_uz_bot)"
    return f"{text}{footer}", []

def process_channel_3(message: Message):
    text = message.caption or message.text or ""
    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    # 3-kanal uchun maxsus logika (kerak bo'lsa to'ldiring)
    return text, entities

# ================= ASOSIY BOT MANTIQI =================

async def main():
    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_HASH")
    session_string = os.environ.get("SESSION_STRING")

    S1, T1 = os.environ.get("SOURCE_1"), os.environ.get("TARGET_1")
    S2, T2 = os.environ.get("SOURCE_2"), os.environ.get("TARGET_2")
    S3, T3 = os.environ.get("SOURCE_3"), os.environ.get("TARGET_3")

    app = Client("render_userbot", api_id=int(api_id), api_hash=api_hash, session_string=session_string)

    @app.on_message()
    async def forward_and_edit(client: Client, message: Message):
        if not message.chat: return
        chat = f"@{message.chat.username}" if message.chat.username else str(message.chat.id)
        
        # 1-KANAL
        if chat == S1:
            txt, ent = process_channel_1(message)
            try:
                if message.photo: await client.send_photo(T1, photo=message.photo.file_id, caption=txt, caption_entities=ent)
                elif message.text: await client.send_message(T1, text=txt, entities=ent)
            except Exception as e: print(f"Error 1: {e}")

        # 2-KANAL
        if chat == S2:
            txt, _ = process_channel_2(message)
            try:
                if message.photo: await client.send_photo(T2, photo=message.photo.file_id, caption=txt)
                elif message.text: await client.send_message(T2, text=txt)
            except Exception as e: print(f"Error 2: {e}")

        # 3-KANAL
        if chat == S3:
            txt, ent = process_channel_3(message)
            try:
                if message.photo: await client.send_photo(T3, photo=message.photo.file_id, caption=txt, caption_entities=ent)
                elif message.text: await client.send_message(T3, text=txt, entities=ent)
            except Exception as e: print(f"Error 3: {e}")

    await app.start()
    print("🚀 Bot ishga tushdi va kuzatmoqda!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    # Render muhitida to'g'ri ishlashi uchun loopni qo'lda boshqaramiz
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
