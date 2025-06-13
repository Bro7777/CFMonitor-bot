# 🚀 CFMonitor

**CFMonitor** is a powerful and minimalistic Discord bot that monitors [Codeforces](https://codeforces.com) activity — contests, submissions, and user statistics — in real-time.

> Built for Codeforces enthusiasts who want live updates, clean stats, and seamless integration into their Discord servers.

---

## 🔧 Features

- 🕒 Live contest monitoring  
- 📊 User rating & performance tracking  
- 🧠 Personalized problem suggestions  
- 🔐 Secure Codeforces account pairing  
- 🧵 Clean slash command interface

---

## Commands

| Command            | Description                                                                                          |
| ------------------ | ---------------------------------------------------------------------------------------------------- |
| `/pair`            | 🔐 Securely link your Codeforces handle to your Discord account using a safe verification process.   |
| `/contests`        | 🗓️ View upcoming Codeforces contests with direct links to their pages.                              |
| `/stats`           | 📊 Check any user's Codeforces profile stats instantly from Discord.                                 |
| `/suggest_problem` | 🧠 Get personalized problem recommendations with optional filters (difficulty, tags, unsolved only). |
| `/user_list`       | 🏆 View a leaderboard of all paired users in the server, sorted by rating.                           |

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/Bro7777/cfmonitor.git
cd cfmonitor
```

### 2. Create .env file
```bash
DISCORD_TOKEN=your_discord_bot_token
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the bot
```bash
python main.py
```

---
## 📁 Project Structure
```bash
cfmonitor/
├── commands.py               # All commands
├── config.py              
├── database.py               # Database functions
├── functions.py              # Helper functions
├── main.py                   # Bot entry point
├── .env                      # Secrets (not tracked)
└── requirements.txt
```

---

## .env Example
```ini
DISCORD_TOKEN=your_discord_token
```

---

## 👨‍💻Developer

Developed by **@Bro7777**  
Feel free to contribute or suggest improvements!

