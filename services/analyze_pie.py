from .market_data import get_stock_summary
import pandas as pd

def analyze_pie(pie: pd.DataFrame):
    pie_current_total_value = 0
    symbol_current_value_list = []
    normalized_highest_price_30d_list = []
    breakdown = []
    symbols = pie["symbols"]

    # Calculate highest price of each symbol
    for idx, symbol in enumerate(symbols):
        stock_data = get_stock_summary(symbol)        
        share = pie["shares"][idx]

        current_value = stock_data["current_price"] * share
        normalized_highest_price_30d = stock_data["highest_price_30d"] * share

        pie_current_total_value += round(float(current_value), 3)
        
        breakdown.append({
            "symbol": symbol,
            "shares": float(share),
            "current_value": float(round(current_value, 2)),
            "high_30d_value": float(round(normalized_highest_price_30d, 2)),
        })

        symbol_current_value_list.append(current_value)
        normalized_highest_price_30d_list.append(normalized_highest_price_30d)
    
    # Calculate total price of all symbols
    pie["current_price"] = symbol_current_value_list
    
    # Calculate average highest price of all symbols in the last 30 days
    pie["normalized_highest_price_30d_list"] = normalized_highest_price_30d_list

    total_current_price = float(round(pie["current_price"].sum(), 4))
    total_normalized_highest_price_30d = float(round(pie["normalized_highest_price_30d_list"].sum(), 4))
    deviation_from_high = float(round(((total_current_price/total_normalized_highest_price_30d) - 1)*100, 4)) 
    
    return pie, {
        "total_current": total_current_price,
        "mean_normalized_highest_price_30d": total_normalized_highest_price_30d,
        "deviation_from_high": deviation_from_high,
        "breakdown": breakdown,
    }
