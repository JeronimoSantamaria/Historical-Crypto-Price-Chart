'''Transform a CSV file into a list of ints and floats and plot the data using matplotlib.'''

from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

# Name of the CSV
ARCHIVO_CSV = "bitcoin_data.csv"

# Read the CSV and create a DataFrame
try:
    btc_df = pd.read_csv(ARCHIVO_CSV)
except FileNotFoundError:
    print(f"The {ARCHIVO_CSV} archive does not exist.")
    print("Make sure the file is in the correct location.")
    exit()

# Trasform the CSV file into a list of integers and floats
try:
    # timestamp to UNIX timestam
    timestamp = pd.to_datetime(btc_df['timestamp']).astype(int) // 10**9
    dates_list = timestamp.tolist()

    # Close to float
    close = btc_df['close'].astype(float).tolist()

    # Confirmación
    print("Columns successfully converted to lists:")
    # Display the first 5 elements of each list
    print(f"Dates (timestamp): {dates_list[:5]} ...")
    print(f"Closing prices: {close[:5]} ...")

except KeyError as e:
    print(f"Error: Column {e} is not present in CSV file.")
    exit()

# Transform the UNIX timestamp to datetime
dates = [datetime.fromtimestamp(ts) for ts in timestamp]

# Create the graph
plt.figure(figsize=(10, 6))
plt.plot(dates, close, marker='o', linestyle='-', color='blue', label='Closing prices (USD)')

# Add title and tags
plt.title('Bitcoin Price Evolution', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Closing prices (USD)', fontsize=12)
plt.xticks(rotation=45)  # Rotate X axis labels for better visualization
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

# Display the graph
plt.tight_layout()
plt.show()
