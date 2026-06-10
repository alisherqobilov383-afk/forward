import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

# ================= SOZLAMALAR =================
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

# Kanallarni ID formatida yozing (yoki username)
# Misol: MAPPING = {"-100123456789": "-100987654321"}
MAPPING = {
    "@eltuzar_live": "@eltuzar_livee"
}

app = Client("render_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# ================= GIPERSILKALARNI O'ZGARTIRISH =================
def get_new_entities(message: Message, text: str):
    entities = message.caption_entities or message.entities or []
    new_entities = []
    
    MY_LINKS = {
        "ХАБАРИНГИЗНИ": "https://t.me/eltuzar_uz_bot",
        "LIVE": "https://t.me/eltuzar_livee",
        "MEDIA": "https://t.me/eltuzar_mediaa",
        "INSTAGRAM": "https://www.instagram.com/eltuzar_uz",
        "FACEBOOK": "https://www.facebook.com/profile.php?id=61585818251235"
    }

    for entity in entities:
        # Eski linkni saqlab qolamiz yoki yangilaymiz
        new_entities.append(entity)
    return new_entities

# ================= XABARLARNI USHLASH =================
@app.on_message(filters.chat(list(MAPPING.keys())))
async def forward_handler(client: Client, message: Message):
    try:
        source_chat = f"@{message.chat.username}" if message.chat.username else str(message.chat.id)
        target_chat = MAPPING.get(source_chat)
        
        if not target_chat:
            return

        # Matnni olish
        text = message.caption or message.text or ""
        entities = message.caption_entities or message.entities
        
        # Yuborish (copy ishlatish osonroq va xatosiz)
        await message.copy(chat_id=target_chat, caption=text, caption_entities=entities)
        print(f"✅ Uzatildi: {source_chat} -> {target_chat}")

    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        print(f"❌ Xatolik: {e}")

# ================= ISHGA TUSHIRISH =================
async def main():
    await app.start()
    print("🚀 Bot muvaffaqiyatli ishga tushdi!")
    await asyncio.Future()  # Botni ushlab turish

if __name__ == "__main__":
    # Render uchun Flask (alohida thread)
    from flask import Flask
    from threading import Thread
    flask_app = Flask("")
    @flask_app.route("/")
    def home(): return "Bot ishlamoqda"
    Thread(target=lambda: flask_app.run(host="0.0.0.0", port=8080), daemon=True).start()
    
    app.run(main())
