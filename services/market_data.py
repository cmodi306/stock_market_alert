import yfinance as yf
from datetime import datetime, timedelta
import requests

def get_fx_rate_to_usd(currency: str) -> float:
    if currency == "USD":
        return 1.0
    fx_symbol = f"{currency}USD=X"
    fx = yf.Ticker(fx_symbol).fast_info.get("lastPrice")
    if fx is None:
        raise ValueError(f"FX rate not found for {currency}")

    return float(fx)

def get_stock_summary(symbol:str):
    if yf.Ticker(symbol).history('30d').empty:
        raise ValueError(f"Invalid {symbol}. Please look up for the correct symbol on https://finance.yahoo.com")
    else:
        fast = yf.Ticker(symbol).fast_info
        currency = fast.get("currency", "USD")
        fx_rate = get_fx_rate_to_usd(currency)
        current_price = round(fast["lastPrice"] * fx_rate, 3)
        stock_price_history_30d  = round(yf.Ticker(symbol).history('30d'), 3)
        highest_price_30d = float(stock_price_history_30d.max()['Close'])
        highest_price_30d_date = stock_price_history_30d.idxmax()['Close'].date()
        gain_loss_ratio = round(((current_price/highest_price_30d) -1) * 100, 3)
        return {
            "symbol": symbol.upper(),
            "current_price": current_price,
            "highest_price_30d": highest_price_30d,
            "highest_price_30d_date": highest_price_30d_date,
            "gain_loss_ratio": gain_loss_ratio
        }