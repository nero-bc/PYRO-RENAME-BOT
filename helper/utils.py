import math
import time
from datetime import datetime
from pytz import timezone
from config import Config, Txt
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Initialize your Pyrogram Client
app = Client("my_account")

async def progress_for_pyrogram(current, total, ud_type, message, start, additional_info, another_detail, file_name, date):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "⬢" * math.floor(percentage / 5) + "⬡" * (20 - math.floor(percentage / 5))
        tmp = PROGRESS_BAR.format(
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != '' else "0 s",
            additional_info,
            another_detail,
            file_name,
            date
        )
        try:
            await message.edit(
                text=f"{ud_type}\n\n{tmp}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="close")
                ]])
            )
        except:
            pass

def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {Dic_powerN[n]}ʙ"

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{days}ᴅ, ") if days else ""
    ) + (
        (f"{hours}ʜ, ") if hours else ""
    ) + (
        (f"{minutes}ᴍ, ") if minutes else ""
    ) + (
        (f"{seconds}ꜱ, ") if seconds else ""
    ) + (
        (f"{milliseconds}ᴍꜱ, ") if milliseconds else ""
    )
    return tmp[:-2]

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)

async def send_log(b, u):
    if Config.LOG_CHANNEL is not None:
        curr = datetime.now(timezone("Asia/Kolkata"))
        date = curr.strftime('%d %B, %Y')
        time = curr.strftime('%I:%M:%S %p')
        await b.send_message(
            Config.LOG_CHANNEL,
            f"**--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\nUꜱᴇʀ: {u.mention}\nIᴅ: `{u.id}`\nUɴ: @{u.username}\n\nDᴀᴛᴇ: {date}\nTɪᴍᴇ: {time}\n\nBy: {b.mention}"
        )

# Start your Pyrogram Client
app.run()
