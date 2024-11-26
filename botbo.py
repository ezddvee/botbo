import discord
from discord.ext import commands
from PIL import Image
import pytesseract
import io
import os
from dotenv import load_dotenv
from openai import OpenAI

# Nạp các biến môi trường
load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

# Khởi tạo OpenAI client
client = OpenAI(api_key=os.getenv('API_KEY'))

# Tạo bot với command prefix là "!"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def get_gpt_response(text):
    """
    Gửi câu hỏi tới GPT-3.5-turbo và nhận đáp án
    """
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Chỉ đưa đáp án, khỏi giải thích: {text}",
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Lỗi khi gọi API OpenAI: {e}")
        return "Không thể lấy đáp án"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    # Kiểm tra nếu tin nhắn có file đính kèm
    if message.attachments:
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
                # Tải ảnh về từ tin nhắn
                image_bytes = await attachment.read()
                image = Image.open(io.BytesIO(image_bytes))
                
                # OCR để nhận diện chữ trong ảnh bằng tiếng Việt
                text = pytesseract.image_to_string(image, lang='vie')
                
                # Kiểm tra nếu có nội dung
                if text.strip():
                    # Gửi câu hỏi tới GPT và nhận đáp án
                    gpt_response = get_gpt_response(text)
                    
                    # Gửi phản hồi với @everyone
                    await message.channel.send(f'@everyone {gpt_response}')

# Chạy bot
bot.run(bot_token)