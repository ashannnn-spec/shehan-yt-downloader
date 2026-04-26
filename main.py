import os
import asyncio
import yt_dlp
from pyrogram import Client, filters
from flask import Flask
import threading

# Render එකේ බොට්ව Live තියාගන්න Flask app එක
app = Flask('')

@app.route('/')
def home():
    return "Shehan's Bot is Running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# --- CONFIGURATION ---
API_ID = 39120212
API_HASH = "891859ea1a8523a0653b0344198f23fc"
BOT_TOKEN = "8600054781:AAHlBkWQLf8RS5TMoSx5qG2KcAjhQGIqgnU"

bot = Client("shehan_yt_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- DOWNLOADER FUNCTION ---
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'max_filesize': 1024 * 1024 * 1024, # 1GB Limit
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# --- BOT COMMANDS ---
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(
        f"👋 ආයුබෝවන් {message.from_user.first_name}!\n\n"
        "🚀 **Shehan Youtube Video Downloader** වෙත සාදරයෙන් පිළිගනිමු.\n"
        "මට ඕනෑම YouTube Link එකක් එවන්න, මම එය 1GB දක්වා download කර දෙන්නම්.\n\n"
        "👨‍💻 Created by: Shehan Hansaka"
    )

@bot.on_message(filters.text & filters.private)
async def handle_download(client, message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        status_msg = await message.reply_text("⏳ වීඩියෝ එක පරීක්ෂා කරමින් පවතී...")
        
        try:
            if not os.path.exists("downloads"):
                os.makedirs("downloads")

            await status_msg.edit("📥 බාගත වෙමින් පවතී (Downloading)...")
            loop = asyncio.get_event_loop()
            file_path = await loop.run_in_executor(None, download_video, url)

            await status_msg.edit("📤 Telegram වෙත පටවමින් පවතී (Uploading)...")
            await message.reply_video(
                video=file_path,
                caption=f"✅ **Downloaded successfully!**\n\n🎬 Title: `{os.path.basename(file_path)}` \n👨‍💻 Bot by Shehan Hansaka",
                supports_hosting=True
            )
            
            if os.path.exists(file_path):
                os.remove(file_path)
            await status_msg.delete()

        except Exception as e:
            await status_msg.edit(f"❌ වැරදීමක් සිදුවුණා: {str(e)}")
    else:
        await message.reply_text("⚠️ කරුණාකර නිවැරදි YouTube ලින්ක් එකක් එවන්න.")

# Flask සර්වර් එක background එකේ run කිරීම
threading.Thread(target=run_flask).start()

print("Bot is starting...")
bot.run()
