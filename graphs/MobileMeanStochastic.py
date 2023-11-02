import krakenex
from datetime import datetime
from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd

class MobileMeanStochastic:
    def __init__(self, pair='XETHZUSD', interval=1440):
        self.pair = pair
        self.interval = interval

    def generate_graph(self):
        try:
            # Initialize the Kraken client
            k = krakenex.API()
            # Get the OHLC data
            response = k.query_public('OHLC', {'pair': self.pair, 'interval': self.interval})

            if response['error']:
                throw(response['error'])

            ohlc_data = response['result'][self.pair]
            ohlc_df = pd.DataFrame(ohlc_data, columns=["timestamp", "Open", "High", "Low", "Close", "NaN", "Volume", "MaM"])
            #ohlc_df["timestamp"] = list(map(datetime.utcfromtimestamp, ohlc_df["timestamp"].astype(int)))
            ohlc_df["timestamp"] = pd.to_datetime(ohlc_df["timestamp"], unit='s')

            ohlc_df.index = pd.DatetimeIndex(ohlc_df["timestamp"])
            ohlc_df["Open"] = ohlc_df["Open"].astype(float)
            ohlc_df["High"] = ohlc_df["High"].astype(float)
            ohlc_df["Low"] = ohlc_df["Low"].astype(float)
            ohlc_df["Close"] = ohlc_df["Close"].astype(float)
            ohlc_df["Volume"] = ohlc_df["Volume"].astype(float)

            # Calculate the stochastic oscillator
            ohlc_df['SMA'] = ohlc_df['Close'].rolling(window=14).mean()
            ohlc_df['SMA'] = ohlc_df['Close'].rolling(window=14).mean()
            ohlc_df['L14'] = ohlc_df['Low'].rolling(window=14).min()
            ohlc_df['H14'] = ohlc_df['High'].rolling(window=14).max()
            ohlc_df['%K'] = (ohlc_df['Close'] - ohlc_df['L14']) / (ohlc_df['H14'] - ohlc_df['L14']) * 100
            ohlc_df['%D'] = ohlc_df['%K'].rolling(window=3).mean()

            # Select the last 60 data points for plotting
            ohlc_df = ohlc_df[-60:]

            data = [
                go.Scatter(x=ohlc_df.index, y=ohlc_df['%K'], name='%K'),
                go.Scatter(x=ohlc_df.index, y=ohlc_df['%D'], name='%D')
            ]
            layout = go.Layout(title='Stochastic Oscillator',
                               xaxis=dict(title='Time'),
                               yaxis=dict(title='Value'))
            fig = go.Figure(data=data, layout=layout)
            return fig
        except Exception as e:
            #print traceback
            print(e)
            return None
