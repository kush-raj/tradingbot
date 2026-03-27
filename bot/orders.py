from bot.client import BinanceTestnetClient
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price, ValidationError
from bot.logging_config import setup_logger

logger = setup_logger()

class OrderService:
    def __init__(self, api_key: str, api_secret: str):
        self.client = BinanceTestnetClient(api_key, api_secret)
        
    def execute_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        # 1. Validate inputs
        try:
            val_symbol = validate_symbol(symbol)
            val_side = validate_side(side)
            val_type = validate_order_type(order_type)
            val_qty = validate_quantity(quantity)
            val_price = validate_price(price, val_type)
        except ValidationError as e:
            logger.warning(f"Validation error: {e}")
            return {"success": False, "error": str(e)}
            
        # 2. Place order via client
        try:
            response = self.client.place_order(val_symbol, val_side, val_type, val_qty, val_price)
            return {
                "success": True,
                "data": response
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
