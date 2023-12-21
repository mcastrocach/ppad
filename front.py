import streamlit as st                         # Import Streamlit for creating web applications
from streamlit_option_menu import option_menu  # Import option_menu for creating option menus in Streamlit apps
from plotly.subplots import make_subplots      # Import make_subplots from Plotly for creating combined plots
from graphs import Graph                       # Import Graph class from the 'graphs' module for graph operations


import requests  # Import the requests library for HTTP request handling

# Retrieves all available currency pairs from the Kraken cryptocurrency exchange API
def get_kraken_pairs():
    url = 'https://api.kraken.com/0/public/AssetPairs'  # Endpoint URL for fetching Kraken currency pairs
    response = requests.get(url)                        # Send a GET request to the Kraken API
    response_json = response.json()                     # Convert the response to JSON format
    pairs = response_json['result'].keys()              # Extract currency pair identifiers from the JSON data
    return tuple(pairs)                                 # Return the currency pairs as a tuple

kraken_pairs = get_kraken_pairs()  # Get and store the list of currency pairs available on Kraken


# A dictionary mapping time intervals to their durations in minutes
intervals = {"1m":1, "5m":5, "15m":15, "30m":30, "1h":60, "4h":240, "1d":1440, "1w":10080, "2w":21600}
keys, options = intervals.keys(), intervals.values()  # Separate lists of interval labels and their corresponding durations

# Finds the largest duration in 'intervals' that is a divisor of 'n'
def find_largest_divisor(n):
    valid_divisors = [d for d in options if n % d == 0]  # Filters durations that are divisors of 'n'
    if not valid_divisors:
        return None                                      # Returns None if no valid divisors are found
    return max(valid_divisors)                           # Returns the largest divisor found


