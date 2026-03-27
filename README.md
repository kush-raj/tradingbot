# Binance Futures Testnet Trading Bot

A simplified Python command-line application for placing Market and Limit orders on the Binance Futures Testnet (USDT-M), complete with input validation and execution logging.

## Features
- **Direct REST API Calls**: Uses HMCA-SHA256 signatures and the requests library. No bloated third-party wrappers required.
- **Rich CLI UX**: Implemented using `click` and `rich` for an interactive, styled terminal experience.
- **Validation**: Strict validation of trading pairs, symbols, order types, prices, and quantities.
- **Robust Logging**: All API traffic, errors, and responses are safely logged to `trading_bot.log`. 

## Prerequisites
- Python 3.8+
- Active Binance Futures Testnet account and API credentials.

## Setup Instructions

1. **Install Requirements**
```bash
pip install -r requirements.txt
```

2. **Configure Environment**
Create a `.env` file in the root directory by copying `.env.example`:
```bash
cp .env.example .env
```
Fill in your API Key and Secret (optional if using mock mode):
```env
BINANCE_API_KEY=mykeys...
BINANCE_API_SECRET=mysecrets...
```

## Running the Bot

You have two ways to run the bot: the Command-Line Interface (CLI) or the new Web UI.

### 1. Web UI (Recommended)
Launch the interactive web application built with Streamlit:
```bash
streamlit run ui.py
```
This will automatically open the web interface in your default browser.

### 2. Command-Line Interface (CLI)

Run the CLI application by calling `cli.py`. You will be interactively prompted for any missing parameters.

**Example: Place a Market Order**
```bash
python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.05
```

**Example: Place a Limit Order**
```bash
python cli.py place-order --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 3500
```

## Logs
Logs are automatically written to `trading_bot.log` in the application root directory. You will see both successful transactions and network/API errors recorded there.

## Project Structure
```text
trading_bot/
  bot/
    __init__.py
    client.py          # HTTP requests and Binance logic
    orders.py          # Service orchestrator (validation -> execution)
    validators.py      # Argument verifications
    logging_config.py  # Logger setup
  cli.py               # Click application entry point
  ui.py                # Streamlit Web UI
  .env.example
  README.md
  requirements.txt
```
## Example Trading Flow
1. Start in Mock Mode
```Test a market buy order:

python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.05 --mock
```
2. Check Logs
```Open trading_bot.log to confirm the simulated order execution
```