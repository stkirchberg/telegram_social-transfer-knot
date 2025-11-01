from telegram import Update
from telegram.ext import ContextTypes
from db import c, conn, get_or_create_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    nickname = update.effective_user.username or f"user{telegram_id}"
    get_or_create_user(telegram_id, nickname)

    welcome_message = (
        f"Welcome {nickname}!\n\n"
        "Here are the commands you can use:\n"
        "/post <text> - Create a new post\n"
        "/feed - Show the latest posts\n"
        "/like <post_id> - Like a post\n"
    )

    await update.message.reply_text(welcome_message)


async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = get_or_create_user(update.effective_user.id, update.effective_user.username)
    text = ' '.join(context.args)
    if not text:
        await update.message.reply_text("Please provide some text: /post Your text here")
        return
    c.execute("INSERT INTO posts (user_id, text) VALUES (?, ?)", (user_id, text))
    conn.commit()
    await update.message.reply_text("Post saved!")


async def feed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    c.execute('''
        SELECT posts.id, users.nickname, posts.text, posts.created_at
        FROM posts
        JOIN users ON posts.user_id = users.id
        ORDER BY posts.created_at DESC
        LIMIT 5
    ''')
    posts = c.fetchall()
    if not posts:
        await update.message.reply_text("No posts available.")
        return

    msg = "\n\n".join([
        f"{nick} ({created_at}):\n{text}"
        for _, nick, text, created_at in posts
    ])
    await update.message.reply_text(msg)


async def like(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide the post ID: /like 1")
        return
    try:
        post_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Invalid post ID.")
        return
    user_id = get_or_create_user(update.effective_user.id, update.effective_user.username)
    c.execute("INSERT INTO likes (user_id, post_id) VALUES (?, ?)", (user_id, post_id))
    conn.commit()
    await update.message.reply_text(f"You liked post {post_id}!")

