#!/usr/bin/env python3
"""
Setup verification script for Binance Futures Trading Bot
"""
import sys
import os

def check_python_version():
    """Check if Python version is 3.7+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("✗ Python 3.7+ is required")
        print(f"  Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    required = [
        "requests",
        "binance",
        "typer",
        "dotenv",
        "pydantic",
        "rich"
    ]
    
    missing = []
    for package in required:
        try:
            if package == "binance":
                __import__("binance.client")
            elif package == "dotenv":
                __import__("dotenv")
            else:
                __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (missing)")
            missing.append(package)
    
    if missing:
        print("\nInstall missing packages with:")
        print("  pip install -r requirements.txt")
        return False
    
    return True


def check_env_file():
    """Check if .env file exists and is configured"""
    if not os.path.exists(".env"):
        print("✗ .env file not found")
        print("\nCreate .env file:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your Binance Futures Testnet API credentials")
        return False
    
    print("✓ .env file exists")
    
    # Check if credentials are set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or api_key == "your_api_key_here":
        print("✗ BINANCE_API_KEY not configured in .env")
        return False
    
    if not api_secret or api_secret == "your_api_secret_here":
        print("✗ BINANCE_API_SECRET not configured in .env")
        return False
    
    print("✓ API credentials configured")
    return True


def check_file_structure():
    """Check if all required files exist"""
    required_files = [
        "main.py",
        "config.py",
        "logger.py",
        "models.py",
        "exceptions.py",
        "binance_client.py",
        "order_service.py",
        "requirements.txt",
        "README.md"
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} (missing)")
            missing.append(file)
    
    return len(missing) == 0


def main():
    """Run all checks"""
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 12 + "Binance Futures Trading Bot Setup Check" + " " * 8 + "║")
    print("╚" + "=" * 58 + "╝\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("File Structure", check_file_structure),
        ("Dependencies", check_dependencies),
        ("Configuration", check_env_file),
    ]
    
    results = []
    
    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 60)
        result = check_func()
        results.append(result)
    
    print("\n" + "=" * 60)
    
    if all(results):
        print("✓ All checks passed! You're ready to use the trading bot.")
        print("\nNext steps:")
        print("  1. Test connection: python main.py test")
        print("  2. Check balance: python main.py balance")
        print("  3. Place an order: python main.py order BTCUSDT BUY MARKET 0.001")
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
