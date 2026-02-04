"""
Custom exceptions for the trading bot
"""


class TradingBotException(Exception):
    """Base exception for trading bot errors"""
    pass


class ConfigurationError(TradingBotException):
    """Raised when configuration is invalid or missing"""
    pass


class BinanceAPIError(TradingBotException):
    """Raised when Binance API returns an error"""
    
    def __init__(self, message: str, code: int = None, response: dict = None):
        self.code = code
        self.response = response
        super().__init__(message)


class NetworkError(TradingBotException):
    """Raised when network request fails"""
    pass


class ValidationError(TradingBotException):
    """Raised when input validation fails"""
    pass
