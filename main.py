import sys
import os
import asyncio
import copy
from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# PYROGRAM SYNC MODULINI O'CHIRISH
class FakeSync:
    def __getattr__(self, name): return None
sys.modules["pyrogram.sync"] = FakeSync()

# ================= SERVER (UPTIME) =================
flask_app = Flask("")
@flask_app.route("/")
def home(): return "Bot 24/7 ishlamoqda!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

Thread(target=run_flask, daemon=True).start()

# ================= MANTIQ FUNKSIYALARI =================

def process_links(message: Message):
    """Linklarni tahrirlash uchun universal funksiya"""
    text = message.caption or message.text
    if not text: return "", []
    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            word = text[entity.offset : entity.offset + entity.length].upper()
            if any(x in word for x in ["ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ", "ЮБОРМОҚЧИ", "УШБУ"]):
                entity.url = "https://t.me/eltuzar_uz_bot"
            elif "LIVE" in word:
                entity.url = "https://t.me/eltuzar_livee"
            elif "MEDIA" in word:
                entity.url = "https://t.me/eltuzar_mediaa"
            elif "X" in word and len(word) == 1:
                entity.url = "https://x.com/eltuzar_uz"
            elif "INSTAGRAM" in word:
                entity.url = "https://www.instagram.com/eltuzaar_uz"
            elif "FACEBOOK" in word:
                entity.url = "https://www.facebook.com/profile.php?id=61585818251235"
    return text, entities

# ================= ASOSIY BOT =================
async def start_bot():
    app = Client("render_userbot", 
                 api_id=int(os.environ.get("API_ID")), 
                 api_hash=os.environ.get("API_HASH"), 
                 session_string=os.environ.get("SESSION_STRING"))

    S1, T1 = os.environ.get("SOURCE_1"), os.environ.get("TARGET_1")
    S2, T2 = os.environ.get("SOURCE_2"), os.environ.get("TARGET_2")
    S3, T3 = os.environ.get("SOURCE_3"), os.environ.get("TARGET_3")

    # 1-KANAL UCHUN ALOHIDA HANDLER
    @app.on_message(filters.chat(S1))
    async def handler_1(client: Client, message: Message):
        txt, ent = process_links(message)
        try:
            await message.copy(T1, caption=txt, caption_entities=ent)
        except Exception as e: print(f"Error Channel 1: {e}")

    # 2-KANAL UCHUN ALOHIDA HANDLER
    @app.on_message(filters.chat(S2))
    async def handler_2(client: Client, message: Message):
        text = message.caption or message.text or ""
        footer = "\n\n[ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ 👈](https://t.me/eltuzar_uz_bot)"
        try:
            await message.copy(T2, caption=f"{text}{footer}")
        except Exception as e: print(f"Error Channel 2: {e}")

    # 3-KANAL UCHUN ALOHIDA HANDLER
    @app.on_message(filters.chat(S3))
    async def handler_3(client: Client, message: Message):
        # 3-kanal uchun boshqa logika kerak bo'lsa shu yerda yozasiz
        txt, ent = process_links(message)
        try:
            await message.copy(T3, caption=txt, caption_entities=ent)
        except Exception as e: print(f"Error Channel 3: {e}")

    await app.start()
    print("🚀 Bot ishga tushdi va 3 ta kanal alohida nazorat qilinmoqda!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start_bot())
