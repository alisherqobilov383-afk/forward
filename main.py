import sys
import os
import asyncio
import copy
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
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

Thread(target=run_flask, daemon=True).start()

# ================= MANTIQ FUNKSIYALARI =================

def get_processed_entities(message: Message, links_map: dict):
    text = message.caption or message.text or ""
    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            word = text[entity.offset : entity.offset + entity.length].upper()
            for key, url in links_map.items():
                if key in word:
                    entity.url = url
    return text, entities

# ================= ASOSIY BOT =================
async def start_bot():
    api_id = int(os.environ.get("API_ID"))
    api_hash = os.environ.get("API_HASH")
    session_string = os.environ.get("SESSION_STRING")

    app = Client("render_userbot", api_id=api_id, api_hash=api_hash, session_string=session_string)

    # 1-KANAL UCHUN
    @app.on_message(filters.chat(os.environ.get("SOURCE_1")))
    async def handler_1(client: Client, message: Message):
        links = {
            "ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ": "https://t.me/eltuzar_uz_bot",
            "LIVE": "https://t.me/eltuzar_livee",
            "MEDIA": "https://t.me/eltuzar_mediaa",
            "INSTAGRAM": "https://www.instagram.com/eltuzaar_uz"
        }
        txt, ent = get_processed_entities(message, links)
        await client.copy_message(os.environ.get("TARGET_1"), message.chat.id, message.id, caption=txt, caption_entities=ent)

    # 2-KANAL UCHUN
    @app.on_message(filters.chat(os.environ.get("SOURCE_2")))
    async def handler_2(client: Client, message: Message):
        text = message.caption or message.text or ""
        footer = "\n\n[ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ 👈](https://t.me/eltuzar_uz_bot)"
        await client.copy_message(os.environ.get("TARGET_2"), message.chat.id, message.id, caption=f"{text}{footer}")

    # 3-KANAL UCHUN
    @app.on_message(filters.chat(os.environ.get("SOURCE_3")))
    async def handler_3(client: Client, message: Message):
        links = {"LIVE": "https://t.me/another_link"} # 3-kanal uchun maxsus linklar
        txt, ent = get_processed_entities(message, links)
        await client.copy_message(os.environ.get("TARGET_3"), message.chat.id, message.id, caption=txt, caption_entities=ent)

    await app.start()
    print("🚀 Bot ishga tushdi!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start_bot())
