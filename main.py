import os
import asyncio
import yt_dlp
from pyrogram import Client, filters

# --- CONFIGURATION ---
API_ID = 39120212
API_HASH = "891859ea1a8523a0653b0344198f23fc"
BOT_TOKEN = "8600054781:AAHlBkWQLf8RS5TMoSx5qG2KcAjhQGIqgnU"

app = Client("shehan_yt_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- DOWNLOADER FUNCTION ---
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'max_filesize': 500 * 1024 * 1024, # 500MB දක්වා අඩු කරමු safe වෙන්න
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# --- BOT COMMANDS ---
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(
        f"👋 ආයුබෝවන් {message.from_user.first_name}!\n\n"
        "🚀 **Shehan Youtube Video Downloader** දැන් සක්‍රීයයි.\n"
        "මට YouTube Link එකක් එවන්න."
    )

@app.on_message(filters.text & filters.private)
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
                caption=f"✅ **Downloaded successfully!**\n👨‍💻 Bot by Shehan Hansaka",
                supports_hosting=True
            )
            
            if os.path.exists(file_path):
                os.remove(file_path)
            await status_msg.delete()

        except Exception as e:
            await status_msg.edit(f"❌ වැරදීමක් සිදුවුණා: {str(e)}")
    else:
        # ලින්ක් එකක් නෙමෙයි නම් නිකන් ඉන්නවා (නැත්නම් හැම මැසේජ් එකටම රිප්ලයි කරයි)
        pass

print("Shehan's Bot is starting...")
app.run()
