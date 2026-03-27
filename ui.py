import os
import streamlit as st
from dotenv import load_dotenv
from bot.orders import OrderService
from bot.logging_config import setup_logger

load_dotenv()
logger = setup_logger()

st.set_page_config(page_title="Binance Futures Web UI", page_icon="📈", layout="centered")

st.title("📈 Binance Futures Testnet Trading Bot")
st.markdown("Place **Market** and **Limit** orders directly from this web interface.")

# Sidebar for credentials status
st.sidebar.header("Credentials")
api_key = os.getenv("BINANCE_API_KEY", "")
api_secret = os.getenv("BINANCE_API_SECRET", "")


if not api_key or not api_secret or "your_testnet" in api_key:
    st.sidebar.error("❌ API Credentials missing or invalid. Please check your `.env` file.")
else:
    st.sidebar.success("✅ API Credentials loaded.")

# Form
with st.form("order_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        symbol = st.text_input("Symbol", value="BTCUSDT", help="e.g. BTCUSDT")
        side = st.selectbox("Side", options=["BUY", "SELL"])
        
    with col2:
        order_type = st.selectbox("Order Type", options=["MARKET", "LIMIT"])
        quantity = st.number_input("Quantity", min_value=0.001, value=0.01, step=0.01, format="%.3f")
        
    price = None
    if order_type == "LIMIT":
        price = st.number_input("Price (Required for LIMIT)", min_value=0.01, value=60000.0, step=10.0)
        
    submit_button = st.form_submit_button("Place Order")

if submit_button:
    if not api_key or not api_secret or "your_testnet" in api_key:
        st.error("Cannot place order. Missing or invalid API credentials in `.env`.")
        st.stop()
        
    with st.spinner("Executing order on Binance Futures Testnet..."):
        service = OrderService(api_key, api_secret)
        result = service.execute_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        
    if result.get("success"):
        st.success("✅ Order placed successfully!")
        st.json(result.get("data"))
        logger.info("UI: Order placed successfully.")
    else:
        st.error(f"❌ Order failed: {result.get('error')}")
        logger.error(f"UI: Order failed: {result.get('error')}")
