from telegram.ext import ApplicationBuilder, CommandHandler
from db import init_db
import commands

init_db()

BOT_TOKEN = "8207945725:AAG2YW2ezeb3rSru21db8Z88Z1kPRJtQCMI"
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", commands.start))
app.add_handler(CommandHandler("post", commands.post))
app.add_handler(CommandHandler("feed", commands.feed))
app.add_handler(CommandHandler("like", commands.like))

print("Bot läuft...")
app.run_polling()

