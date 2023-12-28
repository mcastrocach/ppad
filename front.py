import streamlit as st                         # Import Streamlit for creating web applications
from streamlit_option_menu import option_menu  # Import option_menu for creating option menus in Streamlit apps
from plotly.subplots import make_subplots      # Import make_subplots from Plotly for creating combined plots
from graphs import Graph                       # Import Graph class from the 'graphs' module for graph operations
import time                                    # Import time for converting date to Unix timestamp
import datetime                                # Import datetime for date and time operations

import requests  # Import the requests library for HTTP request handling

st.set_page_config(layout="wide")

import plotly.express as px

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


def set_page_container_style(
        max_width: int = 1100, max_width_100_percent: bool = False,
        padding_top: int = 1, padding_right: int = 10, padding_left: int = 1, padding_bottom: int = 10
    ):
        if max_width_100_percent:
            max_width_str = f'max-width: 100%;'
        else:
            max_width_str = f'max-width: {max_width}px;'
        st.markdown(
            f'''
            <style>
                .reportview-container .css-1lcbmhc .css-1outpf7 {{
                    padding-top: 35px;
                }}
                .reportview-container .main .block-container {{
                    {max_width_str}
                    padding-top: {padding_top}rem;
                    padding-right: {padding_right}rem;
                    padding-left: {padding_left}rem;
                    padding-bottom: {padding_bottom}rem;
                }}
            </style>
            ''',
            unsafe_allow_html=True,
        )

