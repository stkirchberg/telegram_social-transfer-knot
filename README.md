# Social Transfer Knot (STK) – Telegram Bot

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://telegram.org/)

**Social Transfer Knot (STK)** is a decentralized mini-social network built entirely on Telegram. Users can post messages, broadcast them automatically to all other users, and manage their personal nickname — all without storing messages on Telegram servers.

---

## ✨ Features

- Users can **set their own nickname** (unique, case-insensitive).  
- Post messages via `/post <text>` and have them **automatically broadcast** to all registered users.  
- Messages display the sender’s nickname in **bold** for clarity.  
- Lightweight, decentralized, and easy to run locally.  
- SQLite database for persistent storage.  

---

## 🛠 Commands

| Command | Description |
|---------|-------------|
| `/setname <nickname>` | Set your unique nickname before posting. |
| `/post <text>` | Create a new post that will be sent to all users. |

> ⚠️ Note: The `/feed` and `/like` commands are no longer used. Posts are automatically delivered.  

---

## 🚀 Installation

1. Clone the repository:

git clone https://github.com/yourusername/social-transfer-knot.git  
cd social-transfer-knot

2. Install dependencies:

pip install python-telegram-bot

3. Initialize the database:

python db.py

4. Add your Telegram bot token to `main.py`:

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

5. Run the bot:

python main.py

---

## 💾 Database Structure

- **users** – stores Telegram ID, nickname, and timestamp.  
- **posts** – stores the user ID, post text, and timestamp.  

> SQLite database file: `social_bot.db`  

---

## 📖 Usage

1. Start the bot in Telegram with `/start`.  
2. Set a nickname using `/setname <nickname>`.  
3. Post a message using `/post <text>`.  
4. Your message is automatically broadcasted to all users.  

---

## ⚡ Notes

- Nicknames are **case-insensitive and unique**.  
- All messages are stored **locally**, not on Telegram servers.  
- Works best in small to medium communities.  

---

## 📝 License

MIT License – feel free to use, modify, and distribute.  
