from telethon import TelegramClient, events
import asyncio

# =========================
# CONFIG (FILL THIS IN)
# =========================
api_id = 1234567
api_hash = "YOUR_API_HASH"
bot_token = "YOUR_BOT_TOKEN"

# Put your group username or ID here
GROUP = "YOUR_GROUP_USERNAME_OR_ID"

# Delay to avoid Telegram rate limits
DELAY = 0.1

# =========================
# CLIENT START
# =========================
client = TelegramClient("auto_approve_session", api_id, api_hash).start(bot_token=bot_token)


# =========================
# AUTO APPROVE NEW REQUESTS
# =========================
@client.on(events.ChatAction)
async def handler(event):

    # Ignore normal joins
    if event.user_joined or event.user_added:
        return

    # Handle join requests
    if event.join_request:
        try:
            await client.approve_chat_join_request(
                event.chat_id,
                event.user_id
            )
            print(f"Approved: {event.user_id}")
        except Exception as e:
            print(f"Error approving user {event.user_id}: {e}")


# =========================
# CLEAR EXISTING REQUESTS
# =========================
async def clear_old_requests():
    print("Checking existing join requests...")

    try:
        async for req in client.iter_chat_join_requests(GROUP):
            try:
                await client.approve_chat_join_request(GROUP, req.user_id)
                print(f"Approved existing: {req.user_id}")
                await asyncio.sleep(DELAY)
            except Exception as e:
                print(f"Failed: {req.user_id} | {e}")

    except Exception as e:
        print(f"Could not fetch join requests: {e}")


# =========================
# STARTUP
# =========================
async def main():
    print("Bot is running...")

    # Clear old pending requests once at startup
    await clear_old_requests()

    # Keep running for new requests
    await client.run_until_disconnected()


client.loop.run_until_complete(main())
