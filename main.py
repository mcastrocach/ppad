import krakenex
from datetime import datetime
import pandas as pd
import mplfinance as fplt
import matplotlib.pyplot as plt
import streamlit as st

from Stochastic import generate_graph

st.title('Kraken API')
st.write('Please select a currency pair')

#dropdown to select currency pair
c1 = st.selectbox(
   "Please select currency pair",
   ("XETHZUSD", "XXBTZUSD", "XLTCZUSD", "XETHXXBT", "XLTCXXBT", "XLTCZUSD", "XETHZUSD", "XXBTZUSD", "XXMRZUSD", "XXMRXXBT", "XXMRZEUR", "XXMRXBT", "XXMRXXBT", "XXMRZEUR", "XXMRZUSD", "XXRPZUSD", "XXRPXXBT", "XXRPZUSD", "XXRPXXBT", "XXRPZEUR", "XXRPZUSD", "XZECZUSD", "XZECXXBT", "XZECZEUR", "XZECZUSD", "XZECXXBT", "XZECZEUR", "XZECZUSD", "XETCZUSD", "XETCXXBT", "XETCZEUR", "XETCZUSD", "XETCXXBT", "XETCZEUR", "XETCZUSD", "XETHZUSD", "XETHXXBT", "XETHZEUR", "XETHZUSD", "XETHXXBT", "XETHZEUR", "XETHZUSD", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD", "XLTCZUSD", "XLTCXXBT", "XLTCZEUR", "XLTCZUSD", "XLTCXXBT", "XLTCZEUR", "XLTCZUSD", "XETHZUSD", "XETHXXBT", "XETHZEUR", "XETHZUSD", "XETHXXBT", "XETHZEUR", "XETHZUSD", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD"),
   index=None,
   placeholder="Select currency pair...",
)

#dropdown to select interval
c2 = st.selectbox(
    "Please select interval",
    ("1", "5", "15", "30", "60", "240", "1440", "10080", "21600"),
    index=None,
    placeholder="Select interval...",
)

#button to generate graph
if st.button('Plot it!'):
    fig = generate_graph(pair=c1, interval=c2)
    st.pyplot(fig)


# Las variables son:
#     timestamp = data[0]
#     date_time = datetime.utcfromtimestamp(timestamp)
#     date = date_time.strftime('%Y-%m-%d')
#     time = date_time.strftime('%H:%M:%S')
#     open_price = data[1]
#     high = data[2]
#     low = data[3]
#     close = data[4]
#     volume = data[6]
# Fórmula del oscilador estocástico, %K = (U - Mi) / (Max - Mi) x 100  (U - cierre, Mi - mínimo, Max - máximo)
