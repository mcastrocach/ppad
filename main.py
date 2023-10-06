import krakenex
from datetime import datetime
import pandas as pd
import mplfinance as fplt
import matplotlib.pyplot as plt
import streamlit as st

st.title('Kraken API')
st.write('Please select a currency pair')

#dropdown to select currency pair
c1 = st.selectbox(
   "Please select currency one",
   ("BTC", "USD", "EUR"),
   index=None,
   placeholder="Select currency 1...",
)
c2 = st.selectbox(
   "Please select currency two",
   ("BTC", "USD", "EUR"),
   index=None,
   placeholder="Select currency 2...",
)
#check if they are the same
if c1 == c2:
    st.write('Please select different currencies')
#button that prints the currency pair
else:
    if st.button('Submit'):
        st.write('You selected:', c1, c2)

# Inicializa el cliente de Kraken
k = krakenex.API()

# Obtiene los datos OHLC
response = k.query_public('OHLC', {'pair': 'XETHZUSD', 'interval': 1440})
#weekly = k.query_public('OHLC', {'pair': 'XETHZUSD', 'interval': 20160})  
# print(weekly['result'])

if not response['error']:
    ohlc_data = response['result']['XETHZUSD']
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

    # weekly_data = weekly['result']['XETHZUSD']
    # weekly_df = pd.DataFrame(weekly_data,columns=["timestamp","Open","High","Low","Close","NaN","Volume","MaM"])
    # weekly_df["timestamp"] = list(map(datetime.utcfromtimestamp, weekly_df["timestamp"]))
    # weekly_df = weekly_df.drop('NaN',axis=1)
    # weekly_df = weekly_df.drop('MaM',axis=1)

    # weekly_df.index = pd.DatetimeIndex(weekly_df["timestamp"])
    # weekly_df["Open"] = weekly_df["Open"].astype(float)
    # weekly_df["High"] = weekly_df["High"].astype(float)
    # weekly_df["Low"] = weekly_df["Low"].astype(float)
    # weekly_df["Close"] = weekly_df["Close"].astype(float)
    # weekly_df["Volume"] = weekly_df["Volume"].astype(float)

    ohlc_df["Stochastic"] = (ohlc_df["Close"]-ohlc_df["Low"])/(ohlc_df["High"]-ohlc_df["Low"])*100
    #ohlc_df["Smoothed"] = ohlc_df["Stochastic"].rolling(window=3, center=True).mean()
    #ohlc_df["Smooothed"] = ohlc_df["Stochastic"].rolling(window=3, center=True).mean()

    # stochastic = fplt.make_addplot(ohlc_df[["Smooothed"]])
    stochastic = fplt.make_addplot(ohlc_df[["Stochastic"]])
    fig, ax = fplt.plot(
            ohlc_df,
            type='candle',
            addplot = stochastic,
            title='Title',
            ylabel='Price ($)',
            returnfig=True
        )
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

else:
    print(response['error'])
# Fórmula del oscilador estocástico, %K = (U - Mi) / (Max - Mi) x 100  (U - cierre, Mi - mínimo, Max - máximo)
