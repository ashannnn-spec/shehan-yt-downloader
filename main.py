import os
import asyncio
import yt_dlp
from pyrogram import Client, filters

# --- CONFIGURATION ---
API_ID = 39120212
API_HASH = "891859ea1a8523a0653b0344198f23fc"
BOT_TOKEN = "8600054781:AAHlBkWQLf8RS5TMoSx5qG2KcAjhQGIqgnU"

app = Client("shehan_yt_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def download_social_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'max_filesize': 50 * 1024 * 1024,
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(f"👋 හලෝ {message.from_user.first_name}!\n\nTikTok හෝ FB ලින්ක් එකක් එවන්න.")

@app.on_message(filters.text & filters.private)
async def handle_download(client, message):
    url = message.text
    if any(site in url for site in ["tiktok.com", "facebook.com", "instagram.com", "fb.watch"]):
        status_msg = await message.reply_text("⏳ පොඩ්ඩක් ඉන්න...")
        try:
            if not os.path.exists("downloads"): os.makedirs("downloads")
            loop = asyncio.get_event_loop()
            file_path = await loop.run_in_executor(None, download_social_video, url)
            
            await status_msg.edit("📤 Upload වෙමින් පවතී...")
            
            # මෙතන මම අර ප්‍රශ්නය එන සේරම අයින් කළා. දැන් වැරදෙන්න විදිහක් නැහැ.
            await message.reply_video(video=file_path, caption="✅ Done by Shehan Hansaka")
            
            if os.path.exists(file_path): os.remove(file_path)
            await status_msg.delete()
        except Exception as e:
            await status_msg.edit(f"❌ වැරදීමක්: {str(e)[:100]}")

if __name__ == "__main__":
    app.run()
