import os
import logging
import random
import string
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
WALLET_ADDRESS = 1

# Global state for trading status
trading_active = False

def generate_random_string(length=10):
    """Generate random letters only string"""
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def create_reply_keyboard():
    """Create the custom keyboard with 5 buttons"""
    keyboard = [
        [KeyboardButton("Deposit")],
        [KeyboardButton("Trade")],
        [KeyboardButton("Start/Stop Trading")],
        [KeyboardButton("Withdraw")],
        [KeyboardButton("Check Status")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with custom keyboard"""
    welcome_text = (
        "🤖 *Demo Trading Bot*\n\n"
        "Welcome! This is a DEMONSTRATION bot only.\n"
        "No real trading or transactions will occur.\n\n"
        "Available buttons:\n"
        "• Deposit - Get demo deposit address\n"
        "• Trade - Execute demo trade\n"
        "• Start/Stop Trading - Toggle trading state\n"
        "• Withdraw - Simulate profit withdrawal\n"
        "• Check Status - View current status\n\n"
        "⚠️ *This is for demonstration purposes only!*"
    )
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=create_reply_keyboard()
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses"""
    global trading_active
    text = update.message.text
    
    if text == "Deposit":
        random_address = generate_random_string(15)
        response = f"💎 *Deposit ETH here:*\n\n`{random_address}`\n\n⚠️ *Note:* This is a demo address. No real deposits accepted."
        
    elif text == "Trade":
        response = "🚀 *Trade Executed!*\n\nHurry! I am entering the ETH market now to make profit for you!\n\n📊 *Demo Trade Details:*\n• Market: ETH/USD\n• Direction: Long\n• Demo Amount: 1 ETH"
        
    elif text == "Start/Stop Trading":
        # Toggle trading state
        trading_active = not trading_active
        status = "✅ STARTED" if trading_active else "⏸️ STOPPED"
        response = f"🔄 *Trading Status Updated*\n\nTrading is now: *{status}*\n\n"
        if trading_active:
            response += "Demo bot is now actively monitoring the market.\n(No real trades will be executed)"
        else:
            response += "Demo bot has been paused.\nClick again to restart."
            
    elif text == "Withdraw":
        response = "💸 *Withdraw Profits*\n\nPlease enter your ETH wallet address:"
        # Set state to wait for wallet address
        context.user_data['awaiting_address'] = True
        return WALLET_ADDRESS
        
    elif text == "Check Status":
        status = "🟢 ACTIVE" if trading_active else "🔴 INACTIVE"
        response = f"📊 *Bot Status*\n\n• Trading: {status}\n• Mode: DEMONSTRATION ONLY\n• Last Action: Ready\n\nNo real funds are involved."
    
    else:
        response = "Please use one of the buttons below 👇"
    
    await update.message.reply_text(
        response,
        parse_mode='Markdown',
        reply_markup=create_reply_keyboard()
    )

async def handle_wallet_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle wallet address input for withdrawal"""
    wallet_address = update.message.text
    
    # Simple validation (demo purposes)
    if wallet_address.strip():
        # Generate a fake transaction ID
        fake_tx_id = generate_random_string(20)
        
        response = (
            "🎉 *Withdrawal Successful!*\n\n"
            f"Congratulations! 10 ETH profit is coming your way.\n\n"
            f"📬 *To Address:* {wallet_address[:15]}...\n"
            f"💰 *Amount:* 10 ETH (Demo)\n"
            f"📄 *Transaction ID:* {fake_tx_id}\n"
            f"⏱️ *Estimated Arrival:* Instant (Demo)\n\n"
            f"⚠️ *Remember:* This is a demonstration.\n"
            f"No real ETH has been transferred."
        )
        
        # Reset the state
        context.user_data['awaiting_address'] = False
        
        await update.message.reply_text(
            response,
            parse_mode='Markdown',
            reply_markup=create_reply_keyboard()
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "Please enter a valid wallet address:",
            reply_markup=create_reply_keyboard()
        )
        return WALLET_ADDRESS

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the conversation"""
    context.user_data['awaiting_address'] = False
    await update.message.reply_text(
        "Withdrawal cancelled.",
        reply_markup=create_reply_keyboard()
    )
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message"""
    help_text = (
        "🤖 *Demo Trading Bot Help*\n\n"
        "This bot demonstrates trading bot functionality.\n\n"
        "📋 *Buttons:*\n"
        "• Deposit: Get demo deposit address\n"
        "• Trade: Execute demo trade\n"
        "• Start/Stop: Toggle trading state\n"
        "• Withdraw: Simulate profit withdrawal\n"
        "• Check Status: View current status\n\n"
        "⚠️ *Important:*\n"
        "This is for DEMONSTRATION only!\n"
        "No real trading occurs.\n"
        "No real funds are involved."
    )
    
    await update.message.reply_text(
        help_text,
        parse_mode='Markdown',
        reply_markup=create_reply_keyboard()
    )

def main():
    """Start the bot."""
    # Get token from environment variable
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    
    # Create the Application
    application = Application.builder().token(TOKEN).build()
    
    # Create conversation handler for withdrawal flow
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^Withdraw$'), handle_buttons)],
        states={
            WALLET_ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet_address)
            ]
        },
        fallbacks=[
            CommandHandler('cancel', cancel),
            MessageHandler(filters.Regex('^Cancel$'), cancel)
        ]
    )
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(conv_handler)
    
    # Handle button presses (except Withdraw which is handled by conv_handler)
    application.add_handler(MessageHandler(
        filters.Regex('^(Deposit|Trade|Start/Stop Trading|Check Status)$'), 
        handle_buttons
    ))
    
    # Handle any other text (show keyboard)
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        lambda update, context: update.message.reply_text(
            "Please use one of the buttons below 👇",
            reply_markup=create_reply_keyboard()
        )
    ))
    
    # Start the Bot
    PORT = int(os.environ.get('PORT', 8443))
    
    if os.getenv('RENDER'):
        # Running on Render - use webhook
        webhook_url = f"https://{os.getenv('RENDER_SERVICE_NAME')}.onrender.com/{TOKEN}"
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            webhook_url=webhook_url,
            secret_token='RENDER_DEPLOYMENT'
        )
    else:
        # Running locally - use polling
        print("Bot is running in polling mode...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
