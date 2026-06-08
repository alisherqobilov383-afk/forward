import sys
import os
import asyncio
import logging

# Loglarni yoqish (Render loglarida xatolikni ko'rish uchun)
logging.basicConfig(level=logging.INFO)

# Pyrogram sync xatosini oldini olish
class FakeSync:
    def __getattr__(self, name): return None
sys.modules["pyrogram.sync"] = FakeSync()

from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# ================= SERVER =================
flask_app = Flask("")
@flask_app.route("/")
def home(): return "Bot 24/7!"
Thread(target=lambda: flask_app.run(host="0.0.0.0", port=8080), daemon=True).start()

# ================= MATN MANTIQI =================
def edit_caption_text(message: Message):
    text = message.caption or message.text
    if not text: return "", []

    entities = message.caption_entities or message.entities or []
    bold_entity = next((e for e in entities if e.type == MessageEntityType.BOLD and e.offset == 0), None)
    
    sarlavha = text[bold_entity.offset : bold_entity.offset + bold_entity.length] if bold_entity else text.split('\n')[0]

    footer_text = (
        "\n\n👇 Давоми\n\n"
        "ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ 👈\n\n"
        "Расмий саҳифаларимизга обуна бўлинг:\n"
        "LIVE | MEDIA | X | INSTAGRAM | FACEBOOK"
    )

    full_text = sarlavha + footer_text
    new_entities = []
    
    if bold_entity:
        new_entities.append(MessageEntityType.BOLD(offset=0, length=len(sarlavha)))
    
    def add_link(url, link_text):
        start = full_text.find(link_text)
        if start != -1:
            new_entities.append(MessageEntityType.TEXT_LINK(offset=start, length=len(link_text), url=url))

    add_link("https://t.me/eltuzar_uz_bot", "ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ 👈")
    add_link("https://t.me/eltuzaar_uz", "LIVE")
    add_link("https://t.me/eltuzaar_uz", "MEDIA")
    add_link("https://x.com/eltuzar_uz", "X")
    add_link("https://www.instagram.com/eltuzaar_uz", "INSTAGRAM")
    add_link("https://www.facebook.com/profile.php?id=61585818251235", "FACEBOOK")

    return full_text, new_entities

# ================= ASOSIY BOT =================
async def start_bot():
    app = Client("render_userbot", 
                 api_id=int(os.environ["API_ID"]), 
                 api_hash=os.environ["API_HASH"], 
                 session_string=os.environ["SESSION_STRING"])

    await app.start()
    me = await app.get_me()
    print(f"✅ Bot ishga tushdi: {me.first_name}")

    # Kanalni aniqlash
    source = os.environ.get("SOURCE_CHANNEL", "@tuztuzttt")
    target = os.environ.get("TARGET_CHANNEL", "@eltuzaar_uz")
    
    try:
        # Kanalni botga tanitish
        chat = await app.get_chat(source)
        print(f"🔍 Kanal topildi: {chat.title} (ID: {chat.id})")
    except Exception as e:
        print(f"❌ Kanalni topib bo'lmadi (Bot kanalga a'zo emasmi?): {e}")

    @app.on_message(filters.chat(source))
    async def forward_and_edit(client: Client, message: Message):
        print(f"📩 Yangi xabar olindi!")
        new_text, new_entities = edit_caption_text(message)
        
        try:
            if message.photo: await client.send_photo(target, message.photo.file_id, caption=new_text, caption_entities=new_entities)
            elif message.video: await client.send_video(target, message.video.file_id, caption=new_text, caption_entities=new_entities)
            elif message.text: await client.send_message(target, text=new_text, entities=new_entities)
        except Exception as e:
            print(f"❌ Yuborishda xatolik: {e}")

    await asyncio.Event().wait() # Botni o'chmasligini ta'minlash

if __name__ == "__main__":
    asyncio.run(start_bot())
