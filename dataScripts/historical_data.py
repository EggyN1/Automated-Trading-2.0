import datetime
from alpaca.data.enums import DataFeed
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(".env.local")
API_KEY = os.getenv("api_key")
SECRET_KEY = os.getenv("secret_key")

missing_credentials = [
    name
    for name, value in (("api_key", API_KEY), ("secret_key", SECRET_KEY))
    if not value or not value.strip()
]


# Initialize the historical data client
client = StockHistoricalDataClient(API_KEY, SECRET_KEY)


def get_historical_data(symbol):
    data = []
    request_params = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.hour,
        start=datetime.datetime.now() - datetime.timedelta(days=30),
        end=datetime.datetime.now(),
        feed=DataFeed.IEX,
    )

    bars = client.get_stock_bars(request_params)
    for bar in bars[symbol]:
        data.append(
            {
                "time": bar.timestamp,
                "open": bar.open,
                "high": bar.high,
                "low": bar.low,
                "close": bar.close,
                "volume": bar.volume,
            }
        )
    return data


print(
    get_historical_data("AAPL")
)  # Replace "AAPL" with the desired stock symbol or name
