from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from helper.database import db
import asyncio
import datetime

# ... (existing code)

# Add this new handler for broadcasting
@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(bot: Client, message: Message):
    await bot.send_message(Config.LOG_CHANNEL, f"{message.from_user.mention} is starting a broadcast...")
    all_users = await db.get_all_users()
    broadcast_msg = message.reply_to_message
    status_message = await message.reply("Broadcast started...")
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = await db.total_users_count()

    for user in all_users:
        result = await send_message(user['_id'], broadcast_msg)
        if result == "success":
            success += 1
        else:
            failed += 1

        done += 1
        if not done % 20:
            await status_message.edit(
                f"Broadcast in progress:\n\n"
                f"Total Users: {total_users}\n"
                f"Completed: {done}/{total_users}\n"
                f"Success: {success}\n"
                f"Failed: {failed}"
            )

    
    await status_message.edit(
        f"Broadcast completed:\n\n"
        f"Completed in: {completed_in}\n\n"
        f"Total Users: {total_users}\n"
        f"Completed: {done}/{total_users}\n"
        f"Success: {success}\n"
        f"Failed: {failed}"
    )

async def send_message(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return "success"
    except Exception as e:
        print(f"Error sending message to {user_id}: {str(e)}")
        return "error"
