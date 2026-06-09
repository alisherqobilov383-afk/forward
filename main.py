import sys
import os
import asyncio
import copy
from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType

# --- SERVER ---
flask_app = Flask("")
@flask_app.route("/")
def home(): return "Bot 24/7 ishlamoqda!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

Thread(target=run_flask, daemon=True).start()

# --- MANTIQ ---
def get_updated_entities(message):
    text = message.caption or message.text or ""
    entities = copy.deepcopy(message.caption_entities or message.entities or [])
    
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            word = text[entity.offset : entity.offset + entity.length].upper()
            if any(x in word for x in ["ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ", "ЮБОРМОҚЧИ", "УШБУ"]):
                entity.url = "https://t.me/eltuzar_uz_bot"
            elif "LIVE" in word:
                entity.url = "https://t.me/eltuzar_livee"
            elif "MEDIA" in word:
                entity.url = "https://t.me/eltuzar_mediaa"
            elif "X" in word and len(word) == 1:
                entity.url = "https://x.com/eltuzar_uz"
            elif "INSTAGRAM" in word:
                entity.url = "https://www.instagram.com/eltuzaar_uz"
            elif "FACEBOOK" in word:
                entity.url = "https://www.facebook.com/profile.php?id=61585818251235"
    return entities

async def start_bot():
    app = Client(
        "render_userbot", 
        api_id=int(os.environ.get("API_ID")), 
        api_hash=os.environ.get("API_HASH"), 
        session_string=os.environ.get("SESSION_STRING")
    )

    # Manzillar
    S1, T1 = "@tuztuzttt", "@wergfdgsdfsfwerw"
    S2, T2 = "@eltuzar_media", "@eltuzar_mediaa"

    # 1-KANAL HANDLERI
    @app.on_message(filters.chat(S1))
    async def handler_1(client, message):
        ents = get_updated_entities(message)
        try:
            await client.copy_message(
                chat_id=T1,
                from_chat_id=message.chat.id,
                message_id=message.id,
                caption=message.caption or message.text,
                caption_entities=ents
            )
        except Exception as e: 
            print(f"Error 1: {e}")

    # 2-KANAL HANDLERI
    @app.on_message(filters.chat(S2))
    async def handler_2(client, message):
        footer = "\n\n[ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ 👈](https://t.me/eltuzar_uz_bot)"
        new_caption = (message.caption or message.text or "") + footer
        try:
            await client.copy_message(
                chat_id=T2,
                from_chat_id=message.chat.id,
                message_id=message.id,
                caption=new_caption
            )
        except Exception as e: 
            print(f"Error 2: {e}")

    await app.start()
    print("🚀 Bot 1 va 2-kanal uchun to'liq ishga tushdi!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot())
