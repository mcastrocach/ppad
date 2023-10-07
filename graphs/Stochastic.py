import krakenex
import mplfinance as fplt
import matplotlib.pyplot as plt

def generate_graph(pair='XETHZUSD', interval=1440):
    try:
        # Inicializa el cliente de Kraken
        k = krakenex.API()
        # Obtiene los datos OHLC
        response = k.query_public('OHLC', {'pair': pair, 'interval': interval})

        if response['error']:
            throw(response['error'])

        ohlc_data = response['result'][pair]
        ohlc_df = pd.DataFrame(ohlc_data,columns=["timestamp","Open","High","Low","Close","NaN","Volume","MaM"])
        ohlc_df["timestamp"] = list(map(datetime.utcfromtimestamp, ohlc_df["timestamp"]))
        ohlc_df = ohlc_df.drop('NaN',axis=1)
        ohlc_df = ohlc_df.drop('MaM',axis=1)

        ohlc_df.index = pd.DatetimeIndex(ohlc_df["timestamp"])
        ohlc_df["Open"] = ohlc_df["Open"].astype(float)
        ohlc_df["High"] = ohlc_df["High"].astype(float)
        ohlc_df["Low"] = ohlc_df["Low"].astype(float)
        ohlc_df["Close"] = ohlc_df["Close"].astype(float)
        ohlc_df["Volume"] = ohlc_df["Volume"].astype(float)

        ohlc_df = ohlc_df[-60:]
        ohlc_df["Stochastic"] = (ohlc_df["Close"]-ohlc_df["Low"])/(ohlc_df["High"]-ohlc_df["Low"])*100

        stochastic = fplt.make_addplot(ohlc_df[["Stochastic"]])
        fig, ax = fplt.plot(
                ohlc_df,
                type='candle',
                addplot = stochastic,
                title='Title',
                ylabel='Price ($)',
                returnfig=True
            )
        return fig

    except Exception:
        st.write('Error: ', Exception)
