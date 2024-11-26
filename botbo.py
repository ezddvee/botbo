import discord
from discord.ext import commands
from PIL import Image
import pytesseract
import io
import os

from dotenv import load_dotenv
load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

# Nếu bạn cần chỉ định đường dẫn tới tesseract (trong trường hợp tesseract không nằm trong PATH)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Tạo bot với command prefix là "!"
intents = discord.Intents.default()
intents.message_content = True  # Cần bật intent này để nhận tin nhắn chứa nội dung
bot = commands.Bot(command_prefix="!", intents=intents)

# Sự kiện khi bot sẵn sàng hoạt động
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Sự kiện khi nhận được một tin nhắn
@bot.event
async def on_message(message):
    # Nếu người gửi là bot thì bỏ qua
    #if message.author.bot:
    #    return

    # Kiểm tra nếu tin nhắn có file đính kèm
    if message.attachments:
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
                # Tải ảnh về từ tin nhắn
                image_bytes = await attachment.read()
                image = Image.open(io.BytesIO(image_bytes))

                # OCR để nhận diện chữ trong ảnh bằng tiếng Việt
                text = pytesseract.image_to_string(image, lang='vie')
                
                # Trả lời trong kênh với nội dung OCR
                if text.strip():  # Kiểm tra nếu có nội dung
                    await message.channel.send(f'@everyone {text}')
                #else:
                #    await message.channel.send('Không tìm thấy văn bản nào trong ảnh.')

# Đặt token bot của bạn ở đây
bot.run(bot_token)
