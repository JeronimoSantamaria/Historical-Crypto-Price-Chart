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

import os
from datetime import datetime
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical import CryptoHistoricalDataClient


# Define the directory path as a constant
SAVE_DIR = 'data'

def fetch_and_save_data(api_key, api_secret, start_date, end_date, asset):
    """
    Fetch historical cryptocurrency data from Alpaca API and save it to a CSV file.
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
        symbol_or_symbols=[asset],
        timeframe=TimeFrame.Day,
        start=start,
        end=end,
    )

    try:
        # Fetch the data
        btc_bars = client.get_crypto_bars(request_params)
        btc_df = btc_bars.df.copy()
        btc_df.reset_index(inplace=True)

        # Ensure the directory exists
        os.makedirs(SAVE_DIR, exist_ok=True)

        # Define the file path with a fixed name
        file_path = os.path.join(SAVE_DIR, "crypto_data.csv")

        # Delete the old CSV file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)

        # Save the data to a new CSV file
        btc_df.to_csv(file_path, index=False)
        return {"success": "Data fetched and saved successfully."}
    except (ConnectionError, TimeoutError, ValueError, OSError) as e:
        return {"error": f"Error fetching data: {e}"}
