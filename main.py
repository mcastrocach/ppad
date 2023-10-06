import krakenex
from datetime import datetime
import pandas as pd
import mplfinance as fplt
import matplotlib.pyplot as plt
import streamlit as st

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

st.title('Kraken API')
st.write('Please select a currency pair')

#dropdown to select currency pair
c1 = st.selectbox(
   "Please select currency pair",
   ("XETHZUSD", "XXBTZUSD", "XLTCZUSD", "XETHXXBT", "XLTCXXBT", "XLTCZUSD", "XETHZUSD", "XXBTZUSD", "XXMRZUSD", "XXMRXXBT", "XXMRZEUR", "XXMRXBT", "XXMRXXBT", "XXMRZEUR", "XXMRZUSD", "XXRPZUSD", "XXRPXXBT", "XXRPZUSD", "XXRPXXBT", "XXRPZEUR", "XXRPZUSD", "XZECZUSD", "XZECXXBT", "XZECZEUR", "XZECZUSD", "XZECXXBT", "XZECZEUR", "XZECZUSD", "XETCZUSD", "XETCXXBT", "XETCZEUR", "XETCZUSD", "XETCXXBT", "XETCZEUR", "XETCZUSD", "XETHZUSD", "XETHXXBT", "XETHZEUR", "XETHZUSD", "XETHXXBT", "XETHZEUR", "XETHZUSD", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD", "XLTCZUSD", "XLTCXXBT", "XLTCZEUR", "XLTCZUSD", "XLTCXXBT", "XLTCZEUR", "XLTCZUSD", "XETHZUSD", "XETHXXBT", "XETHZEUR", "XETHZUSD", "XETHXXBT", "XETHZEUR", "XETHZUSD", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD"),
   index=None,
   placeholder="Select currency pair...",
)

#button to generate graph
if st.button('Plot it!'):
    fig = generate_graph(plot= c1)
    st.pyplot(fig)


"""
Las variables son:
    timestamp = data[0]
    date_time = datetime.utcfromtimestamp(timestamp)
    date = date_time.strftime('%Y-%m-%d')
    time = date_time.strftime('%H:%M:%S')
    open_price = data[1]
    high = data[2]
    low = data[3]
    close = data[4]
    volume = data[6]
"""
# Fórmula del oscilador estocástico, %K = (U - Mi) / (Max - Mi) x 100  (U - cierre, Mi - mínimo, Max - máximo)
