import os
import copy
import time
import traceback
from threading import Thread
from flask import Flask

from pyrogram import Client, filters, idle
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# =========================
# Flask (keep alive)
# =========================
app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "Bot 24/7 ishlamoqda"

def run_flask():
    app_flask.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        threaded=True,
        use_reloader=False
    )

# =========================
# Telegram config
# =========================
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

app = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

SOURCE_CHAT = "tuztuzttt"
TARGET_CHAT = "eltuzar_livee"

# =========================
# Caption editor
# =========================
def edit_caption_text(message: Message):
    text = message.caption or message.text or ""

    entities = copy.deepcopy(
        message.caption_entities or message.entities or []
    )

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

            for key, value in links.items():
                if key in word:
                    entity.url = value

    return text, entities

# =========================
# Handler
# =========================
@app.on_message(filters.chat(SOURCE_CHAT))
async def handler(client, message):
    try:
        text, entities = edit_caption_text(message)

        await client.copy_message(
            chat_id=TARGET_CHAT,
            from_chat_id=message.chat.id,
            message_id=message.id,
            caption=text,
            caption_entities=entities
        )

        print("Forward:", message.id)

    except Exception:
        traceback.print_exc()

# =========================
# Auto restart loop
# =========================
def run_bot():
    while True:
        try:
            print("Bot starting...")
            app.start()
            print("Bot started!")

            idle()

        except Exception as e:
            print("Bot crash:", e)
            traceback.print_exc()
            time.sleep(5)

        finally:
            try:
                app.stop()
            except:
                pass

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    run_bot()
