#!/usr/bin/env python3
"""
Example usage of the trading bot as a module
This demonstrates how to use the bot programmatically
"""
from config import config
from binance_client import BinanceClient
from order_service import OrderService
from models import OrderRequest, OrderSide, OrderType
from logger import setup_logger
from exceptions import TradingBotException

logger = setup_logger(__name__)


def example_market_buy():
    """Example: Place a market buy order"""
    print("\n" + "=" * 60)
    print("Example 1: Market Buy Order")
    print("=" * 60)
    
    try:
        # Initialize client and service
        client = BinanceClient(config.API_KEY, config.API_SECRET)
        service = OrderService(client)
        
        # Create order request
        order = OrderRequest(
            symbol="BTCUSDT",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=0.001
        )
        
        # Place order
        response = service.place_order(order)
        
        print(f"✓ Order placed successfully!")
        print(f"Order ID: {response.order_id}")
        print(f"Status: {response.status}")
        print(f"Executed: {response.executed_qty} @ {response.avg_price}")
        
    except TradingBotException as e:
        print(f"✗ Error: {e}")


def example_limit_sell():
    """Example: Place a limit sell order"""
    print("\n" + "=" * 60)
    print("Example 2: Limit Sell Order")
    print("=" * 60)
    
    try:
        # Initialize client and service
        client = BinanceClient(config.API_KEY, config.API_SECRET)
        service = OrderService(client)
        
        # Create order request
        order = OrderRequest(
            symbol="ETHUSDT",
            side=OrderSide.SELL,
            order_type=OrderType.LIMIT,
            quantity=0.01,
            price=3500.00
        )
        
        # Place order
        response = service.place_order(order)
        
        print(f"✓ Order placed successfully!")
        print(f"Order ID: {response.order_id}")
        print(f"Status: {response.status}")
        print(f"Limit Price: {response.price}")
        
    except TradingBotException as e:
        print(f"✗ Error: {e}")


def example_check_balance():
    """Example: Check account balance"""
    print("\n" + "=" * 60)
    print("Example 3: Check Account Balance")
    print("=" * 60)
    
    try:
        client = BinanceClient(config.API_KEY, config.API_SECRET)
        service = OrderService(client)
        
        account_info = service.get_account_balance()
        
        print("Account Assets:")
        for asset in account_info.get("assets", []):
            balance = float(asset.get("walletBalance", 0))
            if balance > 0:
                print(f"  {asset['asset']}: {asset['walletBalance']} "
                      f"(Available: {asset['availableBalance']})")
        
    except TradingBotException as e:
        print(f"✗ Error: {e}")


def example_check_positions():
    """Example: Check open positions"""
    print("\n" + "=" * 60)
    print("Example 4: Check Open Positions")
    print("=" * 60)
    
    try:
        client = BinanceClient(config.API_KEY, config.API_SECRET)
        service = OrderService(client)
        
        positions = service.get_positions()
        
        has_positions = False
        for pos in positions:
            amount = float(pos.get("positionAmt", 0))
            if amount != 0:
                has_positions = True
                print(f"  {pos['symbol']}: {pos['positionAmt']} @ {pos['entryPrice']} "
                      f"(PnL: {pos['unRealizedProfit']})")
        
        if not has_positions:
            print("  No open positions")
        
    except TradingBotException as e:
        print(f"✗ Error: {e}")


def example_error_handling():
    """Example: Demonstrate error handling"""
    print("\n" + "=" * 60)
    print("Example 5: Error Handling")
    print("=" * 60)
    
    try:
        # This will fail - price required for LIMIT order
        order = OrderRequest(
            symbol="BTCUSDT",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=0.001
            # Missing price!
        )
        
    except Exception as e:
        print(f"✓ Validation error caught: {e}")


def main():
    """Run all examples"""
    print("\n╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "Trading Bot - Programmatic Usage Examples" + " " * 7 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Check configuration
    if not config.validate():
        print("\n✗ Configuration error: API credentials not set")
        print("Please configure your .env file first")
        return
    
    # Run examples
    example_error_handling()  # Start with error handling demo
    
    # Uncomment these to run actual API calls:
    # example_check_balance()
    # example_check_positions()
    # example_market_buy()
    # example_limit_sell()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60 + "\n")
    
    print("Note: Some examples are commented out to prevent accidental orders.")
    print("Uncomment them in the script to test actual API calls.")


if __name__ == "__main__":
    main()
