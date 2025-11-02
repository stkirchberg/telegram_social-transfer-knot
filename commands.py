from telegram import Update
from telegram.ext import ContextTypes
from db import c, conn, get_or_create_user, has_nickname, set_nickname


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    get_or_create_user(telegram_id)

    welcome_message = (
        "👋 Welcome!\n\n"
        "Before you can post or like, please set a nickname using:\n"
        "/setname <nickname>\n\n"
        "Available commands:\n"
        "/post <text> – Create a new post\n"
        "/feed – Show the latest posts\n"
        "/like <post_id> – Like a post\n"
        "/setname <nickname> – Choose your nickname"
    )
    await update.message.reply_text(welcome_message)


async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    if not has_nickname(telegram_id):
        await update.message.reply_text("❌ You need to set a nickname first using /setname <nickname>.")
        return

    user_id = get_or_create_user(telegram_id)
    text = ' '.join(context.args)
    if not text:
        await update.message.reply_text("Please provide some text: /post Your text here")
        return

    c.execute("INSERT INTO posts (user_id, text) VALUES (?, ?)", (user_id, text))
    conn.commit()
    c.execute("SELECT id, created_at FROM posts WHERE rowid = last_insert_rowid()")
    post_id, created_at = c.fetchone()

    c.execute("SELECT nickname FROM users WHERE telegram_id=?", (telegram_id,))
    nickname = c.fetchone()[0]

    broadcast_text = (
        f"🆕 New post by {nickname} (ID {post_id}, {created_at}):\n"
        f"{text}\n\n❤️ Like with /like {post_id}"
    )


    c.execute("SELECT telegram_id FROM users WHERE telegram_id != ?", (telegram_id,))
    recipients = c.fetchall()

    for (recipient_id,) in recipients:
        try:
            await context.bot.send_message(chat_id=recipient_id, text=broadcast_text)
        except Exception as e:
            print(f"Could not send to {recipient_id}: {e}")

    await update.message.reply_text("✅ Post sent to everyone!")


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
        await update.message.reply_text("No posts available yet.")
        return

    msg = "\n\n".join([
        f"ID: {post_id} | {nick} ({created_at}):\n{text}"
        for post_id, nick, text, created_at in posts
    ])
    await update.message.reply_text(msg)


async def like(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    if not has_nickname(telegram_id):
        await update.message.reply_text("❌ You need to set a nickname first using /setname <nickname>.")
        return

    if not context.args:
        await update.message.reply_text("Please provide the post ID: /like 1")
        return

    try:
        post_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Invalid post ID.")
        return

    user_id = get_or_create_user(telegram_id)
    c.execute("INSERT INTO likes (user_id, post_id) VALUES (?, ?)", (user_id, post_id))
    conn.commit()
    await update.message.reply_text(f"You liked post {post_id} ❤️")


async def setname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("Usage: /setname <nickname>")
        return

    nickname = context.args[0].strip()

    if len(nickname) < 3 or len(nickname) > 20:
        await update.message.reply_text("Nickname must be between 3 and 20 characters.")
        return
    if not nickname.isalnum():
        await update.message.reply_text("Nickname must be alphanumeric (letters/numbers only).")
        return

    success = set_nickname(telegram_id, nickname)
    if success:
        await update.message.reply_text(f"✅ Your nickname has been set to '{nickname}'.")
    else:
        await update.message.reply_text("❌ This nickname is already taken (case-insensitive). Please choose another one.")
