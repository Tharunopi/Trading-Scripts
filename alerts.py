from telethon import TelegramClient, events
import asyncio
from twilio.rest import Client

API_ID = '28579025'
API_HASH = '8c7e58b5119f224020e994770fe43127'
PHONE_NUMBER = '+919360496526'
TARGET_GROUP = 'binance_announcements'
acc_ssid = "ACf867ac43d3e65c2a2bea6b23725fb323"
auth_token = "2d5e8aa4e52727e35921068c6516b226"
twilio_number = "+12243872051"
my_number = "+919360496526"

client = Client(acc_ssid, auth_token)

class TelegramAlert:

    def __init__(self, api_id, api_hash, phone_number):
        self.client = TelegramClient(phone_number, api_id, api_hash)

    async def start(self):
        await self.client.start()
        # print("Client Created")

        @self.client.on(events.NewMessage(chats=TARGET_GROUP))
        async def message_handler(event):
            await self.process_message(event.message)

    async def process_message(self, message):
        try:
            sender = await message.get_sender()
            sender_name = sender.first_name if sender else "Unknown" 
            
            # print(f"New message from {sender_name}: {message.text}")
            
            if message.text:
                if "Add" in message.text or "List" in message.text:
                    alert = "Alert! Binance launches new trading pair"
                    # print(alert)
                    messages = client.messages.create(
                        from_=twilio_number,
                        body=alert,
                        to=my_number
                    )
                    # print(messages.sid)
        except Exception as e:
            print(f"Error processing message: {e}")

    async def run(self):
        await self.start()
        await self.client.run_until_disconnected()

async def main():
    processor = TelegramAlert(API_ID, API_HASH, PHONE_NUMBER)
    await processor.run()

await main()