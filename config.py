"""
Configuration module for Binance Futures Trading Bot
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""
    
    # Binance Futures Testnet
    TESTNET_BASE_URL = "https://testnet.binancefuture.com"
    
    # API Credentials
    API_KEY: Optional[str] = os.getenv("BINANCE_API_KEY")
    API_SECRET: Optional[str] = os.getenv("BINANCE_API_SECRET")
    
    # Logging
    LOG_FILE = "trading_bot.log"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_LEVEL = "INFO"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present"""
        if not cls.API_KEY or not cls.API_SECRET:
            return False
        if cls.API_KEY == "your_api_key_here":
            return False
        return True
    
    @classmethod
    def get_missing_config(cls) -> list[str]:
        """Return list of missing configuration items"""
        missing = []
        if not cls.API_KEY or cls.API_KEY == "your_api_key_here":
            missing.append("BINANCE_API_KEY")
        if not cls.API_SECRET or cls.API_SECRET == "your_api_secret_here":
            missing.append("BINANCE_API_SECRET")
        return missing


# Singleton instance
config = Config()
