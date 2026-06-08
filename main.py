import asyncio
import os
import copy

# 1. Loopni birinchi bo'lib yaratamiz
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 2. Pyrogram import qilishdan oldin sync ni bloklaymiz
import sys
class FakeSync:
    def __getattr__(self, name): return None
sys.modules["pyrogram.sync"] = FakeSync()

# 3. Keyin qolganini import qilamiz
from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# Render uchun server
flask_app = Flask("")
@flask_app.route("/")
def home(): return "Bot ishlamoqda!"
Thread(target=lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080))), daemon=True).start()

# Bot sozlamalari
SOURCE_CHANNEL = "@tuztuzttt"
TARGET_CHANNEL = "@eltuzaar_uz"

app = Client(
    "render_userbot", 
    api_id=int(os.environ.get("API_ID", 31041560)), 
    api_hash=os.environ.get("API_HASH", "9a19946a1c73f1d1652636804903e176"), 
    session_string=os.environ.get("SESSION_STRING", "")
)

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
    except Exception as e:
        print(f"Xatolik: {e}")

async def main():
    await app.start()
    print("🚀 Bot muvaffaqiyatli ishga tushdi!")
    # 'idle()' ishlatmasdan o'zimiz loopni ushlab turamiz
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop.run_until_complete(main())
