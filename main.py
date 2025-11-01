import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


conn = sqlite3.connect('social_bot.db')
c = conn.cursor()


c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE,
    nickname TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS likes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    post_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(post_id) REFERENCES posts(id)
)
''')
conn.commit()



def get_or_create_user(telegram_id, nickname=None):
    c.execute("SELECT id FROM users WHERE telegram_id=?", (telegram_id,))
    user = c.fetchone()
    if user:
        return user[0]
    c.execute("INSERT INTO users (telegram_id, nickname) VALUES (?, ?)", (telegram_id, nickname))
    conn.commit()
    return c.lastrowid



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    nickname = update.effective_user.username or f"user{telegram_id}"
    get_or_create_user(telegram_id, nickname)
    await update.message.reply_text(f"Willkommen {nickname}! Nutze /post, um etwas zu posten.")

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = get_or_create_user(update.effective_user.id, update.effective_user.username)
    text = ' '.join(context.args)
    if not text:
        await update.message.reply_text("Bitte gib einen Text an: /post Dein Text hier")
        return
    c.execute("INSERT INTO posts (user_id, text) VALUES (?, ?)", (user_id, text))
    conn.commit()
    await update.message.reply_text("Beitrag gespeichert!")

async def feed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    c.execute('''
        SELECT posts.id, users.nickname, posts.text
        FROM posts
        JOIN users ON posts.user_id = users.id
        ORDER BY posts.created_at DESC
        LIMIT 5
    ''')
    posts = c.fetchall()
    if not posts:
        await update.message.reply_text("Keine Beiträge vorhanden.")
        return
    msg = "\n\n".join([f"{pid}. {nick}: {text}" for pid, nick, text in posts])
    await update.message.reply_text(msg)

async def like(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Bitte gib die Post-ID an: /like 1")
        return
    try:
        post_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Ungültige Post-ID.")
        return
    user_id = get_or_create_user(update.effective_user.id, update.effective_user.username)
    c.execute("INSERT INTO likes (user_id, post_id) VALUES (?, ?)", (user_id, post_id))
    conn.commit()
    await update.message.reply_text(f"Du hast Beitrag {post_id} geliked!")



app = ApplicationBuilder().token("8207945725:AAG2YW2ezeb3rSru21db8Z88Z1kPRJtQCMI").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("post", post))
app.add_handler(CommandHandler("feed", feed))
app.add_handler(CommandHandler("like", like))

print("Bot läuft...")
app.run_polling()
