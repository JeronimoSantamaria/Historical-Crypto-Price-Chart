'''Transform a CSV file into a list of ints and floats and plot the data using matplotlib.'''

import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd


# Define the directory path as a constant
SAVE_DIR = 'data'

def create_plot(asset):
    """
    Create a plot from the cryptocurrency data CSV file and save it as an image.
    Returns the path to the saved plot image.
    """
    try:
        # Read the CSV file with a fixed name
        csv_file_path = os.path.join(SAVE_DIR, "crypto_data.csv")
        btc_df = pd.read_csv(csv_file_path)
        timestamp = pd.to_datetime(btc_df['timestamp']).astype(int) // 10**9
        dates = [datetime.fromtimestamp(ts) for ts in timestamp]
        close = btc_df['close'].astype(float).tolist()

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(dates, close, marker='o', linestyle='-',
                 color='blue', label='Closing prices (USD)')
        plt.title(f'{asset} Price Evolution', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Closing prices (USD)', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()

        # Save the plot as an image
        plot_path = "static/plot.png"
        plt.savefig(plot_path)
        plt.close()
        return plot_path
    except (pd.errors.EmptyDataError, FileNotFoundError, ValueError) as e:
        print(f"Error creating plot: {e}")
        return None
