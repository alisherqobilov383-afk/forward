import os
import copy
import asyncio
from threading import Thread
from flask import Flask
from pyrogram import Client, filters, idle
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# Flask serveri (UptimeRobot/Render uchun)
app_flask = Flask(__name__)
@app_flask.route("/")
def home():
    return "Bot 24/7 ishlamoqda"

def run_flask():
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Environment variable'lardan ma'lumotlarni o'qish
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "") # Pyrogram String Session
SOURCE_CHAT = os.environ.get("SOURCE_CHAT", "tuztuzttt") # Manba
TARGET_CHAT = os.environ.get("TARGET_CHAT", "eltuzar_livee") # Maqsad

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

def edit_caption_text(message: Message):
    text = message.caption or message.text or ""
    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    
    links = {
        "ХАБАРИНГИЗНИ": "https://t.me/eltuzar_uz_bot",
        "LIVE": "https://t.me/eltuzar_livee",
        "MEDIA": "https://t.me/eltuzar_mediaa",
        "X": "https://x.com/eltuzar_uz",
        "INSTAGRAM": "https://www.instagram.com/eltuzar_uz",
        "FACEBOOK": "https://www.facebook.com/profile.php?id=61585818251235"
    }
    
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            word = text[entity.offset:entity.offset+entity.length].upper()
            for key, val in links.items():
                if key in word:
                    entity.url = val
    return text, entities

@app.on_message(filters.chat(SOURCE_CHAT))
async def forward_handler(client, message):
    try:
        text, entities = edit_caption_text(message)
        await client.copy_message(
            chat_id=TARGET_CHAT,
            from_chat_id=message.chat.id,
            message_id=message.id,
            caption=text,
            caption_entities=entities
        )
        print(f"Xabar muvaffaqiyatli uzatildi: {message.id}")
    except Exception as e:
        print(f"Xatolik: {e}")

if __name__ == "__main__":
    # Flask ni fon rejimida ishga tushirish
    Thread(target=run_flask, daemon=True).start()
    
    # Pyrogram ni ishga tushirish
    app.start()
    print("Bot muvaffaqiyatli ishga tushdi!")
    idle()
