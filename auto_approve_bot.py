import os
import asyncio
from telethon import TelegramClient, events

# =========================
# ENV VARIABLES (RAILWAY)
# =========================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP = os.getenv("GROUP")  # @groupusername or group ID
DELAY = float(os.getenv("DELAY", "0.1"))

# =========================
# CLIENT
# =========================
client = TelegramClient("auto_approve_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)


# =========================
# AUTO APPROVE NEW REQUESTS
# =========================
@client.on(events.ChatAction)
async def handler(event):

    if not event.join_request:
        return

    user = await event.get_user()

    try:
        await client.approve_chat_join_request(event.chat_id, user.id)
        print(f"Approved new user: {user.id}")
    except Exception as e:
        print(f"Error approving user {user.id}: {e}")


# =========================
# CLEAR OLD REQUESTS ON START
# =========================
async def clear_old_requests():
    print("Clearing existing join requests...")

    try:
        async for req in client.iter_chat_join_requests(GROUP):
            try:
                await client.approve_chat_join_request(GROUP, req.user_id)
                print(f"Approved old request: {req.user_id}")
                await asyncio.sleep(DELAY)
            except Exception as e:
                print(f"Failed {req.user_id}: {e}")

    except Exception as e:
        print(f"Could not load join requests: {e}")


# =========================
# MAIN START
# =========================
async def main():
    print("Bot is running...")
    await clear_old_requests()
    await client.run_until_disconnected()


client.loop.run_until_complete(main())
