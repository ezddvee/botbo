import discord
from discord.ext import commands
from PIL import Image
import pytesseract
import io
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Nạp các biến môi trường
load_dotenv()
bot_token = os.getenv('DISCORD_BOT_TOKEN')
gemini_api_key = os.getenv('GOOGLE_API_KEY')

# Cấu hình Gemini API
genai.configure(api_key=gemini_api_key)

# Tạo bot với command prefix là "!"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def get_gemini_response(text):
    """
    Gửi câu hỏi tới Gemini 1.5 Flash và nhận đáp án
    """
    try:
        # Khởi tạo model Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Tạo prompt với system instruction
        full_prompt = f"Chỉ đưa đáp án, khỏi giải thích: {text}"
        
        # Gọi API
        response = model.generate_content(full_prompt, 
                                          generation_config=genai.types.GenerationConfig(
                                              max_output_tokens=100,
                                              temperature=0.7
                                          ))
        
        return response.text.strip()
    except Exception as e:
        print(f"Lỗi khi gọi Gemini API: {e}")
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
                    # Gửi câu hỏi tới Gemini và nhận đáp án
                    gemini_response = get_gemini_response(text)
                    
                    # Gửi phản hồi với @everyone
                    await message.channel.send(f'@everyone {gemini_response}')

# Chạy bot
bot.run(bot_token)