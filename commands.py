from telegram import Update
from telegram.ext import ContextTypes
from db import c, conn, get_or_create_user


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
