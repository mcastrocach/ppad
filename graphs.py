import krakenex                   # Import krakenex to interact with the Kraken cryptocurrency exchange API
import plotly.graph_objs as go    # Import Plotly's graph objects for advanced data visualization
import pandas as pd               # Import Pandas for data analysis and manipulation
import numpy as np                # Import NumPy for numerical operations and array processing
import time                       # Import time for time.mktime
import datetime



# The class Graph is designed for constructing candlestick and stochastic oscillator graphs with mobile mean for trading analysis
class Graph:

    # Constructor for initializing a Graph instance with a currency pair, interval, and divisor
    def __init__(self, pair='XETHZUSD', interval=1440, divisor=1):
        self.pair = pair          # The currency pair to be analyzed
        self.interval = interval  # Time interval for each data point in minutes
        self.divisor = divisor    # Divisor for interval adjustment
        self.since = int(time.mktime(datetime.datetime.now().timetuple()))

    # This function aggregates data into custom time intervals that are not natively provided by the API
    def aggregate_intervals(self, df):
        # Resamples the DataFrame to the specified interval and aggregates key metrics
        resampled_df = df.resample(f'{self.interval}T').agg({ 'Open': 'first', 
                                                              'High': 'max', 
                                                              'Low': 'min', 
                                                              'Close': 'last', 
                                                              'Volume': 'sum'})
        return resampled_df


    # Retrieves trading data from the Kraken API and organizes it into a Pandas DataFrame
    def obtain_data(self):
        
        # Initializing a Kraken API client and querying data within a try-except block
        try:
            k = krakenex.API()  # Initialize the Kraken client
            
            # Query for OHLC data for the specified currency pair and interval
            response = k.query_public('OHLC', {'pair': self.pair, 'interval': self.divisor,'since':self.since})
            if response['error']:  # Check and raise an exception if errors exist in the response
                raise Exception(response['error'])

        # Catch and print any exceptions during the data retrieval process
        except Exception as e:
            print(f"An error occurred: {e}")       # Print the specific error message
            print("Error while generating graph")  # Indicate a graph generation error

        # Process the retrieved data if no exceptions occur
        else:
            ohlc_data = response['result'][self.pair]  # Extract OHLC data from API response

            # Convert OHLC data to a DataFrame and remove unnecessary columns
            ohlc_df = pd.DataFrame(ohlc_data, columns=["timestamp", "Open", "High", "Low", "Close", "NaN", "Volume", "MaM"]).drop(['NaN', 'MaM'], axis=1)

            # Convert timestamps to datetime format and set as DataFrame index
            ohlc_df["timestamp"] = pd.to_datetime(ohlc_df["timestamp"], unit='s')
            ohlc_df.set_index(pd.DatetimeIndex(ohlc_df["timestamp"]), inplace=True)

            # Convert all price and volume data to float type for calculations
            ohlc_df["Open"] = ohlc_df["Open"].astype(float)
            ohlc_df["High"] = ohlc_df["High"].astype(float)
            ohlc_df["Low"] = ohlc_df["Low"].astype(float)
            ohlc_df["Close"] = ohlc_df["Close"].astype(float)
            ohlc_df["Volume"] = ohlc_df["Volume"].astype(float)

            # Add Simple Moving Average (SMA) and Exponential Moving Average (EMA) to the DataFrame
            window = 14 if ohlc_df.shape[0] >= 60 else 3  # Determine window size based on data points
            ohlc_df['SMA'] = ohlc_df['Close'].rolling(window=window).mean()
            ohlc_df['EMA'] = ohlc_df['Close'].ewm(span=window, adjust=False).mean()

            # Aggregate data into custom intervals if needed
            if self.interval not in (1, 5, 15, 30, 60, 240, 1440, 10080, 21600):
                ohlc_df = self.aggregate_intervals(ohlc_df)
            return ohlc_df  # Return the prepared DataFrame


    @staticmethod  # Static method to create a candlestick chart from OHLC data using Plotly
    def candlestick(ohlc_df):
        try:
            # Use the last 60 data points from the OHLC DataFrame for the chart
            df = ohlc_df[-60:]

            # Define the candlestick chart components and moving averages
            data = [
                    go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                   low=df['Low'], close=df['Close'], name='Candlestick'),

                    go.Scatter(x=df.index, y=df['SMA'], name='Simple Moving Average'),
                    go.Scatter(x=df.index, y=df['EMA'], name='Exponential Moving Average')]

            fig = go.Figure(data=data)  # Instantiate a Plotly Figure object with the defined data
            return fig                  # Return the Figure object for visualization
        
        except Exception as e:
            # Handle exceptions in chart creation and return an empty figure in case of an error
            print(f"An error occurred while creating the candlestick chart: {e}")
            return go.Figure()  # Return an empty Plotly Figure object if an error occurs


    @staticmethod  # Calculate and graph the stochastic oscillator and its mobile mean 
    def stochastic_mm(df):
        try:
            window = 14 if df.shape[0]>=60 else 3
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
