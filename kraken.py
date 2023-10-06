import krakenex
from datetime import datetime
import streamlit as st
import pandas as pd

# Initialize the Kraken API client
kraken = krakenex.API()

# Fetch ticker information for ETH/USD
response_ticker = kraken.query_public('Ticker', {'pair': 'XETHZUSD'})

# Check for errors in the ticker response
if response_ticker['error']:
    print("Error:", response_ticker['error'])
else:
    eth_usd_data = response_ticker['result']['XETHZUSD']
    last_trade_price = eth_usd_data['c'][0]
    print(f"Last Trade Price for ETH/USD: ${last_trade_price}")

# Fetch the last 100 trades for ETH/USD
response_trades = kraken.query_public('Trades', {'pair': 'XETHZUSD'})

# Check for errors in the trades response
if response_trades['error']:
    print("Error:", response_trades['error'])
else:
    trades_data = response_trades['result']['XETHZUSD'][:1000]  # Get the last 100 trades
    for trade in trades_data:
        price, volume, time, buy_sell, market_limit, empty, misc = trade
        trade_time = datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Price: ${price}, Volume: {volume}, Time: {trade_time},  Type: {'Buy' if buy_sell == 'b' else 'Sell'}, Market Limit: {market_limit}, Misc: {misc}")

def candlestick_diagram(interval, volumes, times, buy_sells, market_limits, miscs):
    pass       
