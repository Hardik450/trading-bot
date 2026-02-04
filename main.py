#!/usr/bin/env python3
"""
Binance Futures Trading Bot - CLI Application
"""
import sys
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from config import config
from logger import setup_logger
from binance_client import BinanceClient
from order_service import OrderService
from models import OrderRequest, OrderSide, OrderType
from exceptions import (
    TradingBotException,
    ConfigurationError,
    BinanceAPIError,
    NetworkError,
    ValidationError
)

# Initialize
app = typer.Typer(
    help="Binance Futures Trading Bot - Place orders on Binance Futures Testnet",
    add_completion=False
)
console = Console()
logger = setup_logger(__name__)


def check_configuration():
    """Check if configuration is valid"""
    if not config.validate():
        missing = config.get_missing_config()
        console.print("\n[bold red]❌ Configuration Error[/bold red]")
        console.print("\nMissing required configuration:")
        for item in missing:
            console.print(f"  • {item}")
        console.print("\n[yellow]Please set up your .env file with Binance API credentials.[/yellow]")
        console.print("Copy .env.example to .env and add your credentials.\n")
        raise ConfigurationError("Missing API credentials")


@app.command()
def order(
    symbol: str = typer.Argument(..., help="Trading pair symbol (e.g., BTCUSDT)"),
    side: str = typer.Argument(..., help="Order side: BUY or SELL"),
    order_type: str = typer.Argument(..., help="Order type: MARKET or LIMIT"),
    quantity: float = typer.Argument(..., help="Order quantity"),
    price: Optional[float] = typer.Option(None, "--price", "-p", help="Limit price (required for LIMIT orders)"),
):
    """
    Place an order on Binance Futures Testnet
    
    Examples:
    
        # Market buy order
        python main.py order BTCUSDT BUY MARKET 0.001
        
        # Limit sell order
        python main.py order BTCUSDT SELL LIMIT 0.001 --price 50000
    """
    try:
        # Check configuration
        check_configuration()
        
        # Display header
        console.print("\n")
        console.print(Panel.fit(
            "[bold cyan]Binance Futures Trading Bot[/bold cyan]\n"
            "[dim]Testnet Environment[/dim]",
            border_style="cyan"
        ))
        console.print()
        
        # Validate and normalize inputs
        side_upper = side.upper()
        type_upper = order_type.upper()
        
        if side_upper not in ["BUY", "SELL"]:
            raise ValidationError(f"Invalid side '{side}'. Must be BUY or SELL")
        
        if type_upper not in ["MARKET", "LIMIT"]:
            raise ValidationError(f"Invalid order type '{order_type}'. Must be MARKET or LIMIT")
        
        # Create order request
        order_request = OrderRequest(
            symbol=symbol,
            side=OrderSide(side_upper),
            order_type=OrderType(type_upper),
            quantity=quantity,
            price=price
        )
        
        # Display order request
        table = Table(title="Order Request", show_header=False, border_style="blue")
        table.add_column("Field", style="cyan", width=15)
        table.add_column("Value", style="white")
        
        table.add_row("Symbol", order_request.symbol)
        # FIXED
        table.add_row("Side", order_request.side.upper())
        table.add_row("Type", order_request.order_type.upper())

        table.add_row("Quantity", str(order_request.quantity))
        if order_request.price:
            table.add_row("Price", str(order_request.price))
        
        console.print(table)
        console.print()
        
        # Initialize client and service
        client = BinanceClient(
            api_key=config.API_KEY,
            api_secret=config.API_SECRET,
            base_url=config.TESTNET_BASE_URL
        )
        service = OrderService(client)
        
        # Place order
        with console.status("[bold green]Placing order...", spinner="dots"):
            order_response = service.place_order(order_request)
        
        # Display response
        console.print("[bold green]✓ Order placed successfully![/bold green]\n")
        
        response_table = Table(title="Order Response", show_header=False, border_style="green")
        response_table.add_column("Field", style="cyan", width=20)
        response_table.add_column("Value", style="white")
        
        response_table.add_row("Order ID", str(order_response.order_id))
        response_table.add_row("Symbol", order_response.symbol)
        response_table.add_row("Status", f"[bold]{order_response.status}[/bold]")
        response_table.add_row("Side", order_response.side)
        response_table.add_row("Type", order_response.order_type)
        response_table.add_row("Quantity", order_response.quantity)
        response_table.add_row("Executed Quantity", order_response.executed_qty)
        
        if order_response.price and float(order_response.price) > 0:
            response_table.add_row("Price", order_response.price)
        
        if order_response.avg_price and float(order_response.avg_price) > 0:
            response_table.add_row("Average Price", f"[bold]{order_response.avg_price}[/bold]")
        
        if order_response.cumulative_quote_qty:
            response_table.add_row("Total Value", order_response.cumulative_quote_qty)
        
        console.print(response_table)
        console.print()
        
        logger.info(f"Order completed successfully: Order ID {order_response.order_id}")
        
    except ValidationError as e:
        console.print(f"\n[bold red]❌ Validation Error:[/bold red] {e}\n")
        logger.error(f"Validation error: {e}")
        sys.exit(1)
    except BinanceAPIError as e:
        console.print(f"\n[bold red]❌ Binance API Error:[/bold red] {e}")
        if e.code:
            console.print(f"[dim]Error code: {e.code}[/dim]\n")
        logger.error(f"Binance API error: {e}")
        sys.exit(1)
    except NetworkError as e:
        console.print(f"\n[bold red]❌ Network Error:[/bold red] {e}\n")
        logger.error(f"Network error: {e}")
        sys.exit(1)
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]❌ Unexpected Error:[/bold red] {e}\n")
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


