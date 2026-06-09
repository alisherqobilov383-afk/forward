import os
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread

# Render'dan o'zgaruvchilarni qabul qilish
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
SESSION_STRING = os.environ.get('SESSION_STRING')

# Kanallar
SOURCE_CHANNEL = 'tuztuzttt'
TARGET_CHANNEL = 'eltuzar_livee'

# Flask (Uptime ushlab turish uchun)
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot 24/7 ishlamoqda!"

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Client
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

def modify_entities(entities):
    if not entities:
        return None
    
    for entity in entities:
        if hasattr(entity, 'url') and entity.url:
            url = entity.url.upper()
            if any(x in url for x in ["ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ", "ЮБОРМОҚЧИ", "УШБУ"]):
                entity.url = "https://t.me/eltuzar_uz_bot"
            elif "LIVE" in url:
                entity.url = "https://t.me/eltuzar_livee"
            elif "MEDIA" in url:
                entity.url = "https://t.me/eltuzar_mediaa"
            elif "X.COM" in url:
                entity.url = "https://x.com/eltuzar_uz"
            elif "INSTAGRAM" in url:
                entity.url = "https://www.instagram.com/eltuzaar_uz"
            elif "FACEBOOK" in url:
                entity.url = "https://www.facebook.com/profile.php?id=61585818251235"
    return entities

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    try:
        # Xabarni nusxalash va havolalarni o'zgartirish
        new_entities = modify_entities(event.message.entities)
        
        await client.send_message(
            TARGET_CHANNEL,
            message=event.message.text,
            file=event.message.media,
            formatting_entities=new_entities
        )
        logging.info("Xabar muvaffaqiyatli ko'chirildi.")
    except Exception as e:
        logging.error(f"Xabar uzatishda xatolik: {e}")

# Ishga tushirish
if __name__ == '__main__':
    # Flask serverini fon rejimida ishga tushirish
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    
    # Userbotni ishga tushirish
    client.start()
    logging.info("Userbot ishga tushdi...")
    client.run_until_disconnected()
