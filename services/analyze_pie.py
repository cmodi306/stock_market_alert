from .market_data import get_stock_summary
import pandas as pd

def analyze_pie(pie: pd.DataFrame):
    pie_current_total_value = 0
    symbol_current_value_list = []
    breakdown = []
    symbols = pie["symbols"]

    for idx, symbol in enumerate(symbols):
        print(symbol)
        stock_data = get_stock_summary(symbol)
        share = pie["shares"][idx]

        current_value = stock_data["current_price"] * share
        high_value = stock_data["highest_price_30d"] * share

        pie_current_total_value += current_value
        
        breakdown.append({
            "symbol": symbol,
            "shares": float(share),
            "current_value": float(round(current_value, 2)),
            "high_30d_value": float(round(high_value, 2)),
        })

        symbol_current_value_list.append(current_value)
    
    pie["current_price"] = symbol_current_value_list
    total_current_price = float(round(pie["current_price"].sum(), 2))
    return pie, {
        "total_current": total_current_price,
        "highest_price_30d": 'n.a.',
        "highest_price_30d_date": 'n.a.',
        "breakdown": breakdown,
    }
