"""
Main bot class - orchestrates all components
"""
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import BotCommand
import logging

from src.core.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class FenrirBot:
    """Fenrir Viking Bot main class"""
    
    def __init__(self):
        """Initialize the bot"""
        logger.info("🐺 Initializing Fenrir Bot...")
        
        self.config = Config
        self.application = None
        
        # Display configuration
        self.config.display()
    
    def setup_handlers(self):
        """Register all command and message handlers"""
        logger.info("⚙️  Setting up handlers...")
        
        app = self.application
        
        # Import handlers here to avoid circular imports
        from src.handlers import commands, conversations
        
        # Command handlers
        app.add_handler(CommandHandler("start", commands.start))
        app.add_handler(CommandHandler("help", commands.help_command))
        
        # Message handler (for conversations)
        app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                conversations.handle_message
            )
        )
        
        logger.info("✅ Handlers registered")
    
    async def post_init(self, application: Application):
        """Post-initialization setup"""
        logger.info("🔧 Running post-initialization...")
        
        # Set bot commands menu
        commands = [
            BotCommand("start", "Begin your journey"),
            BotCommand("help", "Get help and guidance"),
        ]
        await application.bot.set_my_commands(commands)
        
        logger.info("✅ Bot commands menu set")
    
    def run(self):
        """Start the bot"""
        logger.info("🚀 Starting Fenrir Bot...")
        
        # Build application
        self.application = (
            Application.builder()
            .token(self.config.TELEGRAM_TOKEN)
            .post_init(self.post_init)
            .build()
        )
        
        # Setup handlers
        self.setup_handlers()
        
        # Start bot
        print("✅ Fenrir is ready!")
        print("📱 Open Telegram and talk to your bot")
        print("⌨️  Press Ctrl+C to stop\n")
        
        logger.info("🎯 Bot is now running...")
        
        self.application.run_polling(drop_pending_updates=True)