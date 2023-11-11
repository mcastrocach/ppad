import krakenex  # import the krakenex library to interact with the Kraken cryptocurrency exchange
from plotly.offline import plot  # import plotly's offline plotting functionality
import plotly.graph_objs as go  # import plotly's graph objects for creating various types of plots
import pandas as pd  # import pandas for data manipulation and analysis
from typing import List, Optional  # import List and Optional from typing for type hinting in function signatures

possible_intervals = (1, 5, 15, 30, 60, 240, 1440, 10080, 21600)

# Function to find the largest divisor of the integer num in a list of divisors
def find_largest_divisor(num: int, divisors: List[int]) -> Optional[int]:
    valid_divisors = [d for d in divisors if num % d == 0]
    if not valid_divisors:
        return None  
    return max(valid_divisors)

# Definition of the class Graph to create candlestick and stochastic oscillator (w/ mobile mean) graphs for trading analysis
class Graph:
    
    # Initializing the class with a default currency pair and time interval
    def __init__(self, pair='XETHZUSD', interval=1440):
        self.pair = pair
        self.interval = interval


    # Retrieving all the useful information from the Kraken API and storing it in a pandas dataframe
    def obtain_data(self):

        # Attempt to perform operations that may fail
        try:
            k = krakenex.API()  # initialize the Kraken client to interact with the API

            # Get the OHLC (Open, High, Low, Close) data from Kraken for the specified currency pair and interval
            response = k.query_public('OHLC', {'pair': self.pair, 'interval': self.interval})
            if response['error']:  # check for any errors in the response and raise an exception if any are found
                throw(response['error'])

        # Exception handling block to catch any errors during the process
        except Exception as e:
            print(e)  # print the exception error message
            print("Error while generating graph")  # print a general error message indicating failure to generate the graph

        # If no excepetion occurs, the information is retrieved and stored in a pandas dataframe
        else:
            ohlc_data = response['result'][self.pair]  # extract the OHLC data from the response
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

            # Trim the DataFrame to the last 60 data points for visualization
            ohlc_df = ohlc_df[-60:]
            return ohlc_df


    @staticmethod
    def aggregate_intervals(df, interval):
        largest_divisor = find_largest_divisor(interval, possible_intervals)
        interval_ratio = interval / largest_divisor

        new_df = pd.DataFrame(df, columns=["timestamp", "Open", "High", "Low", "Close", "Volume"])
        new_df["Open"] = new_df["Open"].rolling(window=interval_ratio).apply(lambda x: x.iloc[0], raw=False)
        new_df["High"] = new_df["High"].rolling(window=interval_ratio).max()
        new_df["Low"] = new_df["Low"].rolling(window=interval_ratio).min()
        new_df["Close"] = new_df["Close"].rolling(window=interval_ratio).apply(lambda x: x.iloc[-1], raw=False)
        new_df["Volume"] = new_df["Volume"].rolling(window=interval_ratio).sum()
        return new_df


    @staticmethod  # Create a candlestick chart using Plotly with the OHLC data
    def candlestick(df):

        data = [go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                               low=df['Low'], close=df['Close'])]
            
        fig = go.Figure(data=data)  # create a Figure object with the candlestick data
        return fig  # return the Figure object for plotting


    @staticmethod  # Calculate and graph the stochastic oscillator and its mobile mean 
    def stochastic_mm(df):

        df['SMA'] = df['Close'].rolling(window=14).mean()
        df['SMA'] = df['Close'].rolling(window=14).mean()
        df['L14'] = df['Low'].rolling(window=14).min()
        df['H14'] = df['High'].rolling(window=14).max()
        df['%K'] = (df['Close'] - df['L14']) / (df['H14'] - df['L14']) * 100
        df['%D'] = df['%K'].rolling(window=3).mean()

        data = [# The first plot is a line chart for the '%K' line of the stochastic oscillator
                go.Scatter(x=df.index, y=df['%K'], name='%K'),  

                # The second plot is a line chart for the '%D' line of the stochastic oscillator
                go.Scatter(x=df.index, y=df['%D'], name='%D')]

        # Define the layout for the plotly figure, setting titles and axis labels.
        layout = go.Layout(title='Stochastic Oscillator',  
                           xaxis=dict(title='Time'),   # label for the x-axis 
                           yaxis=dict(title='Value'))  # Label for the y-axis
            
        fig = go.Figure(data=data, layout=layout)  # create a Figure object with the candlestick data
        return fig  # return the Figure object for plotting