import krakenex  # import the krakenex library to interact with the Kraken cryptocurrency exchange
from datetime import datetime  # import datetime for handling date and time objects
from plotly.offline import plot  # import plotly's offline plotting functionality
import plotly.graph_objs as go  # import plotly's graph objects for creating various types of plots
import pandas as pd  # import pandas for data manipulation and analysis


# Definition of the class MobileMeanStochastic to create stochastic oscillator's mobile mean graphs for trading analysis
class MobileMeanStochastic:

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

            # Calculate the stochastic oscillator and its mobile mean
            ohlc_df['SMA'] = ohlc_df['Close'].rolling(window=14).mean()
            ohlc_df['SMA'] = ohlc_df['Close'].rolling(window=14).mean()
            ohlc_df['L14'] = ohlc_df['Low'].rolling(window=14).min()
            ohlc_df['H14'] = ohlc_df['High'].rolling(window=14).max()
            ohlc_df['%K'] = (ohlc_df['Close'] - ohlc_df['L14']) / (ohlc_df['H14'] - ohlc_df['L14']) * 100
            ohlc_df['%D'] = ohlc_df['%K'].rolling(window=3).mean()

            # Select the last 60 data points for plotting
            ohlc_df = ohlc_df[-60:]

            data = [# The first plot is a line chart for the '%K' line of the stochastic oscillator
                    go.Scatter(x=ohlc_df.index, y=ohlc_df['%K'], name='%K'),  

                    # The second plot is a line chart for the '%D' line of the stochastic oscillator
                    go.Scatter(x=ohlc_df.index, y=ohlc_df['%D'], name='%D')]

            # Define the layout for the plotly figure, setting titles and axis labels
            layout = go.Layout(title='Stochastic Oscillator',  
                                xaxis=dict(title='Time'),  # label for the x-axis 
                                yaxis=dict(title='Value'))  # Label for the y-axis
            
            fig = go.Figure(data=data, layout=layout)  # create a Figure object with the candlestick data
            return fig  # return the Figure object for plotting
        
        # Exception handling block to catch any errors during the process
        except Exception as e:
            print(e)  # print the exception error message
            print("Error while generating graph")  # print a general error message indicating failure to generate the graph
