import sqlite3

conn = sqlite3.connect('social_bot.db', check_same_thread=False)
c = conn.cursor()


def init_db():
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        nickname TEXT COLLATE NOCASE,
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
    CREATE TABLE IF NOT EXISTS tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT UNIQUE,
        used BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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


def has_nickname(telegram_id):
    c.execute("SELECT nickname FROM users WHERE telegram_id=?", (telegram_id,))
    result = c.fetchone()
    return bool(result and result[0])


def set_nickname(telegram_id, nickname):
    c.execute("SELECT id FROM users WHERE nickname = ? COLLATE NOCASE", (nickname,))
    if c.fetchone():
        return False

    get_or_create_user(telegram_id)
    c.execute("UPDATE users SET nickname=? WHERE telegram_id=?", (nickname, telegram_id))
    conn.commit()
    return True


def is_authenticated(telegram_id):
    c.execute("SELECT 1 FROM users WHERE telegram_id=?", (telegram_id,))
    return c.fetchone() is not None

