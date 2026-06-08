import sys
import os
import asyncio
import copy

# 1. PYROGRAM SYNC MODULINI O'CHIRAMIZ
class FakeSync:
    def __getattr__(self, name): return None
sys.modules["pyrogram.sync"] = FakeSync()

from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# ================= RENDER UPTIME SERVER =================
flask_app = Flask("")
@flask_app.route("/")
def home(): return "Bot 24/7 ishlamoqda!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

Thread(target=run_flask, daemon=True).start()

# ================= MATNNI TAHRIRLASH MANTIQI =================
def edit_caption_text(message: Message):
    text = message.caption or message.text
    if not text: return "", []

    entities = message.caption_entities or message.entities or []
    
    # Faqat boshidagi qalin (BOLD) yozuvni yoki birinchi qatorni sarlavha deb olish
    bold_entity = next((e for e in entities if e.type == MessageEntityType.BOLD and e.offset == 0), None)
    
    if bold_entity:
        sarlavha = text[bold_entity.offset : bold_entity.offset + bold_entity.length]
    else:
        sarlavha = text.split('\n')[0]

    # Footer qismi
    footer_text = (
        "\n\n👇 Давоми\n\n"
        "ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ 👈\n\n"
        "Расмий саҳифаларимизга обуна бўлинг:\n"
        "LIVE | MEDIA | X | INSTAGRAM | FACEBOOK"
    )

    full_text = sarlavha + footer_text
    
    # Entity'larni yangilash
    new_entities = []
    
    # Agar sarlavha qalin bo'lsa, uni saqlab qolamiz
    if bold_entity:
        new_entities.append(MessageEntityType.BOLD(offset=0, length=len(sarlavha)))
    
    # Havolalarni qo'shish
    def add_link(url, link_text):
        start = full_text.find(link_text)
        if start != -1:
            new_entities.append(MessageEntityType.TEXT_LINK(
                offset=start, length=len(link_text), url=url
            ))

    add_link("https://t.me/eltuzar_uz_bot", "ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ 👈")
    add_link("https://t.me/eltuzaar_uz", "LIVE")
    add_link("https://t.me/eltuzaar_uz", "MEDIA")
    add_link("https://x.com/eltuzar_uz", "X")
    add_link("https://www.instagram.com/eltuzaar_uz", "INSTAGRAM")
    add_link("https://www.facebook.com/profile.php?id=61585818251235", "FACEBOOK")

    return full_text, new_entities

# ================= ASOSIY BOT QISMI =================
async def start_bot():
    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_HASH")
    session_string = os.environ.get("SESSION_STRING")
    
    # Kanal nomlari
    source_channel = os.environ.get("SOURCE_CHANNEL", "@tuztuzttt")
    target_channel = os.environ.get("TARGET_CHANNEL", "@eltuzaar_uz")

    if not api_id or not api_hash:
        print("❌ XATOLIK: API sozlamalari topilmadi!")
        return

    app = Client("render_userbot", api_id=int(api_id), api_hash=api_hash, session_string=session_string)

    @app.on_message(filters.chat(source_channel))
    async def forward_and_edit(client: Client, message: Message):
        new_text, new_entities = edit_caption_text(message)
        try:
            if message.photo: await client.send_photo(target_channel, photo=message.photo.file_id, caption=new_text, caption_entities=new_entities)
            elif message.video: await client.send_video(target_channel, video=message.video.file_id, caption=new_text, caption_entities=new_entities)
            elif message.audio or message.voice: await client.send_audio(target_channel, audio=(message.audio or message.voice).file_id, caption=new_text, caption_entities=new_entities)
            elif message.text: await client.send_message(target_channel, text=new_text, entities=new_entities)
        except Exception as e: print(f"❌ Xatolik: {e}")

    await app.start()
    print(f"🚀 Bot ishga tushdi! Kuzatilmoqda: {source_channel}")
    
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(start_bot())
