import os
import copy
from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType

# Flask sozlamalari
app_flask = Flask(__name__)
@app_flask.route("/")
def home():
    return "Bot 24/7 ishlamoqda"

def run_flask():
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Pyrogram sozlamalari
app = Client("userbot", 
             api_id=int(os.environ.get("API_ID", 0)), 
             api_hash=os.environ.get("API_HASH", ""), 
             session_string=os.environ.get("SESSION_STRING", ""))

def edit_caption_text(message):
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

@app.on_message(filters.chat("tuztuzttt"))
async def forward_handler(client, message):
    TARGET_CHAT = "eltuzar_livee"
    try:
        text, entities = edit_caption_text(message)
        await client.copy_message(
            chat_id=TARGET_CHAT,
            from_chat_id=message.chat.id,
            message_id=message.id,
            caption=text,
            caption_entities=entities
        )
    except Exception as e:
        print(f"Xatolik: {e}")
pass

if __name__ == "__main__":
    # Flaskni alohida thread'da ishga tushiramiz
    Thread(target=run_flask, daemon=True).start()
    
    # Pyrogram'ni boshlashning eng to'g'ri yo'li
    app.run()
