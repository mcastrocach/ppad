from front import *

if __name__ == "__main__":
    front = Front()
    front.run()
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
# Fórmula del oscilador estocástico: %K = (U - Mi) / (Max - Mi) x 100, donde U es cierre, Mi es mínimo y Max es máximo
