import os
import asyncio
import yt_dlp
from pyrogram import Client, filters

# --- CONFIGURATION ---
API_ID = 39120212
API_HASH = "891859ea1a8523a0653b0344198f23fc"
BOT_TOKEN = "8600054781:AAHlBkWQLf8RS5TMoSx5qG2KcAjhQGIqgnU"

# මෙතන සරලව app එක හදමු
app = Client("shehan_yt_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'max_filesize': 500 * 1024 * 1024,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(f"👋 ආයුබෝවන් {message.from_user.first_name}!\n\n🚀 Shehan Downloader සූදානම්. Link එක එවන්න.")

@app.on_message(filters.text & filters.private)
async def handle_download(client, message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        status_msg = await message.reply_text("⏳ පොඩ්ඩක් ඉන්න...")
        try:
            if not os.path.exists("downloads"):
                os.makedirs("downloads")
            
            loop = asyncio.get_event_loop()
            file_path = await loop.run_in_executor(None, download_video, url)

            await status_msg.edit("📤 Upload වෙමින් පවතී...")
            await message.reply_video(video=file_path, caption="✅ Done by Shehan Hansaka")
            
            if os.path.exists(file_path):
                os.remove(file_path)
            await status_msg.delete()
        except Exception as e:
            await status_msg.edit(f"❌ Error: {str(e)}")

# Python 3.14 වල RuntimeError එක නොවෙන්න මේ විදිහට run කරමු
if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
