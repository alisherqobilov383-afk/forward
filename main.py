import sys
import os
import asyncio
import copy

# PYROGRAM SYNC MODULINI O'CHIRAMIZ
class FakeSync:
    def __getattr__(self, name): return None
sys.modules["pyrogram.sync"] = FakeSync()

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
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

Thread(target=run_flask, daemon=True).start()

# ================= YORDAMCHI FUNKSIYALAR =================
def edit_caption_text(message: Message):
    text = message.caption or message.text
    if not text: return "", []
    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            word = text[entity.offset : entity.offset + entity.length].upper()
            if any(x in word for x in ["ХАБАРИНГИЗНИ", "ЮБОРМОҚЧИ", "УШБУ"]):
                entity.url = "https://t.me/eltuzar_uz_bot"
            elif "LIVE" in word or "MEDIA" in word:
                entity.url = "https://t.me/eltuzaar_uz"
            elif "X" in word and len(word) == 1:
                entity.url = "https://x.com/eltuzar_uz"
            elif "INSTAGRAM" in word:
                entity.url = "https://www.instagram.com/eltuzaar_uz"
            elif "FACEBOOK" in word:
                entity.url = "https://www.facebook.com/profile.php?id=61585818251235"
    return text, entities

def split_text_with_entities(text, entities, mid):
    """Matn va entity'larni xavfsiz bo'lish"""
    text1, text2 = text[:mid], text[mid:]
    ent1, ent2 = [], []
    
    for e in entities:
        if e.offset < mid:
            # Agar entity birinchi qismda tugasa
            if e.offset + e.length <= mid:
                ent1.append(e)
            else:
                # Entity kesilib ketsa, uni qisqartiramiz (oddiy yechim)
                e.length = mid - e.offset
                ent1.append(e)
        else:
            # Ikkinchi qismdagi entity'lar
            new_e = copy.deepcopy(e)
            new_e.offset -= mid
            ent2.append(new_e)
    return text1, ent1, text2, ent2

# ================= ASOSIY BOT =================
async def start_bot():
    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_HASH")
    session_string = os.environ.get("SESSION_STRING")
    source_channel = os.environ.get("SOURCE_CHANNEL", "@tuztuzttt")
    target_channel = os.environ.get("TARGET_CHANNEL", "@eltuzaar_uz")

    app = Client("render_userbot", api_id=int(api_id), api_hash=api_hash, session_string=session_string)

    @app.on_message(filters.chat(source_channel))
    async def forward_and_edit(client: Client, message: Message):
        text, entities = edit_caption_text(message)
        text = text or ""
        total_len = len(text)
        
        # 1. Jami < 1024: O'zgarishsiz
        if total_len <= 1024:
            if message.photo: await client.send_photo(target_channel, photo=message.photo.file_id, caption=text, caption_entities=entities)
            elif message.video: await client.send_video(target_channel, video=message.video.file_id, caption=text, caption_entities=entities)
            elif message.text: await client.send_message(target_channel, text=text, entities=entities)
        
        # 2 va 3. Media bor (Ajratish kerak)
        elif (message.photo or message.video):
            if message.photo: await client.send_photo(target_channel, photo=message.photo.file_id)
            elif message.video: await client.send_video(target_channel, video=message.video.file_id)
            
            # Matn > 4096 bo'lsa 2 ga bo'lish, bo'lmasa oddiy yuborish
            if total_len > 4096:
                mid = total_len // 2
                t1, e1, t2, e2 = split_text_with_entities(text, entities, mid)
                await client.send_message(target_channel, text=t1, entities=e1)
                await client.send_message(target_channel, text=t2, entities=e2)
            else:
                await client.send_message(target_channel, text=text, entities=entities)
        
        # 4. Media yo'q va Matn > 4096
        else:
            if total_len > 4096:
                mid = total_len // 2
                t1, e1, t2, e2 = split_text_with_entities(text, entities, mid)
                await client.send_message(target_channel, text=t1, entities=e1)
                await client.send_message(target_channel, text=t2, entities=e2)
            else:
                await client.send_message(target_channel, text=text, entities=entities)

    await app.start()
    print(f"🚀 Bot ishga tushdi! Kuzatilmoqda: {source_channel}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start_bot())
