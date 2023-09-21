import requests

# Questrade API endpoints
AUTHORIZATION_URL = "https://login.questrade.com/oauth2/token"
BASE_API_URL = "https://api01.iq.questrade.com/v1/"

# Your Questrade API credentials
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
authorization_code = "YOUR_AUTHORIZATION_CODE"

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
        "symbolId": "YOUR_SYMBOL_ID",  # Obtain the symbol ID for the specific security
        "quantity": quantity,
        "action": "Buy" if is_buy else "Sell",
        "orderType": "Market",
    }

    response = requests.post(BASE_API_URL + "accounts/YOUR_ACCOUNT_NUMBER/orders", headers=headers, json=order_data)
    response_data = response.json()
    return response_data

if __name__ == "__main__":
    access_token = get_access_token()

    # Example: Place a market order to buy 10 shares of a security
    symbol_to_trade = "AAPL"
    order_quantity = 10
    is_buy_order = True

    response = place_market_order(access_token, symbol_to_trade, order_quantity, is_buy_order)
    print("Order Response:", response)