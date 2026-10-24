from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass
from dotenv import load_dotenv
import os

load_dotenv(".env.local")
api_key = os.getenv("api_key")
secret_key = os.getenv("secret_key")
base_url = os.getenv("base_url")

# Raw assets avoid SDK exchange-enum failures for new exchanges such as TXSE.
client = TradingClient(
    api_key, secret_key, paper=True, url_override=base_url, raw_data=True
)

# 1. Fetch all active, tradable US Stocks
stock_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY, status="active")
all_stocks = client.get_all_assets(stock_params)
stock_symbols = [asset["symbol"] for asset in all_stocks if asset["tradable"]]

# 2. Fetch all active Crypto pairs
crypto_params = GetAssetsRequest(asset_class=AssetClass.CRYPTO, status="active")
all_crypto = client.get_all_assets(crypto_params)
crypto_symbols = [asset["symbol"] for asset in all_crypto if asset["tradable"]]

print(f"Total Tradable Stocks: {len(stock_symbols)}")
print(f"Total Tradable Crypto Pairs: {len(crypto_symbols)}")


# create a json file with all the results
import json

results = {"stock_symbols": stock_symbols, "crypto_symbols": crypto_symbols}

with open("symbols.json", "w") as f:
    json.dump(results, f)
