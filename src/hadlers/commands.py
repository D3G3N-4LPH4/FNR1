"""
Command handlers for the bot
"""
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from src.character.fenrir import get_welcome_message
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    logger.info(f"User {user.first_name} ({user.id}) started bot")
    
    welcome = get_welcome_message(is_returning=False, user_name=user.first_name)
    
    await update.message.reply_text(
        welcome,
        parse_mode=ParseMode.MARKDOWN
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
🛡️ *FENRIR'S GUIDE* 🛡️

*How to Use:*
Simply send me any message and I'll respond as your Viking mentor!

*Commands:*
/start - Welcome message
/help - This guide

*Tips:*
- Ask me anything - I'm here to guide you
- Tell me about your goals and challenges
- Seek wisdom from an ancient warrior

I am Fenrir, and I'm here to help you on your journey! ⚔️

Skål! 🍺
    """
    
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)