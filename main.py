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
        'cookiefile': 'cookies.txt', 
        # Format එක වෙනස් කළා - වීඩියෝ සහ ඕඩියෝ දෙකම තියෙන හොඳම තත්ත්වය තෝරනවා
        'format': 'best[ext=mp4]/best', 
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'max_filesize': 500 * 1024 * 1024,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# --- BOT COMMANDS ---
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(
        f"👋 ආයුබෝවන් {message.from_user.first_name}!\n\n"
        "🚀 **Shehan Youtube Downloader** දැන් වැඩ.\n"
        "YouTube Link එක එවන්න."
    )

@app.on_message(filters.text & filters.private)
async def handle_download(client, message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        status_msg = await message.reply_text("⏳ වීඩියෝව පරීක්ෂා කරමින් පවතී...")
        
        try:
            if not os.path.exists("downloads"):
                os.makedirs("downloads")

            await status_msg.edit("📥 බාගත වෙමින් පවතී (Downloading)...")
            
            loop = asyncio.get_event_loop()
            file_path = await loop.run_in_executor(None, download_video, url)

            await status_msg.edit("📤 Telegram වෙත පටවමින් පවතී (Uploading)...")
            
            await message.reply_video(
                video=file_path,
                caption=f"✅ **Shehan Hansaka Bot** මගින් බාගත කළා.",
                supports_hosting=True
            )
            
            if os.path.exists(file_path):
                os.remove(file_path)
            await status_msg.delete()

        except Exception as e:
            await status_msg.edit(f"❌ වැරදීමක් සිදුවුණා: {str(e)[:150]}")
    else:
        await message.reply_text("⚠️ කරුණාකර නිවැරදි YouTube ලින්ක් එකක් එවන්න.")

if __name__ == "__main__":
    print("Bot is Starting...")
    app.run()
