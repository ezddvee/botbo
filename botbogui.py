import discord
from discord.ext import commands
from PIL import Image
import pytesseract
import io
import pystray
from pystray import MenuItem as item
from PIL import Image as PilImage
import threading
import os
import sys

from dotenv import load_dotenv
load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

# Khởi tạo bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Sự kiện khi bot sẵn sàng
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Xử lý tin nhắn
@bot.event
async def on_message(message):
    if message.attachments:
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
                image_bytes = await attachment.read()
                image = Image.open(io.BytesIO(image_bytes))
                text = pytesseract.image_to_string(image, lang='vie')
                if text.strip():
                    await message.channel.send(f'@everyone {text}')

# Chạy bot trong thread riêng
def run_bot():
    bot.run(bot_token)

# Hàm thoát ứng dụng
def quit_app():
    os._exit(0)

# Tạo và chạy icon trong system tray
def create_tray_icon():
    # Tạo icon mặc định nếu không có file icon
    default_icon = PilImage.new('RGB', (64, 64), color='black')
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "icon.ico")
    
    icon_image = PilImage.open(icon_path) if os.path.exists(icon_path) else default_icon
    
    # Tạo menu với chỉ một option là Quit
    tray_icon = pystray.Icon(
        "Bot Bò",
        icon_image,
        "Bot Bò",
        menu=pystray.Menu(
            item("Quit", quit_app)
        )
    )
    
    # Khởi động bot trước khi chạy system tray
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Chạy icon trong system tray
    tray_icon.run()

if __name__ == "__main__":
    # Chạy trực tiếp system tray (không hiện GUI)
    create_tray_icon()