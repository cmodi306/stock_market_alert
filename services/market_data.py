import yfinance as yf
from datetime import datetime, timedelta
import requests

def get_stock_summary(symbol:str):
    if yf.Ticker(symbol).history('30d').empty:
        raise ValueError(f"Invalid {symbol}. Please look up for the correct symbol on https://finance.yahoo.com")
    else:
        current_price = round(yf.Ticker(symbol).fast_info['lastPrice'], 3)
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