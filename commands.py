import secrets
from telegram import Update
from telegram.ext import ContextTypes
from db import c, conn, get_or_create_user, has_nickname, set_nickname, is_authenticated


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "👋 Welcome!\n\n"
        "Before you can use this bot, you need to log in with a one-time token:\n"
        "/login <token>\n\n"
        "After that, set your nickname:\n"
        "/setname <nickname>\n\n"
        "Available commands:\n"
        "/login <token> – Access with a one-time password\n"
        "/setname <nickname> – Choose your nickname\n"
        "/post <text> – Create a new post\n"
    )
    await update.message.reply_text(welcome_message)


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("Usage: /login <token>")
        return

    token = context.args[0].strip()

    c.execute("SELECT id, used FROM tokens WHERE token=?", (token,))
    token_row = c.fetchone()

    if not token_row:
        await update.message.reply_text("❌ Invalid token.")
        return
    if token_row[1]:
        await update.message.reply_text("❌ This token has already been used.")
        return

    get_or_create_user(telegram_id)
    c.execute("UPDATE tokens SET used=1 WHERE id=?", (token_row[0],))
    conn.commit()

    await update.message.reply_text("✅ Access granted. You are now logged in!")


async def generate_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ADMIN_ID = 123456789  # YOUR TELEGRAM ID FOR ADMIN RIGHTS
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not allowed to generate tokens.")
        return

    amount = int(context.args[0]) if context.args else 1
    new_tokens = []

    for _ in range(amount):
        token = secrets.token_hex(4)
        c.execute("INSERT INTO tokens (token) VALUES (?)", (token,))
        new_tokens.append(token)

    conn.commit()
    await update.message.reply_text("✅ Generated tokens:\n" + "\n".join(new_tokens))



async def setname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    if not is_authenticated(telegram_id):
        await update.message.reply_text("❌ You must log in first using /login <token>.")
        return

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
        await update.message.reply_text("❌ This nickname is already taken. Please choose another one.")


async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    if not is_authenticated(telegram_id):
        await update.message.reply_text("❌ You must log in first using /login <token>.")
        return

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
        f"<b>{nickname}</b> (ID {post_id}, {created_at}):\n"
        f"{text}"
    )

    c.execute("SELECT telegram_id FROM users")
    recipients = c.fetchall()

    for (recipient_id,) in recipients:
        try:
            await context.bot.send_message(
                chat_id=recipient_id,
                text=broadcast_text,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Could not send to {recipient_id}: {e}")
