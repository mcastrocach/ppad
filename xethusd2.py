import krakenex
from datetime import datetime
import pandas as pd
import mplfinance as fplt
import matplotlib.pyplot as plt

def compute_rsi(data, window):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

# Inicializa el cliente de Kraken
k = krakenex.API()

# Obtiene los datos OHLC
response = k.query_public('OHLC', {'pair': 'XETHZUSD', 'interval': 1})  

if not response['error']:
    ohlc_data = response['result']['XETHZUSD']
    print(ohlc_data[0])
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

    ohlc_df["High_biweek"] = ohlc_df["High"].rolling(window=14,center=False).max()
    ohlc_df["Low_biweek"] = ohlc_df["Low"].rolling(window=14,center=False).min()

    ohlc_df = ohlc_df[:100]

    ohlc_df["Stochastic"] = (ohlc_df["Close"]-ohlc_df["Low_biweek"])/(ohlc_df["High_biweek"]-ohlc_df["Low_biweek"])*100
    ohlc_df["Smoothed"] = ohlc_df["Stochastic"].rolling(window=5, center=True).mean()
    ohlc_df["Smooothed"] = ohlc_df["Stochastic"].rolling(window=5, center=True).mean()

    ohlc_df["SMA"] = ohlc_df['Close'].rolling(window=14).mean()
    ohlc_df["RSI"] = compute_rsi(ohlc_df, window=14)
    ohlc_df["EMA"] = ohlc_df['Close'].ewm(span=14, adjust=False).mean()

    # indicators = fplt.make_addplot(ohlc_df[["SMA","RSI","EMA"]])
    sma = fplt.make_addplot(ohlc_df["SMA"], color="orange", width=1.5)
    ema = fplt.make_addplot(ohlc_df["EMA"], color="dodgerblue", width=1.5)
    rsi = fplt.make_addplot(ohlc_df["RSI"], color="grey", width=1.5, ylabel="RSI",
                        secondary_y=True, linestyle='dashdot')

    fplt.plot(
            ohlc_df,
            type='candle',
            addplot = [sma,ema,rsi],
            title='Title',
            ylabel='Price ($)'
        )        

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
