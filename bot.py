import subprocess, datetime, os, asyncio
from telegram import Bot
from keep_alive import keep_alive
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- SETTINGS ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # Your Telegram user ID
STREAM_URL = "https://m3umergers.xyz/artl/artl.ts?id=a02p"
# ----------------

bot = Bot(token=BOT_TOKEN)
scheduler = AsyncIOScheduler()

async def record_and_send():
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"pogo_{now}.mp4"
    print(f"🎬 Recording started at {now}...")

    command = [
        "ffmpeg",
        "-i", STREAM_URL,
        "-map", "0:v:0",
        "-map", "0:a:2",   # Track 2 = Tamil
        "-t", "01:00:00",  # Record for 1 hour
        "-c", "copy",
        filename
    ]
    subprocess.run(command)

    print("✅ Recording finished, sending to Telegram...")
    with open(filename, "rb") as video:
        await bot.send_video(chat_id=CHAT_ID, video=video, caption=f"POGO Tamil - {now}")

    os.remove(filename)
    print("🗑️ Sent and deleted local file ✅")

async def main():
    keep_alive()
    scheduler.add_job(record_and_send, "cron", hour=6, minute=0, timezone="Asia/Kolkata")    # Morning 6 AM
    scheduler.add_job(record_and_send, "cron", hour=22, minute=55, timezone="Asia/Kolkata")  # Night 10:55 PM
    scheduler.start()
    print("🕓 Scheduler started successfully ✅")
    await asyncio.Event().wait()  # Keep running

if __name__ == "__main__":
    asyncio.run(main())
