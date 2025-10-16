#!/usr/bin/env python3
"""
Fenrir Viking Bot - Main Entry Point
"""
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.bot import FenrirBot
from src.utils.logger import setup_logging


def main():
    """Start the Fenrir bot"""
    # Setup logging
    setup_logging()
    
    print("\n⚔️  FENRIR THE VIKING MENTOR ⚔️")
    print("🐺 Initializing...\n")
    
    try:
        bot = FenrirBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n⚔️ Fenrir returns to Valhalla...")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        raise


if __name__ == '__main__':
    main()