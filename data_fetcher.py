"""
This script fetches historical cryptocurrency data from the Alpaca API and saves it to a CSV file.
Steps:
1. Initializes Alpaca API connection.
2. Prompts user for start and end dates.
3. Configures request and fetches data.
4. Processes data, calculates percentage change.
5. Saves/updates data in a CSV file.
6. Optionally prints the DataFrame.
"""
from datetime import datetime
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical import CryptoHistoricalDataClient

def fetch_and_save_data(api_key, api_secret, start_date, end_date):
    """
    Fetch historical Bitcoin data from Alpaca API and save it to a CSV file.
    Returns a dictionary with success or error message.
    """
    # Initialize Alpaca API connection
    client = CryptoHistoricalDataClient(api_key, api_secret)
    try:
        # Parse the start and end dates
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format."}

    # Configure the request parameters
    request_params = CryptoBarsRequest(
        symbol_or_symbols=["BTC/USD"],
        timeframe=TimeFrame.Day,
        start=start,
        end=end,
    )

    try:
        # Fetch the data
        btc_bars = client.get_crypto_bars(request_params)
        btc_df = btc_bars.df.copy()
        btc_df.reset_index(inplace=True)
        btc_df['percentage_change'] = (
            (btc_df['close'] - btc_df['open']) / btc_df['open']) * 100
        # Save the data to a CSV file
        btc_df.to_csv("bitcoin_data.csv", index=False)
        return {"success": "Data fetched and saved successfully."}
    except (ConnectionError, TimeoutError, ValueError) as e:
        return {"error": f"Error fetching data: {e}"}
