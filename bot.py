import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

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
# الرد الذكي
# ======================
def get_response(msg: str):
    msg = clean_text(msg)

    # تطابق مباشر
    if msg in QA_DB:
        return QA_DB[msg]

    # بحث جزئي
    for q, a in QA_DB.items():
        q_clean = clean_text(q)
        if q_clean in msg or msg in q_clean:
            return a

    return "مش فاهمك كويس 🤔 جرّب تكتب بطريقة أبسط."

# ======================
# /start
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بيك 👋\nأنا بوت دردشة شغال 24 ساعة 🤖\nجرب اكتب: ازيك"
    )

# ======================
# الرسائل
# ======================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        response = get_response(update.message.text)
        await update.message.reply_text(response)

# ======================
# أخطاء
# ======================
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("حدث خطأ: %s", context.error)

# ======================
# تشغيل البوت
# ======================
def main():
    TOKEN ="8608803954:AAEN8UN3TpJRuYCbGyHWVXL4AgfZSpGQaWw"

    if not TOKEN:
        print("❌ لم يتم العثور على التوكن!")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    print("✅ البوت شغال الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()