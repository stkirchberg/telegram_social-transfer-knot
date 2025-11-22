# Social Transfer Knot (STK) – Telegram Bot

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://telegram.org/)

**Social Transfer Knot (STK)** is a decentralized chat network built entirely on Telegram. Users can post messages, broadcast them automatically to all other users, and manage their personal nickname — all without storing messages on Telegram servers.

---

## ✨ Features

- Users must **log in with a one-time token** before posting.  
- Users can set a **unique, alphanumeric nickname** (3–20 characters, case-insensitive).  
- Messages posted are **automatically broadcast** to all registered users.  
- Admin commands for **token generation** and **user deletion**.  
- Persistent local storage using SQLite.

---

## 🛠 Commands

| Command | Description |
|--------|-------------|
| `/start` | Displays a welcome message and instructions for new users. |
| `/login <token>` | Log in using a one-time token. |
| `/setname <nickname>` | Set your unique nickname. |
| `/commands` | See all commands. |
| `/generate_token [amount]` | *(Admin only)* Generate one or multiple new tokens. |
| `/deleteuser <nickname or telegram_id>` | *(Admin only)* Delete a user and all their posts. |
| `/users` | *(Admin only)* A list of all users. |


> ⚠️ You must log in and set a nickname before posting.

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
2. Login with `/login <token>`
3. Set a nickname using `/setname <nickname>`.  
4. Post a message using `/post <text>`.  
5. Your message is automatically broadcasted to all users.  

---

## ⚡ Notes

- Nicknames are **case-insensitive and unique**.  
- All messages are stored **locally**, not on Telegram servers.  
- Works best in small to medium communities.  

---

## 📝 License

MIT License – feel free to use, modify, and distribute.  
