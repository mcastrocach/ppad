import krakenex
from datetime import datetime
from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd

class Stochastic:
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
            ohlc_df["timestamp"] = list(map(datetime.utcfromtimestamp, ohlc_df["timestamp"].astype(int)))
            ohlc_df = ohlc_df.drop('NaN',axis=1)
            ohlc_df = ohlc_df.drop('MaM',axis=1)

            ohlc_df.index = pd.DatetimeIndex(ohlc_df["timestamp"])
            ohlc_df["Open"] = ohlc_df["Open"].astype(float)
            ohlc_df["High"] = ohlc_df["High"].astype(float)
            ohlc_df["Low"] = ohlc_df["Low"].astype(float)
            ohlc_df["Close"] = ohlc_df["Close"].astype(float)
            ohlc_df["Volume"] = ohlc_df["Volume"].astype(float)

            ohlc_df = ohlc_df[-60:]

            data = [go.Candlestick(x=ohlc_df.index,
                                   open=ohlc_df['Open'],
                                   high=ohlc_df['High'],
                                   low=ohlc_df['Low'],
                                   close=ohlc_df['Close'])]
            fig = go.Figure(data=data)
            return fig

        except Exception as e:
            print(e)
            print("Error while generating graph")
