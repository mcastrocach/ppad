import krakenex  # import the krakenex library to interact with the Kraken cryptocurrency exchange
from datetime import datetime  # import datetime for handling date and time objects
from plotly.offline import plot  # import plotly's offline plotting functionality
import plotly.graph_objs as go  # import plotly's graph objects for creating various types of plots
import pandas as pd  # import pandas for data manipulation and analysis


# Definition of the class Stochastic to create stochastic oscillator graphs for trading analysis
class Stochastic:

    # Initializing the class with a default currency pair and time interval
    def __init__(self, pair='XETHZUSD', interval=1440):
        self.pair = pair
        self.interval = interval

    def generate_graph(self):

        # Attempt to perform operations that may fail
        try:
            k = krakenex.API()  # initialize the Kraken client to interact with the API

            # Get the OHLC (Open, High, Low, Close) data from Kraken for the specified currency pair and interval
            response = k.query_public('OHLC', {'pair': self.pair, 'interval': self.interval})
            if response['error']:  # check for any errors in the response and raise an exception if any are found
                throw(response['error'])

            ohlc_data = response['result'][self.pair]  # extract the OHLC data from the response
            # Convert the OHLC data into a pandas DataFrame with specified column names
            ohlc_df = pd.DataFrame(ohlc_data, columns=["timestamp", "Open", "High", "Low", "Close", "NaN", "Volume", "MaM"])
            
            # Convert the timestamp to a datetime object
            ohlc_df["timestamp"] = list(map(datetime.utcfromtimestamp, ohlc_df["timestamp"].astype(int)))

            # Drop the unnecessary 'NaN' and 'MaM' columns from the DataFrame
            ohlc_df = ohlc_df.drop('NaN', axis=1)
            ohlc_df = ohlc_df.drop('MaM', axis=1)

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

            # Create a candlestick chart using Plotly with the OHLC data
            data = [go.Candlestick(x=ohlc_df.index, open=ohlc_df['Open'], high=ohlc_df['High'],
                                   low=ohlc_df['Low'], close=ohlc_df['Close'])]
            
            fig = go.Figure(data=data)  # create a Figure object with the candlestick data
            return fig  # return the Figure object for plotting


        # Exception handling block to catch any errors during the process
        except Exception as e:
            print(e)  # print the exception error message
            print("Error while generating graph")  # print a general error message indicating failure to generate the graph
