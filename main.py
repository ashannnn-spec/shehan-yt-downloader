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
def download_social_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'max_filesize': 50 * 1024 * 1024, # TikTok වලට 50MB ඇති
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# --- BOT COMMANDS ---
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(
        f"👋 හලෝ {message.from_user.first_name}!\n\n"
        "🚀 **Shehan Social Media Downloader** සක්‍රීයයි.\n"
        "මට TikTok, FB හෝ Instagram ලින්ක් එකක් එවන්න."
    )

@app.on_message(filters.text & filters.private)
async def handle_download(client, message):
    url = message.text
    
    # TikTok, Facebook, Instagram ලින්ක් එකක්දැයි බලමු
    if any(site in url for site in ["tiktok.com", "facebook.com", "instagram.com", "fb.watch"]):
        status_msg = await message.reply_text("⏳ වීඩියෝව බාගත කරමින් පවතී...")
        
        try:
            if not os.path.exists("downloads"):
                os.makedirs("downloads")

            loop = asyncio.get_event_loop()
            file_path = await loop.run_in_executor(None, download_social_video, url)

            await status_msg.edit("📤 ටෙලිග්‍රෑම් වෙත පටවමින් පවතී...")
            
            await message.reply_video(
                video=file_path,
                caption=f"✅ **සාර්ථකව බාගත කළා!**\n👨‍💻 Bot by Shehan Hansaka",
                supports_hosting=True
            )
            
            if os.path.exists(file_path):
                os.remove(file_path)
            await status_msg.delete()

        except Exception as e:
            await status_msg.edit(f"❌ වැරදීමක් සිදුවුණා: {str(e)[:100]}")
    else:
        # YouTube එව්වොත් පණිවිඩයක් දෙමු
        if "youtube.com" in url or "youtu.be" in url:
            await message.reply_text("⚠️ කණගාටුයි, දැනට YouTube බාගත කළ නොහැක. TikTok/FB ලින්ක් එකක් එවන්න.")
        else:
            await message.reply_text("⚠️ කරුණාකර නිවැරදි වීඩියෝ ලින්ක් එකක් එවන්න.")

if __name__ == "__main__":
    print("Social Downloader is starting...")
    app.run()
