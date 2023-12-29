import krakenex                   # Import krakenex to interact with the Kraken cryptocurrency exchange API
import plotly.graph_objs as go    # Import Plotly's graph objects for advanced data visualization
import pandas as pd               # Import Pandas for data analysis and manipulation
import numpy as np                # Import NumPy for numerical operations and array processing
import time                       # Import time for time.mktime
import datetime
import streamlit as st

from plotly.subplots import make_subplots

# This function aggregates data into custom time intervals that are not natively provided by the Kraken API to make queries
def aggregate_intervals(interval, df):
        # Resamples the DataFrame to the specified interval and aggregates key metrics
        resampled_df = df.resample(f'{interval}T').agg({ 'Open': 'first', 
                                                         'High': 'max', 
                                                         'Low': 'min', 
                                                         'Close': 'last', 
                                                         'SMA': 'mean', 
                                                         'EMA': 'mean', 
                                                         'Volume': 'sum'})
        return resampled_df

# Retrieves trading data from the Kraken API and stores it in a Pandas DataFrame
@st.cache_data(ttl=300)
def obtain_function(pair, interval, divisor, since, until):
        
    # Initializing a Kraken API client and querying data within a try-except block
    try:
        k = krakenex.API()  # Initialize the Kraken client
        
        # Query for OHLC data for the specified currency pair and interval
        response = k.query_public('OHLC', {'pair':pair, 'interval':divisor, 'since':since})
        if response['error']:  # Check and raise an exception if errors exist in the response
            print(f"There was an error with the API call")
            raise Exception(response['error'])

    # Catch and print any exceptions during the data retrieval process
    except Exception as e:
        print(f"An error occurred: {e}")       # Print the specific error message
        print("Error while retrieving data")   # Indicate a data retrieval error

    # Process the retrieved data if no exceptions occur
    else:
        ohlc_data = response['result'][pair]  # Extract OHLC data from API response

        # Convert OHLC data to a DataFrame and remove unnecessary columns
        ohlc_df = pd.DataFrame(ohlc_data, columns=["Time", "Open", "High", "Low", "Close", "VWAP", "Volume", "Count"]).drop(['VWAP', 'Count'], axis=1)

        # Convert timestamps to datetime format and set as DataFrame index
        ohlc_df["Time"] = pd.to_datetime(ohlc_df["Time"], unit='s')    # Unix timestamp to pandas datetime
        ohlc_df.set_index(pd.DatetimeIndex(ohlc_df["Time"]), inplace=True)
        if until is not None:                                     # Filter data when until is not None
            cutoff_date = pd.to_datetime(until, unit='s')
            ohlc_df = ohlc_df[ohlc_df.index < cutoff_date]

        # Convert all price and volume data to float type for calculations
        ohlc_df["Open"] = ohlc_df["Open"].astype(float)       # Opening price of a financial instrument for the given period
        ohlc_df["High"] = ohlc_df["High"].astype(float)       # Highest price of the instrument in the given period
        ohlc_df["Low"] = ohlc_df["Low"].astype(float)         # Lowest price of the instrument in the given period
        ohlc_df["Close"] = ohlc_df["Close"].astype(float)     # Closing price of the instrument for the given period
        ohlc_df["Volume"] = ohlc_df["Volume"].astype(float)   # Volume of transactions occurred in the given period

        # Add Simple Moving Average (SMA) and Exponential Moving Average (EMA) to the DataFrame
        window = 14 if ohlc_df.shape[0] >= 60 else 3  # Determine window size based on data points
        ohlc_df['SMA'] = ohlc_df['Close'].rolling(window=window).mean()
        ohlc_df['EMA'] = ohlc_df['Close'].ewm(span=window, adjust=False).mean()

        # Aggregate data into custom intervals if needed
        resampled_df = aggregate_intervals(interval, ohlc_df)

        if interval not in (1, 5, 15, 30, 60, 240, 1440, 10080, 21600):
            ohlc_df = resampled_df            
        return ohlc_df  # Return the prepared DataFrame