class Front:

    def __init__(self):

        
        st.markdown("""
                        <style>
                            .appview-container .main .block-container {{
                                padding-top: {padding_top}rem;
                                padding-bottom: {padding_bottom}rem;
                                }}

                        </style>""".format(
                        padding_top=1, padding_bottom=1
                    ),
                    unsafe_allow_html=True,
                )

        st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

        st.markdown("""
        <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #5848d5;">
        <a class="navbar-brand" href="https://www.kraken.com/" target="_blank"><b>KRAKEN</b></a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
            <li class="nav-item active">
                <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="https://github.com/mcastrocach/ppad/" target="_blank">GitHub</a>
            </li>
            </ul>
        </div>
        </nav>
        """, unsafe_allow_html=True)

        st.markdown(
            f'''
            <style>
                .reportview-container .sidebar-content {{
                    padding-top: {1}rem;
                }}
                .reportview-container .main .block-container {{
                    padding-top: {1}rem;
                }}
            </style>
            ''',unsafe_allow_html=True)

        set_page_container_style(
                max_width = 1100, max_width_100_percent = True,
                padding_top = 0, padding_right = 10, padding_left = 5, padding_bottom = 10
        )

        hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
        st.markdown(hide_st_style, unsafe_allow_html=True)

        st.markdown('# **KRAKEN CURRENCY ANALYSIS TOOL**')
        st.markdown("<hr>", unsafe_allow_html=True)                               # Inserts a horizontal line for visual separation

        self.currency_pair = None                                                   # Placeholder for the first currency in the pair
        st.session_state.selected_option = st.session_state.get("selected_option")  # Retrieve or initialize the selected time interval for each candle
        st.session_state.is_custom_interval = st.session_state.get("is_custom_interval")
        st.session_state.custom_interval = st.session_state.get("custom_interval")
        self.time_interval = st.session_state.selected_option                       # Store the time interval for each candle from the session state
        self.since, self.until = None, None                                         # Initialize since and until attributes


    # Method to create user input interfaces, including dropdowns and buttons
    def select_boxes(self):

        # Prompt user to select a currency pair from the pairs retrieved
        st.write("1. Please select a currency pair from the available options.")

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
            st.session_state.is_custom_interval = not st.session_state.is_custom_interval
        if st.session_state.is_custom_interval:
            st.session_state.custom_interval = st.number_input('Custom interval', min_value=1, max_value=43200, step=1, value=None, label_visibility='collapsed')
        if st.session_state.custom_interval is not None: 
            self.time_interval = st.session_state.custom_interval
            st.session_state.selected_option = st.session_state.custom_interval# Update the time interval with the custom input

        st.markdown("<hr>", unsafe_allow_html=True)  # Inserts a horizontal line for visual separation

        st.markdown("3. Optionally, choose a time interval within the range of the original selection:")
        
        # Date picker for selecting the start date
        columns0, columns1 = st.columns([1, 1])
        with columns0:
            with st.expander("Start Date", expanded=True):
                self.since = st.date_input('start', value=None, label_visibility = "collapsed")
                if self.since is not None:
                    # Convert date to datetime
                    self.since = datetime.datetime.combine(self.since, datetime.datetime.min.time())
                    self.since = datetime.datetime.strptime(str(self.since), "%Y-%m-%d %H:%M:%S").timestamp()
        with columns1:
            with st.expander("End Date", expanded=True):
                self.until = st.date_input('end', value=None, label_visibility = "collapsed")
                if self.until is not None:
                    # Convert date to datetime
                    self.until = datetime.datetime.combine(self.until, datetime.datetime.min.time())
                    self.until = datetime.datetime.strptime(str(self.until), "%Y-%m-%d %H:%M:%S").timestamp()


    # Method to generate and display graphs based on user-selected parameters
    def display_graph(self):

        # Horizontal menu for selecting the type of graph to display
        self.graph_selected = option_menu(None, ["Candlestick graph of OHLC data", "Stochastic Oscillator & Smoothed Version", "Both options combined"],
                                                icons=['bar-chart-line', 'activity', "layers"],
                                                menu_icon="cast", default_index=0, orientation="horizontal")

        if self.graph_selected != None:
            # Conditional to verify if self.currency_pair is of NoneType
            if self.currency_pair is None:
                st.markdown('&nbsp;'*30 + 'Please, select a &nbsp;*currency pair*&nbsp; to graph the corresponding data', unsafe_allow_html=True)
                return  # End the execution of this method
            
            # Conditional to verify if self.time_interval is of NoneType
            if self.time_interval is None:
                st.markdown('&nbsp;'*30 + 'Please, choose a &nbsp;*time interval*&nbsp; to graph the corresponding data', unsafe_allow_html=True)
                return  # End the execution of this method

        graph = Graph(pair=self.currency_pair, interval=self.time_interval, divisor=find_largest_divisor(self.time_interval), since=self.since, until=self.until)
        ohlc_df = graph.obtain_data()
        candlestick, stochastic = graph.candlestick(ohlc_df), graph.stochastic(ohlc_df)

        if self.graph_selected == "Candlestick graph of OHLC data":
            fig = candlestick

        elif self.graph_selected == "Stochastic Oscillator & Smoothed Version":
            fig = stochastic

        elif self.graph_selected == "Both options combined":
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.8, 0.2], specs=[[{"secondary_y": True}], [{}]])
            fig.add_trace(candlestick['data'][0], row=1, col=1, secondary_y=True)
            fig.add_trace(candlestick['data'][1], row=1, col=1, secondary_y=False)
            fig.add_trace(candlestick['data'][2], row=1, col=1, secondary_y=True)
            fig.add_trace(candlestick['data'][3], row=1, col=1, secondary_y=True)
            fig.add_trace(stochastic['data'][0], row=2, col=1)
            fig.add_trace(stochastic['data'][1], row=2, col=1)

            fig.update_layout(
                title='Candlestick Graph with Moving Average and Stochastic Oscillator',
                yaxis3_title='%K - %D',
                xaxis_rangeslider_visible=False,
                height=450, width = 650)


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

            # Invoke methods to display user input options and the graph based on selections
            col1, spacer, col2 = st.columns([100,5,95])
            with col1:
                self.select_boxes()   # Displays currency pair and time interval selection options

            with col2:
                self.display_graph()  # Renders the graph based on user selections

        except Exception as e:
            # Handle and display any exceptions that occur during execution
            st.error(f"An error occurred: {e}")  # Show the error message to the user in the app