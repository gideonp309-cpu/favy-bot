# Telegram Demo Trading Bot

A demonstration trading bot with 5 interactive buttons, deployed on Render.com.

## Features

### 5 Interactive Buttons:
1. **Deposit** - Generates random string for demo deposit address
2. **Trade** - Shows demo trade execution message
3. **Start/Stop Trading** - Toggles trading state (active/inactive)
4. **Withdraw** - Asks for ETH address and shows success message
5. **Check Status** - Shows current bot status

## Setup Instructions

### 1. Create a Telegram Bot
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow instructions
3. Get your bot token (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Local Development
```bash
# Clone and setup
git clone <your-repo>
cd telegram-demo-bot

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your bot token

# Run locally
python bot.py
