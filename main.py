import asyncio
import logging
from config import Config
from pyrogram import Client, idle
from typing import Union, Optional, AsyncGenerator
from logging.handlers import RotatingFileHandler
from plugins.regix import restart_forwards

# --- LOGGING SETUP CONFIGURATION ---
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        RotatingFileHandler("bot_engine.log", maxBytes=10485760, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AI-Forwarder")

# --- AI ADVANCED CUSTOM START BANNER ---
AI_BANNER = """
====================================================================
      🧬 ULTRA FAST AI-BASED FORWARD ENGINE ACTIVATED 🧬
====================================================================
           __  __ _____ _____ _____   ____   ____ _______ 
     /\   |  \/  |_   _/ ____|  __ \ / __ \ / __ \__   __|
    /  \  | \  / | | || |    | |__) | |  | | |  | | | |   
   / /\ \ | |\/| | | || |    |  _  /| |  | | |  | | | |   
  / ____ \| |  | |_| || |____| | \ \| |__| | |__| | | |   
 /_/    \_\_|  |_|_____\_____|_|  \_\\\____/ \____/  |_|   
                                                          
 >> System Status: OPTIMIZED & MULTI-THREADED
 >> Core Architecture: Asynchronous Event-Driven IO
====================================================================
"""

if __name__ == "__main__":
    print(AI_BANNER)
    logger.info("🤖 Initializing AI Neural Network Engine...")

    # Client object initialization with high-performance parameters
    AI_Bot = Client(
        "AI-Forward-Bot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=60,  # Lower threshold for faster rate-limit recovery
        plugins=dict(root="plugins"),
        workers=100          # Multi-threading capability for hyper-fast handling
    )  

    # Super-charged message iterator engine (0ms delay bulk message generator)
    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Hyper-Fast Streamlined Message Fetcher Engine."""
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            
            # Non-blocking chunk fetching architecture
            messages = await self.get_messages(chat_id, list(range(current, current + new_diff + 1)))
            for message in messages:
                yield message
                current += 1
               
    async def main():
        logger.info("🚀 Syncing Core Systems with Telegram Servers...")
        await AI_Bot.start()
        
        bot_info = await AI_Bot.get_me()
        logger.info(f"✨ AI Engine Identity Authenticated: @{bot_info.username}")
        
        # Recovering unfinished tasks from database
        logger.info("🔄 Scanning Database & Recovering Pending Tasks...")
        await restart_forwards(AI_Bot)
        
        logger.info("⚡ CORE SYSTEM ONLINE: Forwarding engine running at maximum performance! ⚡")
        await idle()

    # Executing the system loop
    asyncio.get_event_loop().run_until_complete(main())
