import asyncio
import sys
import os
import copy
from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# 1. Loopni yaratish va Sync ni bloklash
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

class FakeSync:
    def __getattr__(self, name): return None
sys.modules["pyrogram.sync"] = FakeSync()

# 2. Flask server
flask_app = Flask("")
@flask_app.route("/")
def home(): return "Bot 24/7 rejimida!"
Thread(target=lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080))), daemon=True).start()

# 3. Xavfsiz sozlamalar (API ma'lumotlarini Render'dan o'qiydi)
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

if not API_ID or not API_HASH:
    print("❌ XATOLIK: API_ID yoki API_HASH topilmadi! Render'dagi Environment Variables ni tekshiring.")
    sys.exit(1)

app = Client(
    "render_userbot", 
    api_id=int(API_ID), 
    api_hash=API_HASH, 
    session_string=SESSION_STRING
)

SOURCE_CHANNEL = "@tuztuzttt"
TARGET_CHANNEL = "@eltuzaar_uz"

# 4. Link almashtirish funksiyasi
def get_edited_message(message: Message):
    text = message.caption or message.text
    if not text: return None, []
    
    new_text = text.replace("https://t.me/eltuzar_live", "https://t.me/eltuzaar_uz")
    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            start = entity.offset
            end = entity.offset + entity.length
            word = text[start:end].upper()
            if "LIVE" in word or "MEDIA" in word:
                entity.url = "https://t.me/eltuzaar_uz"
    return new_text, entities

# 5. Xabarni ushlash
@app.on_message(filters.chat(SOURCE_CHANNEL))
async def forward_and_edit(client: Client, message: Message):
    new_text, new_entities = get_edited_message(message)
    try:
        if message.photo:
            await client.send_photo(TARGET_CHANNEL, photo=message.photo.file_id, caption=new_text, caption_entities=new_entities)
        elif message.video:
            await client.send_video(TARGET_CHANNEL, video=message.video.file_id, caption=new_text, caption_entities=new_entities)
        elif message.text:
            await client.send_message(TARGET_CHANNEL, text=new_text, entities=new_entities)
        print("✅ Post muvaffaqiyatli tahrirlanib, yuborildi!")
    except Exception as e:
        print(f"❌ Yuborishda xato: {e}")

# 6. Botni ishga tushirish
async def main():
    await app.start()
    print("🚀 Bot xavfsiz ishga tushdi!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop.run_until_complete(main())
