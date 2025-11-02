from telegram.ext import ApplicationBuilder, CommandHandler
from db import init_db
import commands

init_db()

BOT_TOKEN = "12345678:aaaBBBcccDDDeeeFFF"
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", commands.start))
app.add_handler(CommandHandler("post", commands.post))
app.add_handler(CommandHandler("setname", commands.setname))


print("Bot läuft...")
app.run_polling()

