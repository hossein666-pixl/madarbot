import logging
import openai
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# 🔑 جایگزین کن با اطلاعات خودت:
TELEGRAM_BOT_TOKEN = "7913959222:AAGwUKUHi04pak3lbNlHASEWuRh3qng3hYk"
OPENAI_API_KEY = "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"

# فعال‌سازی لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

openai.api_key = OPENAI_API_KEY

# ✅ فرمان /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من ربات مادر هوشمند هستم.\nچه رباتی می‌خوای برات بسازم؟")

# 🧠 پاسخ به پیام‌های فارسی برای ساخت ربات
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("⌛ در حال ساخت ربات مورد نظر...")

    prompt = f"""به عنوان برنامه‌نویس تلگرام، یک کد کامل پایتون برای رباتی بنویس که ویژگی زیر را داشته باشد:\n{user_text}\nاز کتابخانه python-telegram-bot استفاده کن. کد کامل باشد."""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )

        code = response.choices[0].message["content"]
        await update.message.reply_text("✅ ربات ساخته شد!\n👇 اینم کد:")
        await update.message.reply_text(code[:4000])  # محدودیت پیام

    except Exception as e:
        await update.message.reply_text(f"❌ خطا در تولید کد: {e}")

# 🚀 اجرای ربات
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
