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

def split_text_smart(text, entities, limit=4096):
    """Matnni va linklarni buzmaydigan qilib qismlarga ajratadi"""
    parts = []
    current_idx = 0
    
    while current_idx < len(text):
        split_point = min(current_idx + limit, len(text))
        
        # Kesish nuqtasi link ichiga tushib qolsa, linkdan oldinroq kesamiz
        for ent in entities:
            if ent.type == MessageEntityType.TEXT_LINK:
                if ent.offset < split_point < (ent.offset + ent.length):
                    split_point = ent.offset
        
        part_text = text[current_idx:split_point]
        part_entities = []
        for ent in entities:
            if current_idx <= ent.offset < split_point:
                new_ent = copy.deepcopy(ent)
                new_ent.offset -= current_idx
                # Agar entity kesilib qolsa, uni sig'adigan qilib kesamiz
                if new_ent.offset + new_ent.length > len(part_text):
                    new_ent.length = len(part_text) - new_ent.offset
                part_entities.append(new_ent)
        
        parts.append((part_text, part_entities))
        current_idx = split_point
        if current_idx == split_point: # Infinite loop oldini olish
            current_idx += 1
            
    return parts

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
        
        # 1. Jami <= 1024 (Media + Matn birga)
        if total_len <= 1024:
            if
