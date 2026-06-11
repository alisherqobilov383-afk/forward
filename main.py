import os
import asyncio

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import MessageEntityTextUrl

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

SOURCE_CHANNEL = os.environ.get(
"SOURCE_CHANNEL",
"@tuztuzttt"
)

TARGET_CHANNEL = os.environ.get(
"TARGET_CHANNEL",
"@eltuzar_livee"
)

client = TelegramClient(
StringSession(SESSION_STRING),
API_ID,
API_HASH
)

def replace_links(text, entities):
if not text:
return text, entities

```
if not entities:
    return text, entities

for entity in entities:

    if not isinstance(entity, MessageEntityTextUrl):
        continue

    word = text[
        entity.offset:
        entity.offset + entity.length
    ].upper()

    if any(
        x in word
        for x in [
            "ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ",
            "ЮБОРМОҚЧИ",
            "УШБУ",
        ]
    ):
        entity.url = "https://t.me/eltuzar_uz_bot"

    elif "LIVE" in word:
        entity.url = "https://t.me/eltuzar_livee"

    elif "MEDIA" in word:
        entity.url = "https://t.me/eltuzar_mediaa"

    elif word == "X":
        entity.url = "https://x.com/eltuzar_uz"

    elif "INSTAGRAM" in word:
        entity.url = (
            "https://www.instagram.com/eltuzaar_uz"
        )

    elif "FACEBOOK" in word:
        entity.url = (
            "https://www.facebook.com/"
            "profile.php?id=61585818251235"
        )

return text, entities
```

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
try:
message = event.message

```
    text = message.message or ""
    entities = message.entities

    text, entities = replace_links(
        text,
        entities
    )

    if message.media:

        await client.send_file(
            TARGET_CHANNEL,
            file=message.media,
            caption=text,
            formatting_entities=entities
        )

        print(
            f"Media forwarded: {message.id}"
        )

    else:

        await client.send_message(
            TARGET_CHANNEL,
            text,
            formatting_entities=entities
        )

        print(
            f"Message forwarded: {message.id}"
        )

except Exception as e:
    print(
        f"Forward error: {e}"
    )
```

async def main():
print(
f"Listening: {SOURCE_CHANNEL}"
)

```
print(
    f"Target: {TARGET_CHANNEL}"
)

await client.run_until_disconnected()
```

with client:
client.loop.run_until_complete(main())
