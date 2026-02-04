"""
Order service - Business logic layer for order management
"""
from typing import Optional
from binance_client import BinanceClient
from models import OrderRequest, OrderResponse
from logger import setup_logger
from exceptions import ValidationError

logger = setup_logger(__name__)


class OrderService:
    """
    Service layer for managing orders
    Handles validation and interacts with Binance client
    """
    
    def __init__(self, client: BinanceClient):
        """
        Initialize order service
        
        Args:
            client: Configured BinanceClient instance
        """
        self.client = client
        logger.info("Order service initialized")
    
    def validate_symbol(self, symbol: str) -> bool:
        """
        Validate that the symbol exists on the exchange
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            True if symbol is valid
            
        Raises:
            ValidationError: If symbol is invalid
        """
        try:
            info = self.client.get_exchange_info(symbol=symbol)
            if "symbols" in info and len(info["symbols"]) > 0:
                logger.info(f"Symbol {symbol} validated successfully")
                return True
            else:
                raise ValidationError(f"Symbol {symbol} not found on exchange")
        except Exception as e:
            logger.error(f"Symbol validation failed: {e}")
            raise ValidationError(f"Failed to validate symbol {symbol}: {e}")
    
    def place_order(self, order_request: OrderRequest) -> OrderResponse:
        """
        Place an order on Binance Futures
        
        Args:
            order_request: Validated order request
            
        Returns:
            Order response with execution details
            
        Raises:
            ValidationError: If validation fails
            BinanceAPIError: If API returns an error
        """
        # Validate symbol before placing order
        logger.info("Validating order request...")
        self.validate_symbol(order_request.symbol)
        
        # Log order summary
        logger.info("=" * 60)
        logger.info("ORDER REQUEST SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Symbol: {order_request.symbol}")
        logger.info(f"Side: {order_request.side}")
        logger.info(f"Type: {order_request.order_type}")
        logger.info(f"Quantity: {order_request.quantity}")
        if order_request.price:
            logger.info(f"Price: {order_request.price}")
        logger.info("=" * 60)
        
        # Place order
        try:
            response_data = self.client.place_order(
                symbol=order_request.symbol,
                side=order_request.side,
                order_type=order_request.order_type,
                quantity=order_request.quantity,
                price=order_request.price
            )
            
            # Parse response
            order_response = OrderResponse(**response_data)
            
            logger.info("=" * 60)
            logger.info("ORDER EXECUTED SUCCESSFULLY")
            logger.info("=" * 60)
            logger.info(f"\n{order_response}")
            logger.info("=" * 60)
            
            return order_response
            
        except Exception as e:
            logger.error(f"Order placement failed: {e}")
            raise
    
    def get_account_balance(self) -> dict:
        """
        Get account balance information
        
        Returns:
            Account balance data
        """
        try:
            account_info = self.client.get_account_info()
            logger.info("Retrieved account information")
            return account_info
        except Exception as e:
            logger.error(f"Failed to get account balance: {e}")
            raise
    
    def get_positions(self, symbol: Optional[str] = None) -> list:
        """
        Get current positions
        
        Args:
            symbol: Optional symbol to filter by
            
        Returns:
            List of positions
        """
        try:
            positions = self.client.get_position_info(symbol=symbol)
            logger.info(f"Retrieved position information for {symbol or 'all symbols'}")
            return positions
        except Exception as e:
            logger.error(f"Failed to get positions: {e}")
            raise
