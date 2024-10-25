import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import time
from IPython.display import clear_output

# Function to fetch and update the plot in intervals
def plot_realtime_stock(stock_symbol, interval_sec=10, duration_min=1):
    stock_data = yf.Ticker(stock_symbol)
    
    # List to hold fetched prices
    times = []
    prices = []
    
    start_time = time.time()
    end_time = start_time + duration_min * 60
    
    while time.time() < end_time:
        # Fetch the latest stock price
        latest_data = stock_data.history(period="1d", interval="1m")  # 1-minute interval
        
        # Extract the latest price and time
        latest_price = latest_data['Close'].iloc[-1]
        latest_time = latest_data.index[-1]
        
        # Append to lists
        times.append(latest_time)
        prices.append(latest_price)
        
        # Plot the data
        clear_output(wait=True)  # Clear the previous output for live updating
        plt.figure(figsize=(10, 6))
        plt.plot(times, prices, marker='o', linestyle='-', color='b')
        plt.title(f'Real-time Stock Price for {stock_symbol}')
        plt.xlabel('Time')
        plt.ylabel('Price (INR)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
        # Wait for the next update
        time.sleep(interval_sec)

# Use Google Colab to visualize real-time plotting of stock prices (e.g., RELIANCE.NS)
plot_realtime_stock('RELIANCE.NS', interval_sec=10, duration_min=1)  # Run for 1 minute with 10-sec interval