# The class Graph is designed for constructing candlestick and stochastic oscillator graphs with mobile mean for trading analysis
class Graph:

    # Constructor for initializing a Graph instance
    def __init__(self, pair='XETHZUSD', interval=1440, divisor=1, since=None, until=None):
        self.pair = pair          # The currency pair to be analyzed
        self.interval = interval  # Time interval for each data point in minutes
        self.divisor = divisor    # Divisor for interval adjustment
        self.since = since        # Start of the time window
        self.until = until        # Time limit for the time window

    # Retrieves trading data from the Kraken API and stores it in a Pandas DataFrame
    def obtain_data(self):
        return obtain_function(self.pair, self.interval, self.divisor, self.since, self.until)

    @staticmethod  # Static method to create a candlestick chart from OHLC data using Plotly
    def candlestick(ohlc_df):
        try:
            size = ohlc_df.shape[0]
            if size <= 14:
                df = ohlc_df[:]    # Take the whole dataframe when it has small size
            else:
                df = ohlc_df[14:]  # Remove the first intervals so that SMA is defined

            colors = ['#008080' if close >= open else 'red' for open, close in zip(df['Open'], df['Close'])]
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # Include candlestick with range selector
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='', legendgroup='group', legendrank=1), secondary_y=True)
            
            # Bar diagram displaying the Volume data
            fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=colors, opacity=0.25, showlegend=False), secondary_y=False)
            
            # Line chart displaying the computed SMA values
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA'], marker=dict(color='#0000FF'), opacity=0.35, name='SMA', legendgroup='group', legendrank=2), secondary_y=True)
            
            # Line chart displaying the computed EMA values
            fig.add_trace(go.Scatter(x=df.index, y=df['EMA'], marker=dict(color='#FF0000'), opacity=0.35, name='EMA', legendgroup='group', legendrank=3), secondary_y=True)
            
            fig.layout.yaxis2.showgrid = False
            fig.layout.title = 'Candlestick Graph with Volume and Moving Averages'
            fig.layout.height = 400
            fig.layout.width = 650

            return fig  # Return the Figure object for plotting
        
        except Exception as e:
            # Handle exceptions in chart creation and return an empty figure in case of an error
            print(f"An error occurred while creating the candlestick chart: {e}")
            return go.Figure()  # Return an empty Plotly Figure object if an error occurs


    @staticmethod  # Calculate and graph the stochastic oscillator and its mobile mean 
    def stochastic(df):
        try:
            window = 14 if df.shape[0]>=60 else 3
            df['L14'] = df['Low'].rolling(window=window).min()
            df['H14'] = df['High'].rolling(window=window).max()
            df['%K'] = (df['Close'] - df['L14']) / (df['H14'] - df['L14']) * 100
            df['%D'] = df['%K'].rolling(window=3).mean()
            df['Buy_Signal'] = ((df['%K'] > df['%D']) & (df['%K'].shift(1) < df['%D'].shift(1))) & (df['%D'] < 20)
            df['Sell_Signal'] = ((df['%K'] < df['%D']) & (df['%K'].shift(1) > df['%D'].shift(1))) & (df['%D'] > 80)
            df = df[14:]

            data = [# The first plot is a line chart for the '%D' line of the stochastic oscillator
                    go.Scatter(x=df.index, y=df['%D'], name='Smoothed Stochastic', marker=dict(color='#b2b2b2'), legendgroup='group', legendrank=5),
                    
                    # The second plot is a line chart for the '%K' line of the stochastic oscillator
                    go.Scatter(x=df.index, y=df['%K'], name='Stochastic Oscillator', marker=dict(color='#4c4c4c'), legendgroup='group', legendrank=4),

                    # Horizontal line at 20
                    go.Scatter(x=df.index, y=[20]*len(df.index), mode='lines', name='20% threshold', line=dict(color='purple', width=1, dash='dash'), showlegend=False),

                    # Horizontal line at 80
                    go.Scatter(x=df.index, y=[80]*len(df.index), mode='lines', name='80% threshold', line=dict(color='purple', width=1, dash='dash'), showlegend=False)]

            # Define the layout for the plotly figure, setting titles and axis labels.
            layout = go.Layout(title='Stochastic Oscillator with its Smoothed Version',
                               yaxis=dict(title='Value (%)', range=[0,100]))  # Label for the y-axis

            fig = go.Figure(data=data, layout=layout)  # create a Figure object with the candlestick data
            fig.layout.height = 250
            return fig  # return the Figure object for plotting

        except Exception as e:
            print(f"An error occurred while creating the candlestick chart: {e}")
            return go.Figure()


    def calculate_profit(self, df):
        try:
            coins = 0
            total_spent = 0
            df['Buy_Price'] = np.where(df['Buy_Signal'], df['Close'], np.nan)
            df['Sell_Price'] = np.where(df['Sell_Signal'], df['Close'], np.nan)
            for i in range(len(df)):
                if df['Buy_Signal'].iloc[i]:
                    coins += 100
                    total_spent += df['Buy_Price'].iloc[i]*100
                if df['Sell_Signal'].iloc[i] and coins >= 100:
                    coins -= 100
                    total_spent -= df['Sell_Price'].iloc[i]*100
            df['Profit'] = df['Close'] * coins - total_spent
            return df
        except Exception as e:
            print(f"An error occurred while creating the profit data: {e}")
            return pd.DataFrame()


    def profit_graph(self, df):
        try:
            if not df['Buy_Signal'].any():  # Check if there are any buy signals
                return None  # Return None if no buy signals
            first_buy_signal = df[df['Buy_Signal']].index[0]  # Get the index of the first buy signal
            df = df.loc[first_buy_signal:]  # Slice the DataFrame from the first buy signal onwards
            data = [go.Scatter(x=df.index, y=df['Profit'].cumsum(), name='Profit', marker=dict(color='#0d0c52')),
                    go.Scatter(x=df[df['Buy_Signal']].index, y=df[df['Buy_Signal']]['Profit'].cumsum(), mode='markers', marker=dict(color='#05e3a0', size=10), name='Buy Signal'),
                    go.Scatter(x=df[df['Sell_Signal']].index, y=df[df['Sell_Signal']]['Profit'].cumsum(), mode='markers', marker=dict(color='#f77088', size=10), name='Sell Signal')]
            
            # Adjust layout, including margin settings
            layout = go.Layout(
                yaxis=dict(title='Value'),  # Label for the y-axis
                margin=dict(l=40, r=40, t=20, b=40)  # Adjust left, right, top, bottom margins
            )
            fig = go.Figure(data=data, layout=layout)  # create a Figure object with the profit data
            fig.layout.height = 350
            fig.layout.width = 650
            return fig  # return the Figure object for plotting
        except Exception as e:
            print(f"An error occurred while creating the profit chart: {e}")
            return go.Figure()
