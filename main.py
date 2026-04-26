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
        'max_filesize': 500 * 1024 * 1024, # 500MB Limit
        # YouTube Block මඟහරවා ගැනීමට අවශ්‍ය සෙටින්ග්ස්
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
        'add_header': [
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language: en-us,en;q=0.5',
            'Sec-Fetch-Mode: navigate',
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# --- BOT COMMANDS ---
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(
        f"👋 ආයුබෝවන් {message.from_user.first_name}!\n\n"
        "🚀 **Shehan Youtube Downloader** දැන් සක්‍රීයයි.\n"
        "මට YouTube Link එකක් එවන්න, මම එය බාගත කර දෙන්නම්."
    )

@app.on_message(filters.text & filters.private)
async def handle_download(client, message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        status_msg = await message.reply_text("⏳ වීඩියෝව පරීක්ෂා කරමින් පවතී...")
        
        try:
            # Download folder එකක් නැත්නම් හදනවා
            if not os.path.exists("downloads"):
                os.makedirs("downloads")

            await status_msg.edit("📥 බාගත වෙමින් පවතී (Downloading)...")
            
            # Async විදිහට download එක run කරනවා
            loop = asyncio.get_event_loop()
            file_path = await loop.run_in_executor(None, download_video, url)

            await status_msg.edit("📤 Telegram වෙත පටවමින් පවතී (Uploading)...")
            
            # වීඩියෝව යැවීම
            await message.reply_video(
                video=file_path,
                caption=f"✅ **සාර්ථකව බාගත කළා!**\n\n👨‍💻 Bot by Shehan Hansaka",
                supports_hosting=True
            )
            
            # ඉඩ ඉතිරි කර ගැනීමට සර්වර් එකේ තියෙන file එක මකා දැමීම
            if os.path.exists(file_path):
                os.remove(file_path)
            await status_msg.delete()

        except Exception as e:
            # වැරැද්දක් වුණොත් ඒක පෙන්වනවා
            error_text = str(e)
            if "Sign in to confirm you’re not a bot" in error_text:
                await status_msg.edit("❌ YouTube එකෙන් සර්වර් එක බ්ලොක් කරලා. පසුව උත්සාහ කරන්න හෝ වෙනත් ලින්ක් එකක් දෙන්න.")
            else:
                await status_msg.edit(f"❌ වැරදීමක් සිදුවුණා: {error_text[:100]}")
    else:
        # YouTube ලින්ක් එකක් නෙමෙයි නම්
        await message.reply_text("⚠️ කරුණාකර නිවැරදි YouTube ලින්ක් එකක් එවන්න.")

# බොට් ක්‍රියාත්මක කිරීම
if __name__ == "__main__":
    print("Shehan's Bot is Starting...")
    app.run()
