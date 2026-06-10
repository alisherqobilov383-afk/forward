import os
import copy
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# 1. Flask server (Bot 24/7 ishlashi uchun)
app_flask = Flask(__name__)
@app_flask.route("/")
def home():
    return "Bot 24/7 ishlamoqda"

def run_flask():
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# 2. Userbot sozlamalari
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# 3. Matnni tahrirlash funksiyasi
def edit_caption_text(message: Message):
    text = message.caption or message.text or ""
    if not text: return "", []
    
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

# 4. Handler: Username yordamida ishlash
# @tuztuzttt dan olib, @eltuzar_livee ga yuboradi
@app.on_message(filters.chat("tuztuzttt")) 
async def forward_handler(client, message):
    TARGET_CHAT = "eltuzar_livee"
    try:
        new_text, new_entities = edit_caption_text(message)
        
        # copy_message - barcha media turlari uchun eng ishonchli usul
        await client.copy_message(
            chat_id=TARGET_CHAT,
            from_chat_id=message.chat.id,
            message_id=message.id,
            caption=new_text,
            caption_entities=new_entities
        )
        print("Xabar muvaffaqiyatli yuborildi!")
        
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

# 5. Ishga tushirish
if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    app.run()
