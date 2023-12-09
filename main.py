from front import *  # importing everything from the 'front' module

# Execute the main code only if the script is run directly (and not imported as a module elsewhere)
if __name__ == "__main__":
    front = Front()  # instantiating an object 'front' from the class 'Front' (which is defined in the 'front' module)
    front.run()  # running the main process of the 'front' object which starts the streamlit application 



#  timestamp = data[0]  -> unix timestamp of the data entry
#  date_time = datetime.utcfromtimestamp(timestamp)  -> converting the timestamp to a datetime object
#  date = date_time.strftime('%Y-%m-%d')  -> formatting the date in YYYY-MM-DD format
#  time = date_time.strftime('%H:%M:%S')  -> formatting the time in HH:MM:SS format

#  open_price = data[1]  -> the opening price of a financial instrument (e.g., stock, commodity, etc.)
#  high = data[2]  -> the highest price of the instrument in the given period
#  low = data[3]  -> the lowest price of the instrument in the given period
#  close = data[4]  -> the closing price of the instrument
#  volume = data[6]  -> the volume of transactions occurred

#  %K is one of the two lines that make up the stochastic oscillator:
#    %K = (C - L) / (H - L) x 100, where C is the closing price, L is the lowest price, and H is the highest price in the given period