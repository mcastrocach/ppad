import krakenex
from datetime import datetime

# Inicializa el cliente de Kraken
k = krakenex.API()

# Obtiene los datos OHLC
response = k.query_public('OHLC', {'pair': 'XETHZUSD', 'interval': 5})  # intervalo de 60 minutos

if not response['error']:
    ohlc_data = response['result']['XETHZUSD']

    # Imprime los encabezados
    print("Id,Date,Time,Type,Open,High,Low,Last,Volume")

    for data in ohlc_data:
        timestamp = data[0]
        date_time = datetime.utcfromtimestamp(timestamp)
        date = date_time.strftime('%Y-%m-%d')
        time = date_time.strftime('%H:%M:%S')
        open_price = data[1]
        high = data[2]
        low = data[3]
        close = data[4]
        volume = data[6]

        # Kraken no proporciona directamente el "Type" (Buy/Sell) en los datos de OHLC. 
        # También, "Open Interest" no está disponible en los datos públicos de OHLC.
        print(f"{timestamp},{date},{time},N/A,{open_price},{high},{low},{close},{volume},N/A")

else:
    print(response['error'])