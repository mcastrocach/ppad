import json
import krakenex                   # Import the krakenex library to interact with the Kraken cryptocurrency exchange
import plotly.graph_objs as go    # Import plotly's graph objects for creating various types of plots
import pandas as pd               # Import pandas to manipulate the retrieved currency data
import numpy as np


intervals = (1, 5, 15, 30, 60, 240, 1440, 10080, 21600)

# Definition of the class Graph to create candlestick and stochastic oscillator (w/ mobile mean) graphs for trading analysis
class Graph:

    # Initializing the class with a default currency pair and time interval
    def __init__(self, pair='XETHZUSD', interval=1440, divisor=1):
        self.pair = pair
        self.interval = interval
        self.divisor = divisor

    # Function to aggregate the information in specific intervals that are not available for direct data retrieval using the API
    def aggregate_intervals(self, df):
        resampled_df = df.resample(f'{self.interval}T').agg({'Open':'first', 'High':'max', 'Low':'min', 'Close':'last', 'Volume':'sum'})
        return resampled_df

    # Retrieving all the useful information from the Kraken API and storing it in a pandas dataframe
    def obtain_data(self):
        
        # Attempt to perform operations that may fail
        try:
            k = krakenex.API()  # initialize the Kraken client to interact with the API
            
            # Get the OHLC (Open, High, Low, Close) data from Kraken for the specified currency pair and interval
            response = k.query_public('OHLC', {'pair': self.pair, 'interval': self.divisor})
            if response['error']:  # Check for any errors in the response and raise an exception if any are found
                throw(response['error'])

        # Exception handling block to catch any errors during the process
        except Exception as e:
            print(e)                               # Print the exception error message
            print("Error while generating graph")  # Print a general error message indicating failure to generate the graph

        # If no excepetion occurs, the information is retrieved and stored in a pandas dataframe
        else:
            ohlc_data = response['result'][self.pair]  # Extract the OHLC data from the response
            # Convert the OHLC data into a pandas DataFrame with specified column names
            ohlc_df = pd.DataFrame(ohlc_data, columns=["timestamp", "Open", "High", "Low", "Close", "NaN", "Volume", "MaM"])
            ohlc_df = ohlc_df.drop('NaN',axis=1)
            ohlc_df = ohlc_df.drop('MaM',axis=1)

            # Convert the 'timestamp' column from Unix time (seconds since January 1, 1970) to datetime objects
            ohlc_df["timestamp"] = pd.to_datetime(ohlc_df["timestamp"], unit='s')

            # Set the DataFrame index to the 'timestamp' column for time series analysis
            ohlc_df.index = pd.DatetimeIndex(ohlc_df["timestamp"])

            # Convert all price and volume data to float type for calculations
            ohlc_df["Open"] = ohlc_df["Open"].astype(float)
            ohlc_df["High"] = ohlc_df["High"].astype(float)
            ohlc_df["Low"] = ohlc_df["Low"].astype(float)
            ohlc_df["Close"] = ohlc_df["Close"].astype(float)
            ohlc_df["Volume"] = ohlc_df["Volume"].astype(float)

            window = 14 if ohlc_df.shape[0]>=60 else 3
            ohlc_df['SMA'] = ohlc_df['Close'].rolling(window=window).mean()
            ohlc_df['EMA'] = ohlc_df['Close'].ewm(span=window, adjust=False).mean()


            # Trim the DataFrame to the last 60 data points for visualization
            if self.interval not in intervals:
                ohlc_df = self.aggregate_intervals(ohlc_df)
            return ohlc_df

    @staticmethod  # Create a candlestick chart using Plotly with the OHLC data
    def candlestick(ohlc_df):
        try:
            df = ohlc_df[-60:]
            data = [go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                low=df['Low'], close=df['Close'], name='Candlestick'),
            go.Scatter(x=df.index, y=df['SMA'], name='Simple Mobile Mean'),
            go.Scatter(x=df.index, y=df['EMA'], name='Exponential Mobile Mean')]

            fig = go.Figure(data=data)  # Create a Figure object with the candlestick data
            return fig                  # Return the Figure object for plotting
        except Exception as e:
            print(f"An error occurred while creating the candlestick chart: {e}")
            return go.Figure()

    @staticmethod  # Calculate and graph the stochastic oscillator and its mobile mean 
    def stochastic_mm(df, sma=False, ema=False):
        try:
            window = 14 if df.shape[0]>=60 else 3
            df['SMA'] = df['Close'].rolling(window=window).mean()
            df['L14'] = df['Low'].rolling(window=window).min()
            df['H14'] = df['High'].rolling(window=window).max()
            df['%K'] = (df['Close'] - df['L14']) / (df['H14'] - df['L14']) * 100
            df['%D'] = df['%K'].rolling(window=3).mean()
            df['Buy_Signal'] = ((df['%K'] > df['%D']) & (df['%K'].shift(1) < df['%D'].shift(1))) & (df['%D'] < 20)
            df['Sell_Signal'] = ((df['%K'] < df['%D']) & (df['%K'].shift(1) > df['%D'].shift(1))) & (df['%D'] > 80)
            df = df[-60:]

            data = [# The first plot is a line chart for the '%K' line of the stochastic oscillator
                    go.Scatter(x=df.index, y=df['%K'], name='Stochastic Oscillator'),

                    # The second plot is a line chart for the '%D' line of the stochastic oscillator
                    go.Scatter(x=df.index, y=df['%D'], name='Mobile Mean')]

            # Define the layout for the plotly figure, setting titles and axis labels.
            layout = go.Layout(title='Stochastic Oscillator',
                            xaxis=dict(title='Time'),   # label for the x-axis 
                            yaxis=dict(title='Value', range=[0,100]))  # Label for the y-axis

            fig = go.Figure(data=data, layout=layout)  # create a Figure object with the candlestick data
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
            df = df[-60:]
            if not df['Buy_Signal'].any():  # Check if there are any buy signals
                print("No buy signals found.")
                return None  # Return None if no buy signals
            first_buy_signal = df[df['Buy_Signal']].index[0]  # Get the index of the first buy signal
            df = df.loc[first_buy_signal:]  # Slice the DataFrame from the first buy signal onwards
            data = [go.Scatter(x=df.index, y=df['Profit'].cumsum(), name='Profit'),
                    go.Scatter(x=df[df['Buy_Signal']].index, y=df[df['Buy_Signal']]['Profit'].cumsum(), mode='markers', marker=dict(color='green', size=10), name='Buy Signal'),
                    go.Scatter(x=df[df['Sell_Signal']].index, y=df[df['Sell_Signal']]['Profit'].cumsum(), mode='markers', marker=dict(color='red', size=10), name='Sell Signal')]
            layout = go.Layout(title='Profit',
                        xaxis=dict(title='Time'),   # label for the x-axis 
                        yaxis=dict(title='Value'))  # Label for the y-axis
            fig = go.Figure(data=data, layout=layout)  # create a Figure object with the profit data
            return fig  # return the Figure object for plotting
        except Exception as e:
            print(f"An error occurred while creating the profit chart: {e}")
            return go.Figure()