# The Front class manages the front-end of the application, particularly the Streamlit interface
class Front:

    # Constructor for initializing the Front class instances
    def __init__(self):
        st.title("Kraken Currency Analysis Tool")                                 # Displays the title on the Streamlit app interface
        st.markdown("Authors: Rodrigo de la Nuez Moraleda, Marcos Castro Cacho")  # Credits authors in the app
        st.markdown("<hr>", unsafe_allow_html=True)                               # Inserts a horizontal line for visual separation

        # Initialize variables for tracking currency pair selections
        self.currency_pair = None                                                   # Placeholder for the first currency in the pair
        st.session_state.selected_option = st.session_state.get("selected_option")  # Retrieve or initialize the selected time interval for each candle
        self.time_interval = st.session_state.selected_option                       # Store the time interval for each candle from the session state


    # Method to create user input interfaces, including dropdowns and buttons
    def select_boxes(self):

        # Dropdown menu for selecting a currency pair
        self.currency_pair = st.selectbox(
           label = 'placeholder',            # Streamlit's selectbox requires a label, even when collapsed
           options = kraken_pairs,           # List of currency pairs from Kraken
           index = None,
           placeholder = "xxxxxxx",          # Placeholder text in the dropdown
           label_visibility = "collapsed"
        )

        st.markdown("<hr>", unsafe_allow_html=True)  # Inserts a horizontal line for visual separation

        # Applies dynamic CSS to highlight the selected time interval button
        st.markdown("2. Choose a time window from the most commonly used options:" + 
            f"""
            <style>
            div.stButton > button {{
                width: 100%;
            }}
            div.stButton > button# {{
                background-color: #0d6efd;
                color: white;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        # Generate a row of buttons for selecting time intervals
        columns = st.columns(len(keys))
        for i, key in enumerate(keys):
            with columns[i]:
                button_key = f"button-{key}"
                if st.button(key, key=button_key):
                    self.time_interval = int(intervals[key])               # Sets the selected time interval
                    st.session_state.selected_option = self.time_interval  # Updates the session state

        # Button for allowing custom time interval input
        if st.button("...or enter a custom time interval (in minutes)", key="Other"):
            # Input field for custom time interval in minutes
            number = st.number_input('', min_value=1, max_value=43200, step=1, value=None, label_visibility='collapsed')
            if number is not None: 
                self.time_interval = number  # Update the time interval with the custom input


        st.markdown("<hr>", unsafe_allow_html=True)  # Inserts a horizontal line for visual separation

        # Horizontal menu for selecting the type of graph to display
        self.graph_selected = option_menu(None, ["Candlestick graph of OHLC data", "Stochastic Oscillator & Mobile Mean", "Both options combined"],
                                                icons=['bar-chart-line', 'activity', "layers"],
                                                menu_icon="cast", default_index=0, orientation="horizontal")


    # Method to generate and display graphs based on user-selected parameters.
    # Method to handle graph generation and display
    def display_graph(self):

        if st.button("Plot it!") or 'fig_dict' in st.session_state:

            # Conditional to verify if self.currency_pair is of NoneType
            if self.currency_pair is None:
                st.markdown('&nbsp;'*33 + f'NoneTypeError  -  Please, select a &nbsp;*currency pair*&nbsp; to graph the corresponding data', unsafe_allow_html=True)
                return  # End the execution of this method
            
            # Conditional to verify if self.time_interval is of NoneType
            if self.time_interval is None:
                st.markdown('&nbsp;'*30 + f'NoneTypeError  -  Please, choose a &nbsp;*time interval*&nbsp; to graph the corresponding data', unsafe_allow_html=True)
                return  # End the execution of this method

            graph = Graph(pair=self.currency_pair, interval=self.time_interval, divisor=find_largest_divisor(self.time_interval))
            ohlc_df = graph.obtain_data()
            candlestick, stochastic_mm = graph.candlestick(ohlc_df), graph.stochastic_mm(ohlc_df)

            if self.graph_selected == "Candlestick graph of OHLC data":
                fig = candlestick

            elif self.graph_selected == "Stochastic Oscillator & Mobile Mean":
                fig = stochastic_mm

            elif self.graph_selected == "Both options combined":
                fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[0.8, 0.2,0.3])
                fig.add_trace(candlestick['data'][0], row=1, col=1)
                fig.add_trace(candlestick['data'][1], row=1, col=1)
                fig.add_trace(candlestick['data'][2], row=1, col=1)
                fig.add_trace(stochastic_mm['data'][0], row=2, col=1)
                fig.add_trace(stochastic_mm['data'][1], row=2, col=1)

                fig.update_layout(
                    title='Candlestick and Stochastic Oscillator with Mobile Mean',
                    yaxis_title='Price',
                    xaxis2_title='Time',
                    yaxis2_title='%K - %D',
                    xaxis_rangeslider_visible=False)


            fig_dict = fig.to_dict()   # Convert the figure to a dictionary for Streamlit to display
            st.session_state['fig_dict'] = fig_dict  # Save the figure to the session state
            st.plotly_chart(fig_dict)  # Use Streamlit to display the plotly graph

            # Moved the button definition here
            profit_df = graph.calculate_profit(ohlc_df)
            fig_profit = graph.profit_graph(profit_df)
            if st.button("Calculate potential earnings"):
                if fig_profit is not None:
                    st.write("This graph simulates potential profit based on the data.")
                    st.write("Every time a \"Buy Signal\" occurs we buy a 100 units of the currency, every time a \"Sell signal\" we sell a 100 units of the currency.")
                    fig_profit_dict = fig_profit.to_dict()
                    st.plotly_chart(fig_profit_dict)  # Use Streamlit to display the plotly graph
                else:
                    st.write("There are no buy signals")

    
    # Method to execute the core operations of the Streamlit application
    def run(self):
        try:
            # Prompt user to select a currency pair from the pairs retrieved
            st.write("1. Please select a currency pair from the available options.")

            # Invoke methods to display user input options and the graph based on selections
            self.select_boxes()   # Displays currency pair and time interval selection options
            self.display_graph()  # Renders the graph based on user selections

        except Exception as e:
            # Handle and display any exceptions that occur during execution
            st.error(f"An error occurred: {e}")  # Show the error message to the user in the app