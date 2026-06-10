import os
import copy
import asyncio
import logging
from threading import Thread

from flask import Flask
from pyrogram import Client, filters, idle
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# ================== LOGGING ==================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ================== FLASK ==================
app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "Bot 24/7 ishlamoqda"

def run_flask():
    app_flask.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        debug=False,
        use_reloader=False
    )

# ================== PYROGRAM CONFIG ==================
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

app = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# ================== TEXT EDIT ==================
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
            word = text[entity.offset:entity.offset + entity.length].upper()
            for key, val in links.items():
                if key in word:
                    entity.url = val

    return text, entities

# ================== HANDLER ==================
TARGET_CHAT = "eltuzar_livee"

@app.on_message(filters.chat("tuztuzttt"))
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

        logging.info("Message copied successfully")

    except Exception as e:
        logging.error(f"Xatolik: {e}")

# ================== RUN BOT WITH RECONNECT ==================
async def run_bot():
    while True:
        try:
            logging.info("Bot ishga tushyapti...")
            await app.start()
            logging.info("Bot ishlayapti!")

            await idle()

        except Exception as e:
            logging.error(f"Bot crash bo‘ldi: {e}")
            await asyncio.sleep(5)

        finally:
            try:
                await app.stop()
            except:
                pass
            logging.info("Qayta ulanmoqda...")

# ================== MAIN ==================
if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()

    asyncio.run(run_bot())
