# Quick Start Guide

Get your trading bot running in 5 minutes!

## Step 1: Get API Credentials (2 minutes)

1. Go to https://testnet.binancefuture.com
2. Login with GitHub or Google account
3. Click on your profile → API Keys
4. Generate new API Key
5. Copy the API Key and API Secret

**Note**: Save both values - you won't be able to see the secret again!

## Step 2: Setup (2 minutes)

### Install dependencies:
```bash
pip install requests python-binance typer python-dotenv pydantic rich
```

### Configure credentials:
```bash
# Copy example file
cp .env.example .env

# Edit .env file and paste your credentials
# Replace 'your_api_key_here' with your actual API key
# Replace 'your_api_secret_here' with your actual API secret
```

### Verify setup:
```bash
python setup_check.py
```

## Step 3: Test Connection (30 seconds)

```bash
python main.py test
```

Expected output:
```
✓ Connection successful!
Server time: 1707049247123
```

## Step 4: Your First Order (30 seconds)

### Check your balance first:
```bash
python main.py balance
```

You should see some test USDT in your account.

### Place a small market order:
```bash
python main.py order BTCUSDT BUY MARKET 0.001
```

**Congratulations!** 🎉 You just placed your first order!

## Common Commands Cheat Sheet

```bash
# Place market buy order
python main.py order BTCUSDT BUY MARKET 0.001

# Place market sell order
python main.py order ETHUSDT SELL MARKET 0.01

# Place limit buy order
python main.py order BTCUSDT BUY LIMIT 0.001 --price 45000

# Place limit sell order
python main.py order ETHUSDT SELL LIMIT 0.01 --price 3500

# Check balance
python main.py balance

# Check positions
python main.py positions

# Check specific symbol position
python main.py positions BTCUSDT

# Get help
python main.py --help
```

## Troubleshooting

### "Configuration Error: Missing API credentials"
→ Make sure you created `.env` file and added your actual API credentials

### "Connection Error"
→ Check your internet connection and verify the testnet is accessible

### "Symbol validation failed"
→ Make sure symbol is correct (e.g., BTCUSDT, not BTC-USDT)

### "Price required for LIMIT orders"
→ Add `--price` parameter: `python main.py order BTCUSDT BUY LIMIT 0.001 --price 45000`

## Important Trading Symbols

- `BTCUSDT` - Bitcoin
- `ETHUSDT` - Ethereum
- `BNBUSDT` - Binance Coin
- `ADAUSDT` - Cardano
- `SOLUSDT` - Solana
- `DOGEUSDT` - Dogecoin

## Pro Tips

1. **Start small**: Use small quantities (0.001 BTC, 0.01 ETH) for testing
2. **Check logs**: All operations are logged to `trading_bot.log`
3. **Check balance**: Always check balance before large orders
4. **Use limit orders**: For better price control
5. **Monitor positions**: Check open positions regularly

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [examples.py](examples.py) for programmatic usage
- Review `trading_bot.log` to understand what's happening

## Safety Reminders

✅ This is a TESTNET - no real money involved  
✅ Perfect for learning and testing  
✅ Free test funds provided automatically  
⚠️ Never use testnet credentials on mainnet  
⚠️ Keep your API keys secure  

## Support

Having issues? Check:
1. `trading_bot.log` for detailed error messages
2. [README.md](README.md) troubleshooting section
3. [Binance Futures API Documentation](https://binance-docs.github.io/apidocs/futures/en/)

---

Happy Trading! 🚀