@app.command()
def balance():
    """
    Get account balance information
    """
    try:
        check_configuration()
        
        console.print("\n")
        console.print(Panel.fit(
            "[bold cyan]Account Balance[/bold cyan]",
            border_style="cyan"
        ))
        
        client = BinanceClient(
            api_key=config.API_KEY,
            api_secret=config.API_SECRET,
            base_url=config.TESTNET_BASE_URL
        )
        service = OrderService(client)
        
        with console.status("[bold green]Fetching balance...", spinner="dots"):
            account_info = service.get_account_balance()
        
        console.print()
        
        # Display assets with balance
        table = Table(title="Assets", border_style="green")
        table.add_column("Asset", style="cyan", width=10)
        table.add_column("Wallet Balance", style="white", justify="right")
        table.add_column("Available Balance", style="green", justify="right")
        
        for asset in account_info.get("assets", []):
            balance = float(asset.get("walletBalance", 0))
            if balance > 0:
                table.add_row(
                    asset.get("asset"),
                    asset.get("walletBalance"),
                    asset.get("availableBalance")
                )
        
        console.print(table)
        console.print()
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {e}\n")
        logger.error(f"Error fetching balance: {e}", exc_info=True)
        sys.exit(1)


@app.command()
def positions(
    symbol: Optional[str] = typer.Argument(None, help="Trading pair symbol (optional)")
):
    """
    Get current positions
    """
    try:
        check_configuration()
        
        console.print("\n")
        title = f"Positions - {symbol}" if symbol else "All Positions"
        console.print(Panel.fit(f"[bold cyan]{title}[/bold cyan]", border_style="cyan"))
        
        client = BinanceClient(
            api_key=config.API_KEY,
            api_secret=config.API_SECRET,
            base_url=config.TESTNET_BASE_URL
        )
        service = OrderService(client)
        
        with console.status("[bold green]Fetching positions...", spinner="dots"):
            positions_data = service.get_positions(symbol=symbol)
        
        console.print()
        
        # Display positions
        table = Table(title="Open Positions", border_style="green")
        table.add_column("Symbol", style="cyan")
        table.add_column("Position Amount", style="white", justify="right")
        table.add_column("Entry Price", style="white", justify="right")
        table.add_column("Unrealized PnL", style="white", justify="right")
        table.add_column("Leverage", style="white", justify="right")
        
        has_positions = False
        for pos in positions_data:
            amount = float(pos.get("positionAmt", 0))
            if amount != 0:
                has_positions = True
                pnl = float(pos.get("unRealizedProfit", 0))
                pnl_style = "green" if pnl >= 0 else "red"
                
                table.add_row(
                    pos.get("symbol"),
                    pos.get("positionAmt"),
                    pos.get("entryPrice"),
                    f"[{pnl_style}]{pos.get('unRealizedProfit')}[/{pnl_style}]",
                    pos.get("leverage")
                )
        
        if has_positions:
            console.print(table)
        else:
            console.print("[dim]No open positions[/dim]")
        
        console.print()
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {e}\n")
        logger.error(f"Error fetching positions: {e}", exc_info=True)
        sys.exit(1)


@app.command()
def test():
    """
    Test connection to Binance Futures Testnet
    """
    try:
        check_configuration()
        
        console.print("\n")
        console.print(Panel.fit(
            "[bold cyan]Testing Connection[/bold cyan]",
            border_style="cyan"
        ))
        console.print()
        
        client = BinanceClient(
            api_key=config.API_KEY,
            api_secret=config.API_SECRET,
            base_url=config.TESTNET_BASE_URL
        )
        
        with console.status("[bold green]Testing connection...", spinner="dots"):
            server_time = client.get_server_time()
        
        console.print("[bold green]✓ Connection successful![/bold green]")
        console.print(f"[dim]Server time: {server_time}[/dim]\n")
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Connection failed:[/bold red] {e}\n")
        logger.error(f"Connection test failed: {e}", exc_info=True)
        sys.exit(1)


def main():
    """Entry point for the application"""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
