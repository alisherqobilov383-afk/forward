import os
import asyncio
from telethon import TelegramClient, errors
from telethon.tl.types import MessageEntityType

class TelegramForwarder:
    def __init__(self, api_id, api_hash, session_string=None):
        self.api_id = api_id
        self.api_hash = api_hash
        # Session string or session file
        self.client = TelegramClient(session_string if session_string else 'anon', api_id, api_hash)

    def process_entities(self, text, entities):
        if not entities:
            return text, entities
        
        for entity in entities:
            if isinstance(entity, MessageEntityType.TextLink):
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
        return text, entities

    async def forward_messages(self, source_chat_id, destination_channel_id):
        await self.client.start()
        
        # Oxirgi xabarni olish
        last_message = await self.client.get_messages(source_chat_id, limit=1)
        last_message_id = last_message[0].id if last_message else 0

        print(f"Monitoring boshlandi: {source_chat_id} -> {destination_channel_id}")

        while True:
            messages = await self.client.get_messages(source_chat_id, min_id=last_message_id, limit=None)
            
            for message in reversed(messages):
                text = message.text
                entities = message.entities
                
                # Havolalarni yangilash
                new_text, new_entities = self.process_entities(text, entities)
                
                # Xabarni yuborish (Copy)
                await self.client.send_message(
                    destination_channel_id, 
                    message=new_text, 
                    formatting_entities=new_entities,
                    file=message.media # Agar rasm/video bo'lsa
                )
                
                last_message_id = max(last_message_id, message.id)
                print(f"Xabar yuborildi: {message.id}")

            await asyncio.sleep(5)

async def main():
    # Environment variable'lardan o'qish
    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_HASH")
    session_string = os.environ.get("SESSION_STRING")
    source_channel = os.environ.get("SOURCE_CHANNEL", "@tuztuzttt")
    target_channel = os.environ.get("TARGET_CHANNEL", "@eltuzar_livee")

    if not api_id or not api_hash:
        print("Error: API_ID va API_HASH o'rnatilmagan!")
        return

    forwarder = TelegramForwarder(api_id, api_hash, session_string)
    await forwarder.forward_messages(source_channel, target_channel)

if __name__ == "__main__":
    asyncio.run(main())
