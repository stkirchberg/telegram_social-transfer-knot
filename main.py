from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from db import init_db
import commands

init_db()

BOT_TOKEN = "12345678:aaaBBBcccDDDeeeFFF"
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", commands.start))
app.add_handler(CommandHandler("setname", commands.setname))
app.add_handler(CommandHandler("login", commands.login))
app.add_handler(CommandHandler("generate_token", commands.generate_token))
app.add_handler(CommandHandler("deleteuser", commands.deleteuser))
app.add_handler(CommandHandler("commands", commands.commands_list))
app.add_handler(CommandHandler("users", commands.users_list))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, commands.post_message))
app.add_handler(MessageHandler(filters.COMMAND, commands.unknown_command))

print("Bot is running...")
app.run_polling()