import krakenex                   # Import krakenex to interact with the Kraken cryptocurrency exchange API
import plotly.graph_objs as go    # Import Plotly's graph objects for advanced data visualization
import pandas as pd               # Import Pandas for data analysis and manipulation
import numpy as np                # Import NumPy for numerical operations and array processing
import time                       # Import time for time.mktime
import datetime

from plotly.subplots import make_subplots

# The class Graph is designed for constructing candlestick and stochastic oscillator graphs with mobile mean for trading analysis
class Graph:

    # Constructor for initializing a Graph instance with a currency pair, interval, and divisor
    def __init__(self, pair='XETHZUSD', interval=1440, divisor=1, since= int((time.mktime(datetime.datetime.now().timetuple())))):
        self.pair = pair          # The currency pair to be analyzed
        self.interval = interval  # Time interval for each data point in minutes
        self.divisor = divisor    # Divisor for interval adjustment
        self.since = since

    # This function aggregates data into custom time intervals that are not natively provided by the API
    def aggregate_intervals(self, df):
        # Resamples the DataFrame to the specified interval and aggregates key metrics
        print(df)
        resampled_df = df.resample(f'{self.interval}T').agg({ 'Open': 'first', 
                                                              'High': 'max', 
                                                              'Low': 'min', 
                                                              'Close': 'last', 
                                                              'SMA': 'first', 
                                                              'EMA': 'first', 
                                                              'Volume': 'sum'})
        print(resampled_df)
        return resampled_df


    # Retrieves trading data from the Kraken API and organizes it into a Pandas DataFrame
    def obtain_data(self):
        
        # Initializing a Kraken API client and querying data within a try-except block
        try:
            k = krakenex.API()  # Initialize the Kraken client
            
            # Query for OHLC data for the specified currency pair and interval
            response = k.query_public('OHLC', {'pair':self.pair, 'interval':self.divisor, 'since':self.since})
            if response['error']:  # Check and raise an exception if errors exist in the response
                print(f"There was an error with the API call")
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
            ohlc_df["timestamp"] = pd.to_datetime(ohlc_df["timestamp"], unit='s')    # Unix timestamp to Python datetime
            ohlc_df.set_index(pd.DatetimeIndex(ohlc_df["timestamp"]), inplace=True)

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
            if self.interval not in (1, 5, 15, 30, 60, 240, 1440, 10080, 21600):
                ohlc_df = self.aggregate_intervals(ohlc_df)
            return ohlc_df  # Return the prepared DataFrame


    @staticmethod  # Static method to create a candlestick chart from OHLC data using Plotly
    def candlestick(ohlc_df):
        try:
            # Use the last 60 data points from the OHLC DataFrame for the chart
            #df = ohlc_df[-60:]
            df = ohlc_df[14:]

            colors = ['#008080' if close >= open else 'red' for open, close in zip(df['Open'], df['Close'])]
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            # include candlestick with rangeselector
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Candlestick Data'), secondary_y=True)
            fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=colors, opacity=0.25, showlegend=False), secondary_y=False)
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA'], marker=dict(color='#0000FF'), opacity=0.35, name='Simple Moving Average'), secondary_y=True)
            fig.add_trace(go.Scatter(x=df.index, y=df['EMA'], marker=dict(color='#FF0000'), opacity=0.35, name='Exponential Moving Average'), secondary_y=True)
            fig.layout.yaxis2.showgrid=False
            fig.layout.title = 'Candlestick Graph with Moving Average'
            fig.layout.height = 450

            """
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.03, 
                    subplot_titles=('OHLC', 'Volume'), 
                    row_width=[0.2, 0.7])

            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']), row=1, col=1)
            fig.add_trace(go.Bar(x=df.index, y=df['Volume']), row=2, col=1)
            fig.update_layout(title='Stock Price with Volume', 
                  xaxis_tickfont_size=12, 
                  yaxis=dict(title='Stock Price'),
                  yaxis2=dict(title='Volume', overlaying='y', side='right'))
            """


            """
            # Define the candlestick chart components and moving averages
            data = [ go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                   low=df['Low'], close=df['Close'], name='Candlestick Data'),

                     go.Scatter(x=df.index, y=df['SMA'], name='Simple Moving Average'),
                     go.Scatter(x=df.index, y=df['EMA'], name='Exponential Moving Average') ]

            # Define the layout for the plotly figure, setting titles and axis labels.
            layout = go.Layout(title='Candlestick Graph with Moving Average',
                               yaxis=dict(title='Price'))  # Label for the y-axis

            fig = go.Figure(data=data, layout=layout)  # create a Figure object with the OHLC data
            """
            
            return fig  # return the Figure object for plotting
        
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

            data = [# The first plot is a line chart for the '%K' line of the stochastic oscillator
                    go.Scatter(x=df.index, y=df['%K'], name='Stochastic Oscillator', marker=dict(color='#1E90FF')),

                    # The second plot is a line chart for the '%D' line of the stochastic oscillator
                    go.Scatter(x=df.index, y=df['%D'], name='Smoothed Stochastic Oscillator', marker=dict(color='#FFA500'))]

            # Define the layout for the plotly figure, setting titles and axis labels.
            layout = go.Layout(title='Stochastic Oscillator with its Smoothed Version',
                               yaxis=dict(title='Value (%)', range=[0,100]))  # Label for the y-axis

            fig = go.Figure(data=data, layout=layout)  # create a Figure object with the candlestick data
            current_height = fig.layout.height if fig.layout.height is not None else 450
            fig.layout.height = height=current_height/2
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