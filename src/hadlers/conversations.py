"""
Handle natural language conversations
"""
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from openai import OpenAI

from src.core.config import Config
from src.character.fenrir import get_system_prompt
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Initialize OpenAI client
openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)

# Store conversations per user (in-memory for now)
conversations = {}


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    user_message = update.message.text
    
    logger.info(f"Message from {user_name} ({user_id}): {user_message[:50]}...")
    
    # Show typing indicator
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )
    
    try:
        # Initialize conversation for new user
        if user_id not in conversations:
            conversations[user_id] = [
                {"role": "system", "content": get_system_prompt()}
            ]
        
        # Add user message
        conversations[user_id].append({
            "role": "user",
            "content": user_message
        })
        
        # Get AI response
        response = openai_client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=conversations[user_id],
            max_tokens=Config.MAX_TOKENS,
            temperature=Config.TEMPERATURE
        )
        
        ai_message = response.choices[0].message.content
        
        # Add AI response to conversation
        conversations[user_id].append({
            "role": "assistant",
            "content": ai_message
        })
        
        # Keep conversation history manageable (last 20 messages + system)
        if len(conversations[user_id]) > 21:
            conversations[user_id] = [conversations[user_id][0]] + conversations[user_id][-20:]
        
        # Send response
        await update.message.reply_text(ai_message)
        
        logger.info(f"Responded to {user_name}")
        
    except Exception as e:
        logger.error(f"Error handling message: {e}", exc_info=True)
        await update.message.reply_text(
            "⚡ By Thor's hammer! An error occurred. Try again, warrior!"
        )