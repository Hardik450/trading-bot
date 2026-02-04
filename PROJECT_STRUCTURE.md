# Project Structure

## Overview
```
binance-trading-bot/
│
├── main.py                 # CLI application entry point
├── config.py               # Configuration management
├── logger.py               # Logging utilities
├── models.py               # Pydantic data models
├── exceptions.py           # Custom exceptions
├── binance_client.py       # Binance API client
├── order_service.py        # Business logic layer
│
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Your credentials (DO NOT COMMIT)
├── .gitignore             # Git ignore rules
│
├── README.md              # Full documentation
├── QUICKSTART.md          # Quick start guide
├── setup_check.py         # Setup verification script
├── examples.py            # Usage examples
│
└── trading_bot.log        # Generated log file (DO NOT COMMIT)
```

## Module Descriptions

### Core Application Files

#### `main.py`
- **Purpose**: CLI application entry point
- **Features**:
  - Command-line interface using Typer
  - Rich terminal output with tables and colors
  - Commands: order, balance, positions, test
  - Input validation and error handling
  - User-friendly error messages

#### `config.py`
- **Purpose**: Centralized configuration management
- **Features**:
  - Environment variable loading
  - Configuration validation
  - Default values
  - Testnet URL configuration

#### `logger.py`
- **Purpose**: Logging setup and utilities
- **Features**:
  - File and console logging
  - Configurable log levels
  - Structured log format
  - Automatic log file creation

### Business Logic Layer

#### `models.py`
- **Purpose**: Data models with validation
- **Features**:
  - Pydantic models for type safety
  - Order request validation
  - Order response parsing
  - Enum types for sides and order types
  - Custom field validators

#### `exceptions.py`
- **Purpose**: Custom exception hierarchy
- **Features**:
  - TradingBotException (base)
  - ConfigurationError
  - BinanceAPIError
  - NetworkError
  - ValidationError

#### `binance_client.py`
- **Purpose**: Low-level Binance API interaction
- **Features**:
  - HMAC SHA256 signature generation
  - Request signing and authentication
  - HTTP request handling
  - Error parsing
  - Rate limiting awareness
  - Methods: place_order, get_account_info, get_exchange_info, etc.

#### `order_service.py`
- **Purpose**: High-level order management
- **Features**:
  - Symbol validation
  - Order placement orchestration
  - Account balance queries
  - Position management
  - Business logic separation from API calls

### Utility Files

#### `setup_check.py`
- **Purpose**: Environment setup verification
- **Features**:
  - Python version check
  - Dependency verification
  - Configuration validation
  - File structure check
  - Helpful error messages

#### `examples.py`
- **Purpose**: Programmatic usage examples
- **Features**:
  - Market order examples
  - Limit order examples
  - Balance checking
  - Position monitoring
  - Error handling demonstrations

### Configuration Files

#### `requirements.txt`
- **Dependencies**:
  - requests: HTTP client
  - python-binance: Binance API wrapper (optional)
  - typer: CLI framework
  - python-dotenv: Environment variable loading
  - pydantic: Data validation
  - rich: Terminal formatting

#### `.env.example`
- **Purpose**: Template for environment variables
- **Contains**:
  - BINANCE_API_KEY placeholder
  - BINANCE_API_SECRET placeholder
  - Instructions

#### `.gitignore`
- **Purpose**: Prevent sensitive files from being committed
- **Excludes**:
  - .env (credentials)
  - *.log (log files)
  - __pycache__/ (Python cache)
  - Virtual environments

### Documentation Files

#### `README.md`
- **Comprehensive documentation**:
  - Feature list
  - Architecture overview
  - Setup instructions
  - Usage examples
  - Error handling guide
  - Troubleshooting
  - Security notes

#### `QUICKSTART.md`
- **Fast start guide**:
  - 5-minute setup
  - Step-by-step instructions
  - Common commands
  - Pro tips

## Architecture Layers

### Layer 1: CLI (Presentation)
- `main.py`
- User interaction
- Input parsing
- Output formatting

### Layer 2: Business Logic (Service)
- `order_service.py`
- Validation
- Orchestration
- High-level operations

### Layer 3: API Client (Data Access)
- `binance_client.py`
- HTTP communication
- Authentication
- Request/response handling

### Cross-Cutting Concerns
- `config.py` - Configuration
- `logger.py` - Logging
- `models.py` - Data structures
- `exceptions.py` - Error handling

## Data Flow

### Placing an Order
```
User Input (CLI)
    ↓
main.py (validation & parsing)
    ↓
OrderRequest model (validation)
    ↓
OrderService (business logic)
    ↓
BinanceClient (API communication)
    ↓
Binance API
    ↓
OrderResponse model (parsing)
    ↓
main.py (display results)
```

## Design Patterns Used

1. **Separation of Concerns**: Clear layer boundaries
2. **Dependency Injection**: Services receive clients
3. **Single Responsibility**: Each module has one job
4. **Factory Pattern**: Model creation and validation
5. **Strategy Pattern**: Different order types
6. **Error Handling**: Custom exception hierarchy

## Best Practices Implemented

✅ Type hints throughout  
✅ Pydantic for validation  
✅ Comprehensive error handling  
✅ Structured logging  
✅ Environment-based configuration  
✅ Clear documentation  
✅ Code reusability  
✅ Security considerations  

## Extensibility Points

### Adding New Order Types
1. Add enum value to `OrderType` in models.py
2. Update validation in `OrderRequest`
3. Add support in `BinanceClient.place_order()`
4. Update CLI help text

### Adding New Commands
1. Add `@app.command()` in main.py
2. Implement business logic in `order_service.py`
3. Add API method in `binance_client.py` if needed
4. Update documentation

### Custom Strategies
1. Create new service class extending base patterns
2. Implement strategy logic
3. Use existing `BinanceClient` for API calls
4. Add CLI command or use programmatically

## Security Considerations

🔒 **Credentials**: Stored in .env, never in code  
🔒 **Logging**: Sensitive data not logged  
🔒 **Git**: .env excluded from version control  
🔒 **HTTPS**: All API calls over secure connection  
🔒 **Signatures**: HMAC SHA256 for authentication  

## Testing Strategy

### Manual Testing
- `setup_check.py` - Environment verification
- `python main.py test` - Connection test
- Small order amounts for live testing

### Programmatic Testing
- `examples.py` - Demonstrates API usage
- Can be extended with unit tests
- Mock API responses for testing

## Deployment Notes

### Requirements
- Python 3.7+
- Internet connection
- Valid Binance Futures Testnet credentials

### Installation
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with credentials
python setup_check.py
python main.py test
```

### Production Considerations
⚠️ This is designed for TESTNET only  
⚠️ For production (mainnet):
- Change base URL
- Use mainnet credentials
- Implement additional safety checks
- Add confirmation prompts
- Consider rate limiting
- Add position size limits

## Maintenance

### Log Management
- Logs stored in `trading_bot.log`
- Rotate logs periodically
- Monitor log file size

### Dependency Updates
```bash
pip list --outdated
pip install --upgrade package_name
```

### API Version Updates
- Monitor Binance API changelog
- Test thoroughly after updates
- Update signature method if needed

---

For questions or issues, refer to the main [README.md](README.md) or check the logs.
