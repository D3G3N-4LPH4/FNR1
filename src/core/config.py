"""
Configuration management for Fenrir bot
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Bot configuration"""
    
    # Project paths
    BASE_DIR = Path(__file__).parent.parent.parent
    SRC_DIR = BASE_DIR / "src"
    DATA_DIR = BASE_DIR / "data"
    
    # API Keys (from environment variables)
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # OpenAI Settings
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1500"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Bot Settings
    MAX_CONVERSATION_LENGTH = 20
    MESSAGE_COOLDOWN = 2  # seconds between messages
    
    # File paths
    MEMORY_FILE = DATA_DIR / "fenrir_memories.json"
    SHARED_FILE = DATA_DIR / "fenrir_shared.json"
    
    @classmethod
    def validate(cls):
        """Validate that all required settings are present"""
        errors = []
        
        if not cls.TELEGRAM_TOKEN:
            errors.append("TELEGRAM_TOKEN not found in .env file")
        
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY not found in .env file")
        
        if errors:
            error_msg = "Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors)
            raise ValueError(error_msg)
        
        # Create data directory if it doesn't exist
        cls.DATA_DIR.mkdir(exist_ok=True)
        
        print("✅ Configuration validated")
    
    @classmethod
    def display(cls):
        """Display current configuration (safely)"""
        print("\n📋 Configuration:")
        print(f"  Model: {cls.OPENAI_MODEL}")
        print(f"  Max Tokens: {cls.MAX_TOKENS}")
        print(f"  Temperature: {cls.TEMPERATURE}")
        print(f"  Data Directory: {cls.DATA_DIR}")
        print()


# Validate configuration when module is imported
Config.validate()