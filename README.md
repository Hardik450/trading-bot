# Binance Futures Trading Bot

A professional Python trading bot for placing orders on Binance Futures Testnet (USDT-M). Features a clean architecture with proper logging, error handling, and type safety.

## Features

✅ **Order Types**: Market and Limit orders  
✅ **Order Sides**: Buy and Sell  
✅ **Clean Architecture**: Separated client, service, and CLI layers  
✅ **Comprehensive Logging**: All operations logged to file  
✅ **Error Handling**: Network errors, API errors, validation errors  
✅ **Type Safety**: Pydantic models with validation  
✅ **Rich CLI**: Beautiful terminal interface with tables and colors  
✅ **Account Management**: Check balance and positions  

## Architecture

```
├── main.py              # CLI application (entry point)
├── config.py            # Configuration management
├── logger.py            # Logging setup
├── models.py            # Data models (Pydantic)
├── exceptions.py        # Custom exceptions
├── binance_client.py    # Binance API client
├── order_service.py     # Business logic layer
└── requirements.txt     # Python dependencies
```

## Setup

### 1. Get Binance Futures Testnet Credentials

1. Visit [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Register/login with GitHub or Google
3. Generate API credentials
4. Save your API Key and API Secret

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install requests==2.31.0 python-binance==1.0.19 typer==0.12.3 python-dotenv==1.0.0 pydantic==2.5.0 rich
```

### 3. Configure API Credentials

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
BINANCE_API_KEY=your_actual_api_key_here
BINANCE_API_SECRET=your_actual_api_secret_here
```

### 4. Test Connection

```bash
python main.py test
```

## Usage

### Place Orders

#### Market Order (Buy)
```bash
python main.py order BTCUSDT BUY MARKET 0.001
```

#### Market Order (Sell)
```bash
python main.py order ETHUSDT SELL MARKET 0.01
```

#### Limit Order (Buy)
```bash
python main.py order BTCUSDT BUY LIMIT 0.001 --price 45000
```

#### Limit Order (Sell)
```bash
python main.py order ETHUSDT SELL LIMIT 0.01 --price 3500
```

### Check Account Balance
```bash
python main.py balance
```

### View Open Positions
```bash
# All positions
python main.py positions

# Specific symbol
python main.py positions BTCUSDT
```

### Test Connection
```bash
python main.py test
```

### Get Help
```bash
python main.py --help
python main.py order --help
```

## Order Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `symbol` | Yes | Trading pair symbol | BTCUSDT, ETHUSDT |
| `side` | Yes | Order side | BUY, SELL |
| `order_type` | Yes | Order type | MARKET, LIMIT |
| `quantity` | Yes | Order quantity | 0.001, 0.01 |
| `--price` / `-p` | For LIMIT only | Limit price | 45000, 3500 |

## Logging

All operations are logged to `trading_bot.log` with detailed information:
- API requests and responses
- Order executions
- Errors and exceptions
- Timestamps for all events

Example log entries:
```
2026-02-04 10:30:45 - binance_client - INFO - Initialized Binance client with base URL: https://testnet.binancefuture.com
2026-02-04 10:30:46 - order_service - INFO - Symbol BTCUSDT validated successfully
2026-02-04 10:30:47 - order_service - INFO - Placing MARKET BUY order for 0.001 BTCUSDT
2026-02-04 10:30:48 - order_service - INFO - ORDER EXECUTED SUCCESSFULLY
```

## Error Handling

The bot handles various error scenarios:

### Configuration Errors
- Missing API credentials
- Invalid credentials
- Clear error messages with setup instructions

### Validation Errors
- Invalid symbol names
- Invalid order sides (must be BUY/SELL)
- Invalid order types (must be MARKET/LIMIT)
- Missing price for LIMIT orders
- Negative quantities or prices

### Network Errors
- Connection timeouts
- Connection failures
- DNS resolution errors

### API Errors
- Invalid API keys
- Insufficient balance
- Invalid order parameters
- Rate limiting
- Market/symbol not found

## Example Output

### Successful Market Order
```
╭──────────────────────────────────────╮
│ Binance Futures Trading Bot         │
│ Testnet Environment                  │
╰──────────────────────────────────────╯

         Order Request          
┌───────────────┬────────────────┐
│ Symbol        │ BTCUSDT        │
│ Side          │ BUY            │
│ Type          │ MARKET         │
│ Quantity      │ 0.001          │
└───────────────┴────────────────┘

✓ Order placed successfully!

         Order Response          
┌─────────────────────┬────────────────┐
│ Order ID            │ 12345678       │
│ Symbol              │ BTCUSDT        │
│ Status              │ FILLED         │
│ Side                │ BUY            │
│ Type                │ MARKET         │
│ Quantity            │ 0.001          │
│ Executed Quantity   │ 0.001          │
│ Average Price       │ 48500.50       │
│ Total Value         │ 48.50          │
└─────────────────────┴────────────────┘
```

### Successful Limit Order
```
         Order Request          
┌───────────────┬────────────────┐
│ Symbol        │ ETHUSDT        │
│ Side          │ SELL           │
│ Type          │ LIMIT          │
│ Quantity      │ 0.01           │
│ Price         │ 3500           │
└───────────────┴────────────────┘

✓ Order placed successfully!

         Order Response          
┌─────────────────────┬────────────────┐
│ Order ID            │ 87654321       │
│ Symbol              │ ETHUSDT        │
│ Status              │ NEW            │
│ Side                │ SELL           │
│ Type                │ LIMIT          │
│ Quantity            │ 0.01           │
│ Executed Quantity   │ 0.00           │
│ Price               │ 3500.00        │
└─────────────────────┴────────────────┘
```

## Code Quality Features

- **Type Hints**: Full type annotations throughout the codebase
- **Pydantic Models**: Data validation and serialization
- **Enum Types**: Type-safe enums for sides and order types
- **Separation of Concerns**: Clear separation between API, business logic, and CLI
- **DRY Principle**: Reusable components and utilities
- **Error Propagation**: Proper exception hierarchy
- **Logging Strategy**: Structured logging with appropriate levels
- **Configuration Management**: Environment-based configuration

## Testing Tips

On Binance Futures Testnet:
1. You get test USDT automatically
2. Orders execute against test markets
3. No real money is involved
4. Perfect for testing and development

Common test scenarios:
```bash
# Test with small quantities first
python main.py order BTCUSDT BUY MARKET 0.001

# Check your balance
python main.py balance

# View positions
python main.py positions

# Test limit orders
python main.py order BTCUSDT BUY LIMIT 0.001 --price 40000
```

## Troubleshooting

### "Configuration Error: Missing API credentials"
- Make sure `.env` file exists in project root
- Check that API key and secret are correct
- Ensure no extra spaces in `.env` file

### "Symbol validation failed"
- Check symbol spelling (must be uppercase)
- Verify symbol exists on Binance Futures
- Common symbols: BTCUSDT, ETHUSDT, BNBUSDT

### "Network Error: Connection timeout"
- Check internet connection
- Verify testnet URL is accessible
- Check firewall settings

### "API Error: Signature invalid"
- Regenerate API credentials
- Check system time is synchronized
- Ensure no spaces in API key/secret

## Security Notes

⚠️ **Important Security Practices:**

1. Never commit `.env` file to version control
2. Never share your API keys
3. Use testnet credentials only for testnet
4. Regenerate keys if compromised
5. Set IP restrictions on Binance (optional)

## Advanced Usage

### Using as a Module

```python
from config import config
from binance_client import BinanceClient
from order_service import OrderService
from models import OrderRequest, OrderSide, OrderType

# Initialize
client = BinanceClient(config.API_KEY, config.API_SECRET)
service = OrderService(client)

# Place order
order = OrderRequest(
    symbol="BTCUSDT",
    side=OrderSide.BUY,
    order_type=OrderType.MARKET,
    quantity=0.001
)

response = service.place_order(order)
print(f"Order ID: {response.order_id}")
```

## License

This project is for educational purposes. Use at your own risk.

## Support

For Binance API documentation:
- [Binance Futures API](https://binance-docs.github.io/apidocs/futures/en/)
- [Binance Futures Testnet](https://testnet.binancefuture.com)

For issues with this bot, check the `trading_bot.log` file for detailed error information.
