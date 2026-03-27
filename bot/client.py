# import hashlib
# import hmac
# import time
# import requests
# from urllib.parse import urlencode
# from bot.logging_config import setup_logger

# logger = setup_logger()

# class BinanceTestnetClient:
#     BASE_URL = "https://testnet.binancefuture.com"
    
#     def __init__(self, api_key: str, api_secret: str):
#         if not api_key or not api_secret:
#             raise ValueError("API Key and Secret must be provided.")
#         self.api_key = api_key
#         self.api_secret = api_secret
#         self.session = requests.Session()
#         self.session.headers.update({
#             "X-MBX-APIKEY": self.api_key
#         })

#     def _generate_signature(self, query_string: str) -> str:
#         return hmac.new(
#             self.api_secret.encode('utf-8'),
#             query_string.encode('utf-8'),
#             hashlib.sha256
#         ).hexdigest()
        
#     def _dispatch_request(self, method: str, endpoint: str, params: dict = None):
#         params = params or {}
#         params['timestamp'] = int(time.time() * 1000)
#         params['recvWindow'] = 5000
        
#         query_string = urlencode(params)
#         signature = self._generate_signature(query_string)
        
#         url = f"{self.BASE_URL}{endpoint}?{query_string}&signature={signature}"
        
#         logger.info(f"Sending {method} request to {endpoint}")
#         try:
#             response = self.session.request(method, url)
#             response.raise_for_status()
#             logger.info(f"Response from {endpoint}: {response.status_code}")
#             return response.json()
#         except requests.exceptions.HTTPError as e:
#             try:
#                 error_msg = response.json()
#                 logger.error(f"Binance API Error: {error_msg}")
#             except Exception:
#                 error_msg = response.text
#                 logger.error(f"HTTP Error: {error_msg}")
#             raise Exception(f"Binance API Error: {error_msg}") from e
#         except requests.exceptions.RequestException as e:
#             logger.error(f"Network error: {str(e)}")
#             raise Exception(f"Network Error: {str(e)}") from e

#     def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
#         endpoint = "/fapi/v1/order"
#         params = {
#             "symbol": symbol,
#             "side": side,
#             "type": order_type,
#             "quantity": quantity
#         }
        
#         if order_type == "LIMIT":
#             params["price"] = price
#             params["timeInForce"] = "GTC"  # Good Till Cancel required for LIMIT
            
#         logger.info(f"Placing order: {params}")
#         return self._dispatch_request("POST", endpoint, params)



import time
import random
from bot.logging_config import setup_logger

logger = setup_logger()


class BinanceTestnetClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        logger.info(f"[MOCK] Placing order: {symbol}, {side}, {order_type}, {quantity}, {price}")

        # simulate delay
        time.sleep(1)

        # fake response
        mock_response = {
            "orderId": random.randint(100000, 999999),
            "symbol": symbol,
            "status": "FILLED" if order_type == "MARKET" else "NEW",
            "clientOrderId": "mockOrder123",
            "executedQty": str(quantity),
            "avgPrice": str(price if price else 65000),
            "type": order_type,
            "side": side
        }

        logger.info(f"[MOCK] Order response: {mock_response}")

        return mock_response