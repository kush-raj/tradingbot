class ValidationError(Exception):
    pass

def validate_symbol(symbol: str) -> str:
    symbol = symbol.upper().strip()
    if not symbol.isalnum():
        raise ValidationError(f"Invalid symbol '{symbol}'. Must be alphanumeric.")
    return symbol

def validate_side(side: str) -> str:
    side = side.upper().strip()
    if side not in ["BUY", "SELL"]:
        raise ValidationError(f"Invalid side '{side}'. Must be BUY or SELL.")
    return side

def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper().strip()
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValidationError(f"Invalid order type '{order_type}'. Must be MARKET or LIMIT.")
    return order_type

def validate_quantity(quantity: float) -> float:
    try:
        qty = float(quantity)
    except ValueError:
        raise ValidationError(f"Invalid quantity '{quantity}'. Must be a number.")
    if qty <= 0:
        raise ValidationError("Quantity must be greater than zero.")
    return qty

def validate_price(price: float, order_type: str) -> float:
    if order_type == "MARKET":
        return None
    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid price '{price}'. LIMIT orders require a numeric price.")
    if p <= 0:
        raise ValidationError("Price must be greater than zero for LIMIT orders.")
    return p
