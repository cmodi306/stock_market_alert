# Stock Market Alert

A FastAPI-based web application that evaluates how far the current price of individual stocks—and entire stock pies—are from their highest prices over the last 30 days.

Upload a CSV of your portfolio or enter stock positions manually, and the app will calculate the deviation from recent highs using real-time data fetched through the Yahoo Finance (yfinance) API.

## Features
### Stock-Level Analysis

Enter any stock symbol. App fetches:
- Current price
- Highest closing price in the last 30 days
- Date of the highest price
- Gain/Loss % from that recent high

### Portfolio (“Pie”) Analysis

Upload a CSV containing your stock pie or enter positions manually. CSV must contain stock symbols and shares.
The app calculates:
- Current total value of the pie
- Normalized value at each stock’s 30-day high (shares × highest 30-day price)
- Deviation of current pie value relative to recent highs
- Breakdown by individual stocks

Your CSV must contain exactly the following two columns:

|symbols|shares|
| ------ | ----- |
|AAPL|10|
|MSFT|5|
|TSLA|12|

** Note: Make sure the symbols match Yahoo Finance tickers exactly (e.g., AAPL, MSFT, GOOGL, etc.).**

### CSV Output

After analysis, a processed CSV is saved containing:
- Symbols
- Shares
- Current total value per symbol
- Normalized highest price value per symbol

## How to use

```
git clone https://github.com/cmodi306/stock_market_alert.git
cd stock_market_alert
fastapi dev main.py 
```

This will create a server on your localhost. Visit [localhost:8000](localhost.com:8000) to use the app.