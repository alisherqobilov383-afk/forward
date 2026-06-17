import os
import asyncio
from flask import Flask
from threading import Thread
from telethon import TelegramClient, events
from telethon.sessions import StringSession

app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))), daemon=True).start()

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session = os.environ["SESSION_STRING"]

source = os.environ["SOURCE_CHANNEL"]
target = os.environ["TARGET_CHANNEL"]

client = TelegramClient(StringSession(session), api_id, api_hash)

LINK_MAP = {
    "https://t.me/eltuzportali_bot": "https://t.me/eltuzga_murojaat_bot",
    "https://t.me/eltuzar_live": "https://t.me/eltuzportaluz"
}

def replace_links(text):
    if not text:
        return text
    for a, b in LINK_MAP.items():
        text = text.replace(a, b)
    return text

# ================= ALBUM =================
@client.on(events.Album(chats=source))
async def album(event):
    try:
        media = []
        caption = ""

        for msg in event.messages:
            if not caption:
                caption = replace_links(msg.text or msg.message or "")

            # 🔥 MUHIM: HAR QANDAY FILE
            if msg.media:
                media.append(msg.media)

        await client.send_file(target, media, caption=caption)

        print("ALBUM OK")

    except Exception as e:
        print("ALBUM ERROR:", e)

# ================= SINGLE =================
@client.on(events.NewMessage(chats=source))
async def handler(event):
    try:
        msg = event.message
        text = replace_links(msg.text or msg.message or "")

        # 🔥 ENG MUHIM FIX
        if msg.media:
            await client.send_file(target, msg.media, caption=text)

        else:
            await client.send_message(target, text)

        print("OK:", msg.id)

    except Exception as e:
        print("ERROR:", e)

async def main():
    await client.start()
    print("BOT STARTED")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
