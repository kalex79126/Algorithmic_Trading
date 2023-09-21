import requests
import pandas as pd
import numpy as np
import time

# Questrade API endpoints
AUTHORIZATION_URL = "https://login.questrade.com/oauth2/token"
BASE_API_URL = "https://api01.iq.questrade.com/v1/"

# Your Questrade API credentials
client_id = "YOUR_CLIENT_ID"               # Replace with your Questrade API client ID
client_secret = "YOUR_CLIENT_SECRET"       # Replace with your Questrade API client secret
authorization_code = "YOUR_AUTHORIZATION_CODE"  # Replace with your authorization code
account_number = "YOUR_ACCOUNT_NUMBER"  # Replace with your account number

# Your watchlist of assets
watchlist = ["AAPL", "GOOGL", "MSFT", "AMZN"]

# Get an access token using OAuth 2.0 authorization code flow
def get_access_token():
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(AUTHORIZATION_URL, data=data)
    response_data = response.json()
    access_token = response_data["access_token"]
    return access_token

# Place a market order
def place_market_order(access_token, symbol, quantity, is_buy):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Define the order parameters based on your requirements
    order_data = {
        "symbolId": "YOUR_SYMBOL_ID",  # Replace with the actual symbol ID
        "quantity": quantity,
        "action": "Buy" if is_buy else "Sell",
        "orderType": "Market",
    }

    response = requests.post(BASE_API_URL + f"accounts/{account_number}/orders", headers=headers, json=order_data)
    response_data = response.json()
    return response_data

# Algorithmic trading strategy
def trading_strategy(df):
    # Implement your trading strategy here
    # Example: Buy if the short-term moving average crosses above the long-term moving average
    if df['SMA10'].iloc[-1] > df['SMA50'].iloc[-1]:
        return True
    else:
        return False

if __name__ == "__main__":
    access_token = get_access_token()

    while True:
        for symbol_to_trade in watchlist:
            # Simulated historical price data for the asset
            data = {
                'Date': pd.date_range(start='2020-01-01', periods=100),
                'Price': np.random.rand(100) * 100 + 100
            }

            df = pd.DataFrame(data)
            df.set_index('Date', inplace=True)
            df['SMA10'] = df['Price'].rolling(window=10).mean()
            df['SMA50'] = df['Price'].rolling(window=50).mean()

            # Execute trading strategy
            if trading_strategy(df):
                order_quantity = 10  # Adjust order quantity as needed
                is_buy_order = True

                response = place_market_order(access_token, symbol_to_trade, order_quantity, is_buy_order)
                print(f"Order Response for {symbol_to_trade}: {response}")

        # Sleep for a while (e.g., 1 hour) before checking the strategy again
        time.sleep(3600)  # Sleep for 1 hour (adjust as needed)