import logging
import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# ======================
# Flask server (مهم لـ Render)
# ======================
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is running ✅"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

# ======================
# إعداد اللوج
# ======================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ======================
# قاعدة البيانات
# ======================
QA_DB = {
    "السلام عليكم": "وعليكم السلام ورحمة الله.",
    "اهلا": "أهلاً بك! 👋",
    "مرحبا": "مرحباً بيك ❤️",
    "ازيك": "الحمد لله بخير، إنت عامل إيه؟",
    "عامل ايه": "تمام الحمد لله 😊",
    "اخبارك": "كل شيء تمام 👍",
    "صباح الخير": "صباح النور ☀️",
    "مساء الخير": "مساء الورد 🌹",
    "من انت": "أنا بوت دردشة ذكي 🤖",
    "اسمك ايه": "اسمي المساعد الرقمي",
    "ضحكني": "مرة واحد نام بدري… صحى لقى نفسه في المستقبل 😂",
    "نكتة": "ليه الكمبيوتر بردان؟ لأنه فاتح الويندوز 😂",
    "شكرا": "العفو يا بطل ❤️",
    "باي": "مع السلامة 👋"
}

# ======================
# تنظيف النص
# ======================
def clean_text(text: str):
    text = text.lower()
    text = text.replace('أ','ا').replace('إ','ا').replace('آ','ا')
    text = text.replace('ة','ه').replace('ى','ي')
    
    return ''.join(char for char in text if char.isalnum() or char.isspace()).strip()

# ======================
# الرد
# ======================
def get_response(msg: str):
    msg = clean_text(msg)

    if msg in QA_DB:
        return QA_DB[msg]

    for q, a in QA_DB.items():
        if clean_text(q) in msg or msg in clean_text(q):
            return a

    return "مش فاهمك كويس 🤔"

# ======================
# أوامر البوت
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً 👋 البوت شغال 24 ساعة 🤖")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(get_response(update.message.text))

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Error: {context.error}")

# ======================
# تشغيل
# ======================
def main():
    TOKEN = os.getenv("BOT_TOKEN")

    if not TOKEN:"8608803954:AAEN8UN3TpJRuYCbGyHWVXL4AgfZSpGQaWw" 
        print("❌ مفيش توكن!")
        return

    # تشغيل السيرفر في Thread
    threading.Thread(target=run_web).start()

    bot = Application.builder().token(TOKEN).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    bot.add_error_handler(error_handler)

    print("✅ البوت شغال...")
    bot.run_polling()

if __name__ == "__main__":
    main()