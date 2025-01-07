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

# Inicializa la conexión con Alpaca
client = CryptoHistoricalDataClient("",  # API KEY
                                    "")  # Secret API KEY

try:
    print("Please enter the numerical date from which you want to request the data YYYY/MM/DD")
    initial_year = int(input("Year (YYYY); ").strip() or 2024)
    initial_month = int(input("Month (MM); ").strip() or 12)
    initial_day = int(input("Day (DD); "). strip() or 1)
except ValueError:
    print("Please enter valid numbers")

try:
    print("Please enter the numerical date for the end of the data request YYYY/MM/DD")
    final_year = int(input("Year (YYYY); ").strip() or 2024)
    final_month = int(input("Month (MM); ").strip() or 12)
    final_day = int(input("Day (DD); "). strip() or 31)
except ValueError:
    print("Please enter valid numbers")

# Configure the request parameters
request_params = CryptoBarsRequest(
    symbol_or_symbols=["BTC/USD"],
    timeframe=TimeFrame.Day,
    start=datetime(initial_year, initial_month, initial_day),
    end=datetime(final_year, final_month, final_day)
)

# Makes the request to the Alpaca API and stores the response in `btc_bars`
try:
    BTC_BARS = client.get_crypto_bars(request_params)
except (ConnectionError, TimeoutError, ValueError) as e:
    print(f"Error obtaining the data: {e}")
    BTC_BARS = None


def save_update_csv(dataframe, archive):
    """
    Saves or updates the CSV file with the DataFrame data.
    If the file exists, it replaces it with the new content.
    """
    if os.path.exists(archive):
        os.remove(archive)  # Deletes the existing archive
        print(f"Data of {archive} eliminated to upgrade.")
    else:
        print(
            f"No archive '{archive}' to elimanate, creating a new one with the data.")
    dataframe.to_csv(archive, index=False)  # Saves the new data in a new archive with the same name
    print(f"Archive {archive} created/updated with new data.")


if BTC_BARS is not None:
    # Process the DataFrame
    btc_df = BTC_BARS.df.copy()

    # Reset the index to include the `timestamp` as a column
    btc_df.reset_index(inplace=True)
    # Add percentage change column
    btc_df['percentage_change'] = (
        (btc_df['close'] - btc_df['open']) / btc_df['open']) * 100

    # Name of the CSV
    ARCHIVO_CVS = "bitcoin_data.csv"

    # Llamada a la función para guardar o actualizar
    save_update_csv(btc_df, ARCHIVO_CVS)

else:
    print("Could not get data to save.")

# Ask the user if they want to display the DataFrame
if btc_df is not None:
    print_dataframe = input("Do you want to display th DataFrame? Y/N ")
    if print_dataframe == "Y" or "y":
        print(btc_df)
    else:
        pass
else:
    pass
