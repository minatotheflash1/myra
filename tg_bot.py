import os
import psycopg2
import random
import string
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Railway te Variables theke auto load hobe
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
DB_URL = os.getenv("DATABASE_URL")

def setup_key_db():
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS valid_keys (
                        key VARCHAR(255) PRIMARY KEY,
                        days INTEGER,
                        is_used BOOLEAN DEFAULT FALSE
                    )''')
    conn.commit()
    cursor.close()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Boss! Send /genkey <days> to generate a Myra access key.\nExample: /genkey 30")

async def genkey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to generate keys!")
        return
        
    try:
        days = int(context.args[0])
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        key = f"MYRA-{random_str}"
        
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO valid_keys (key, days) VALUES (%s, %s)", (key, days))
        conn.commit()
        cursor.close()
        conn.close()
        
        response = (
            f"✅ *New Access Key Generated!*\n\n"
            f"🔑 *Key:* `{key}`\n"
            f"⏳ *Validity:* {days} Days\n\n"
            f"Give this key to your user."
        )
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except IndexError:
        await update.message.reply_text("⚠️ Please provide the number of days. Example: `/genkey 30`", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"❌ Error saving key: {e}")

if __name__ == "__main__":
    if not BOT_TOKEN or not DB_URL:
        print("Error: Missing Environment Variables!")
    else:
        setup_key_db()
        app = Application.builder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("genkey", genkey))
        
        print("🤖 Telegram Key Generator Bot is running on Railway...")
        app.run_polling()