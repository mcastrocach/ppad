from graphs import Graph
import streamlit as st  # importing streamlit for web app functionality
from streamlit_option_menu import option_menu  # importing a helper for creating option menus in streamlit
from plotly.subplots import make_subplots


import requests  # importing requests library to make HTTP requests

# Function to retrieve all available currency pairs from the Kraken API
def get_kraken_pairs():
    url = 'https://api.kraken.com/0/public/AssetPairs'  # API endpoint for Kraken currency pairs
    response = requests.get(url)                        # Making a GET request to the API
    response_json = response.json()                     # Parsing the JSON response
    pairs = response_json['result'].keys()              # Extraction of the currency pairs
    return tuple(pairs)                                 # Returning the currency pairs as a tuple

kraken_pairs = get_kraken_pairs()  # Retrieve and store the available Kraken currency pairs


intervals = {"1m":1, "5m":5, "15m":15, "30m":30, "1h":60, "4h":240, "1d":1440, "1w":10080, "2w":21600, "Other":-1}
keys, options = intervals.keys(), intervals.values()

def find_largest_divisor(n):
    valid_divisors = [d for d in options if n % d == 0]
    if not valid_divisors:
        return None  
    return max(valid_divisors)


# Definition of the Front class for handling the front-end part of the application
class Front:

    # Method to initialize all objects from the Front class
    def __init__(self):
        st.title("Kraken Currency Analysis Tool")  # Set the title of the Streamlit app
        st.markdown("Authors: Rodrigo de la Nuez Moraleda, Marcos Castro Cacho")
        st.markdown("<hr>", unsafe_allow_html=True)

        # Initialize default values for currency pair and interval
        self.c1 = None
        st.session_state.selected_option = st.session_state.get("selected_option")
        self.c2 = st.session_state.selected_option


    # Method to create selection boxes for user input
    def select_boxes(self):

        # Dropdown to select currency pair
        self.c1 = st.selectbox(
           "Select a currency pair from the available options",
           kraken_pairs,
           index=None,
           placeholder="xxxxxxx",
        )

        st.markdown("<hr>", unsafe_allow_html=True)

        # Dynamic CSS to highlight the selected button
        selected_option_key = f"button-{st.session_state.selected_option}" if st.session_state.selected_option else ""
        st.markdown("We have selected some of the most used time windows, pick one from the following..." + 
            f"""
            <style>
            div.stButton > button {{
                width: 100%;
            }}
            div.stButton > button#{selected_option_key} {{
                background-color: #0d6efd;
                color: white;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        # Creating a row of columns with the options
        columns = st.columns(len(keys))
        for i, key in enumerate(keys):
            with columns[i]:
                button_key = f"button-{key}"
                if st.button(key, key=button_key):
                    self.c2 = int(intervals[key])
                    st.session_state.selected_option = self.c2

        # Creating a number input field
        st.markdown('&nbsp;'*75 + "...or introduce an integer number of minutes in the range (1 - 43200)")
        number = st.number_input('', min_value=1, max_value=43200, step=1, value=None, label_visibility='collapsed')
        if number is not None: 
            self.c2 = number

        st.markdown("<hr>", unsafe_allow_html=True)

        # Horizontal option menu for selecting the graph type.
        self.graph_selected = option_menu(None, ["Candlestick graph of OHLC data", "Stochastic Oscillator & Mobile Mean", "Both options combined"],
                                                icons=['bar-chart-line', 'activity', "layers"],
                                                menu_icon="cast", default_index=0, orientation="horizontal")


    # Method to handle graph generation and display
    def display_graph(self):

        # Verificar si self.c1 es None
        if self.c1 is None:
            st.markdown('&nbsp;'*33 + f'NoneTypeError  -  Please, select a &nbsp;*currency pair*&nbsp; to graph the corresponding data', unsafe_allow_html=True)
            return  # Finalizar la ejecución del método
        
        # Verificar si self.c2 es None
        if self.c2 is None:
            st.markdown('&nbsp;'*30 + f'NoneTypeError  -  Please, choose a &nbsp;*time interval*&nbsp; to graph the corresponding data', unsafe_allow_html=True)
            return  # Finalizar la ejecución del método

        graph = Graph(pair=self.c1, interval=self.c2, divisor=find_largest_divisor(self.c2))
        ohlc_df = graph.obtain_data()
        candlestick, stochastic_mm = graph.candlestick(ohlc_df), graph.stochastic_mm(ohlc_df)

        if self.graph_selected == "Candlestick graph of OHLC data":
            fig = candlestick

        elif self.graph_selected == "Stochastic Oscillator & Mobile Mean":
            fig = stochastic_mm

        elif self.graph_selected == "Both options combined":
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.8, 0.2])
            fig.add_trace(candlestick['data'][0], row=1, col=1)
            fig.add_trace(stochastic_mm['data'][0], row=2, col=1)
            fig.add_trace(stochastic_mm['data'][1], row=2, col=1)

            fig.update_layout(
                title='Candlestick and Stochastic Oscillator',
                yaxis_title='Price',
                xaxis2_title='Time',
                yaxis2_title='%K - %D',
                xaxis_rangeslider_visible=False)

        fig_dict = fig.to_dict()   # Convert the figure to a dictionary for Streamlit to display
        st.plotly_chart(fig_dict)  # Use Streamlit to display the plotly graph

    
    # Method to run the main functionality of the Streamlit app
    def run(self):
        try:
            st.write('Please select a currency pair')  # Prompt user to select a currency pair
            self.select_boxes()   # Call method defined below to display selection boxes
            self.display_graph()  # Call method defined below to display the selected graph
        except Exception as e:
            st.error(f"An error ocurred: {e}")



# Execute the main code only if the script is run directly (and not imported as a module elsewhere)
if __name__ == "__main__":
    front = Front()  # Instantiating an object 'front' from the class 'Front' (which is defined in the 'front' module)
    front.run()      # Running the main process of the 'front' object which starts the streamlit application
