# import os
# import click
# from rich.console import Console
# from rich.table import Table
# from rich.panel import Panel
# from dotenv import load_dotenv

# from bot.orders import OrderService
# from bot.logging_config import setup_logger

# load_dotenv()
# logger = setup_logger()
# console = Console()

# @click.group()
# def cli():
#     """Binance Futures Testnet Trading Bot CLI."""
#     pass

# @cli.command()
# @click.option('--symbol', prompt='Trading Symbol (e.g., BTCUSDT)', help='The trading pair symbol.')
# @click.option('--side', prompt='Order Side (BUY/SELL)', type=click.Choice(['BUY', 'SELL'], case_sensitive=False))
# @click.option('--type', 'order_type', prompt='Order Type (MARKET/LIMIT)', type=click.Choice(['MARKET', 'LIMIT'], case_sensitive=False))
# @click.option('--quantity', prompt='Quantity', type=float, help='Amount to buy/sell.')
# @click.option('--price', type=float, default=None, help='Price for LIMIT orders.')
# def place_order(symbol, side, order_type, quantity, price):
#     """Places a new order on Binance Futures Testnet."""
#     api_key = os.getenv("BINANCE_API_KEY")
#     api_secret = os.getenv("BINANCE_API_SECRET")
    
#     if not api_key or not api_secret:
#         console.print("[bold red]Error: API credentials not found.[/bold red]")
#         console.print("Please set BINANCE_API_KEY and BINANCE_API_SECRET in your .env file.")
#         raise click.Abort()
        
#     if order_type.upper() == "LIMIT" and price is None:
#         price = click.prompt("Price (required for LIMIT)", type=float)
        
#     # Print summary
#     summary_table = Table(title="Order Request Summary")
#     summary_table.add_column("Parameter", style="cyan")
#     summary_table.add_column("Value", style="magenta")
#     summary_table.add_row("Symbol", symbol.upper())
#     summary_table.add_row("Side", side.upper())
#     summary_table.add_row("Type", order_type.upper())
#     summary_table.add_row("Quantity", str(quantity))
#     if price:
#         summary_table.add_row("Price", str(price))
        
#     console.print(summary_table)
    
#     if not click.confirm("Do you want to proceed with this order?"):
#         console.print("[yellow]Order cancelled by user.[/yellow]")
#         return
        
#     console.print("[yellow]Sending order to Binance Futures Testnet...[/yellow]")
    
#     service = OrderService(api_key, api_secret)
#     result = service.execute_order(symbol, side, order_type, quantity, price)
    
#     if result["success"]:
#         data = result["data"]
#         console.print(Panel("[bold green]Order Placed Successfully![/bold green]"))
        
#         response_table = Table(title="Order Details")
#         response_table.add_column("Field", style="cyan")
#         response_table.add_column("Value", style="green")
        
#         fields_to_show = ["orderId", "status", "clientOrderId", "executedQty", "avgPrice", "type", "side"]
#         for field in fields_to_show:
#             if field in data:
#                 response_table.add_row(field, str(data[field]))
                
#         console.print(response_table)
#         logger.info("CLI: Order placed successfully.")
#     else:
#         console.print(Panel(f"[bold red]Order Failed![/bold red]\n\n{result['error']}"))
#         logger.error(f"CLI: Order failed: {result['error']}")

# if __name__ == '__main__':
#     cli()




import os
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from dotenv import load_dotenv

from bot.orders import OrderService
from bot.logging_config import setup_logger

# Load environment variables
load_dotenv()

logger = setup_logger()
console = Console()

@click.group()
def cli():
    """Binance Futures Testnet Trading Bot CLI."""
    pass


@cli.command()
@click.option('--symbol', prompt='Trading Symbol (e.g., BTCUSDT)', help='Trading pair symbol')
@click.option('--side', prompt='Order Side (BUY/SELL)', type=click.Choice(['BUY', 'SELL'], case_sensitive=False))
@click.option('--type', 'order_type', prompt='Order Type (MARKET/LIMIT)', type=click.Choice(['MARKET', 'LIMIT'], case_sensitive=False))
@click.option('--quantity', prompt='Quantity', type=float)
@click.option('--price', type=float, default=None, help='Price (required for LIMIT orders)')
def place_order(symbol, side, order_type, quantity, price):
    """Place order on Binance Futures Testnet (USDT-M)."""

    # ✅ Load Futures API keys
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        console.print("[bold red]❌ API credentials not found[/bold red]")
        console.print("Set BINANCE_API_KEY and BINANCE_API_SECRET in .env file")
        logger.error("Missing API credentials")
        raise click.Abort()

    # ✅ Validate LIMIT price
    if order_type.upper() == "LIMIT" and price is None:
        price = click.prompt("Enter Price (required for LIMIT)", type=float)

    # ✅ Order Summary
    summary = Table(title="Order Request Summary")
    summary.add_column("Parameter", style="cyan")
    summary.add_column("Value", style="magenta")

    summary.add_row("Symbol", symbol.upper())
    summary.add_row("Side", side.upper())
    summary.add_row("Type", order_type.upper())
    summary.add_row("Quantity", str(quantity))

    if price:
        summary.add_row("Price", str(price))

    console.print(summary)

    if not click.confirm("Proceed with order?"):
        console.print("[yellow]Order cancelled[/yellow]")
        return

    console.print("[yellow]Sending order to Binance Futures Testnet...[/yellow]")
    logger.info(f"Placing order: {symbol} {side} {order_type} {quantity} {price}")

    # ✅ Call Order Service
    service = OrderService(api_key, api_secret)
    result = service.execute_order(symbol, side, order_type, quantity, price)

    # ✅ Handle response
    if result.get("success"):
        data = result.get("data", {})

        console.print(Panel("[bold green]✅ Order Placed Successfully[/bold green]"))

        table = Table(title="Order Details")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        fields = ["orderId", "status", "executedQty", "avgPrice", "type", "side"]

        for field in fields:
            if field in data:
                table.add_row(field, str(data[field]))

        console.print(table)
        logger.info(f"Order success: {data}")

    else:
        error_msg = result.get("error", "Unknown error")
        console.print(Panel(f"[bold red]❌ Order Failed[/bold red]\n\n{error_msg}"))
        logger.error(f"Order failed: {error_msg}")


if __name__ == '__main__':
    cli()