# Importing specific classes from local modules to generate the graphs for the stochastic oscillator and its mobile mean
from graphs.Stochastic import Stochastic
from graphs.MobileMeanStochastic import MobileMeanStochastic

import streamlit as st  # importing streamlit for web app functionality
from streamlit_option_menu import option_menu  # importing a helper for creating option menus in streamlit
import plotly.graph_objects as go  # importing Plotly for advanced graphing capabilities
from plotly.subplots import make_subplots


import requests  # using requests library to make HTTP requests

# Function to retrieve all available currency pairs from the Kraken API
def get_kraken_pairs():
    url = 'https://api.kraken.com/0/public/AssetPairs'  # API endpoint for Kraken currency pairs
    response = requests.get(url)   # making a GET request to the API
    response_json = response.json()  # parsing the JSON response
    pairs = response_json['result'].keys()  # extracting the currency pairs
    return tuple(pairs)  # returning the currency pairs as a tuple

# Retrieve and store the available Kraken currency pairs
kraken_pairs = get_kraken_pairs()


# Definition of the Front class for handling the front-end part of the application
class Front:

    # Method to initialize all objects from the Front class
    def __init__(self):
        st.title("Kraken graphs")  # set the title of the Streamlit app

        # Initialize default values for currency pair, interval, and selected graph
        c1 = "XETHZUSD"
        c2 = "21600"
        select_graph = "Stochastic"

    # Method to run the main functionality of the Streamlit app
    def run(self):
        st.write('Please select a currency pair')  # prompt user to select a currency pair
        self.select_boxes()   # call method defined below to display selection boxes
        self.display_graph()  # call method defined below to display the selected graph


    # Method to create selection boxes for user input
    def select_boxes(self):

        # Dropdown to select currency pair
        self.c1 = st.selectbox(
           "Please select currency pair",
           kraken_pairs,
           index=None,
           placeholder="Select currency pair...",
        )

        # Dropdown to select time interval for graphing
        self.c2 = st.select_slider(
            "Please select interval",
            ["1", "5", "15", "30", "60", "240", "1440", "10080", "21600"],
        )

        # Horizontal option menu for selecting the graph type.
        self.graph_select = option_menu(None, ["Stochastic", "MobileMean", "Merge them", "Nada"],
                                        icons=['house', 'cloud-upload', "list-task", 'gear'],  # TODO: Icons?
                                        menu_icon="cast", default_index=0, orientation="horizontal")


    # Method to handle graph generation and display
    def display_graph(self):

        # Button to trigger graph plotting based on user selection
        if st.button('Plot it!'):

            if self.graph_select == "Stochastic":  # stochastic oscillator
                fig = Stochastic(pair=self.c1, interval=self.c2).generate_graph()

            elif self.graph_select == "MobileMean":  # mobile mean of the stochastic oscillator
                fig = MobileMeanStochastic(pair=self.c1, interval=self.c2).generate_graph()

            elif self.graph_select == "Merge them":  # a combination of the two previous options
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.8, 0.2])
                fig.add_trace(Stochastic(pair=self.c1, interval=self.c2).generate_graph()['data'][0], row=1, col=1)
                fig.add_trace(MobileMeanStochastic(pair=self.c1, interval=self.c2).generate_graph()['data'][0], row=2, col=1)
                fig.add_trace(MobileMeanStochastic(pair=self.c1, interval=self.c2).generate_graph()['data'][1], row=2, col=1)
                fig.update_layout(
                    title='Candlestick and Stochastic Oscillator',
                    yaxis_title='Price',
                    xaxis2_title='Time',
                    yaxis2_title='%K - %D',
                    xaxis_rangeslider_visible=False
                )

            fig_dict = fig.to_dict()  # convert the figure to a dictionary for Streamlit to display
            st.plotly_chart(fig_dict)  # use Streamlit to display the Plotly graph


# Execute the main code only if the script is run directly (and not imported as a module elsewhere)
if __name__ == "__main__":
    front = Front()  # instantiating an object 'front' from the class 'Front' (which is defined in the 'front' module)
    front.run()  # running the main process of the 'front' object which starts the streamlit application
