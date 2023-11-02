import streamlit as st
#from graphs.Stochastic import generate_graph
from graphs.Stochastic import Stochastic
from graphs.MobileMeanStochastic import MobileMeanStochastic
from streamlit_option_menu import option_menu
import plotly.graph_objects as go

class Front:
    def __init__(self):
        st.title("Kraken graphs")
        c1 = "XETHZUSD"
        c2 = "21600"
        select_graph = "Stochastic"

    def run(self):
        st.write('Please select a currency pair')
        self.select_boxes()
        self.display_graph()

    def select_boxes(self):
        #dropdown to select currency pair
        #TODO curate input options to only include valid currency pairs
        self.c1 = st.selectbox(
           "Please select currency pair",
           ("XETHZUSD", "XXBTZUSD", "XLTCZUSD", "XETHXXBT", "XLTCXXBT", "XLTCZUSD", "XETHZUSD", "XXBTZUSD", "XXMRZUSD", "XXMRXXBT", "XXMRZEUR", "XXMRXBT", "XXMRXXBT", "XXMRZEUR", "XXMRZUSD", "XXRPZUSD", "XXRPXXBT", "XXRPZUSD", "XXRPXXBT", "XXRPZEUR", "XXRPZUSD", "XZECZUSD", "XZECXXBT", "XZECZEUR", "XZECZUSD", "XZECXXBT", "XZECZEUR", "XZECZUSD", "XETCZUSD", "XETCXXBT", "XETCZEUR", "XETCZUSD", "XETCXXBT", "XETCZEUR", "XETCZUSD", "XETHZUSD", "XETHXXBT", "XETHZEUR", "XETHZUSD", "XETHXXBT", "XETHZEUR", "XETHZUSD", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD", "XLTCZUSD", "XLTCXXBT", "XLTCZEUR", "XLTCZUSD", "XLTCXXBT", "XLTCZEUR", "XLTCZUSD", "XETHZUSD", "XETHXXBT", "XETHZEUR", "XETHZUSD", "XETHXXBT", "XETHZEUR", "XETHZUSD", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD", "XXBTZEUR", "XXBTZUSD"),
           index=None,
           placeholder="Select currency pair...",
        )

        ##dropdown to select interval
        ##TODO curate input options to only include valid intervals
        #self.c2 = st.selectbox(
        #    "Please select interval",
        #    ("1", "5", "15", "30", "60", "240", "1440", "10080", "21600"),
        #    index=None,
        #    placeholder="Select interval...",
        #)
        # Dropdown to select intervals
        self.c2 = st.select_slider(
            "Please select interval",
            ["1", "5", "15", "30", "60", "240", "1440", "10080", "21600"],
        )

        self.graph_select = option_menu(None, ["Stochastic", "MobileMean", "Merge them", "Nada"], 
    icons=['house', 'cloud-upload', "list-task", 'gear'],#TODO Iconos?
    menu_icon="cast", default_index=0, orientation="horizontal")

   #button to generate graph
    def display_graph(self):
        if st.button('Plot it!'):
            if self.graph_select == "Stochastic":
                fig = Stochastic(pair=self.c1, interval=self.c2).generate_graph()
            elif self.graph_select == "MobileMean":
                fig = MobileMeanStochastic(pair=self.c1, interval=self.c2).generate_graph()
            elif self.graph_select == "Merge them":
                #merge both graphs
                fig = Stochastic(pair=self.c1, interval=self.c2).generate_graph()
                fig2 = MobileMeanStochastic(pair=self.c1, interval=self.c2).generate_graph()
                line_trace = fig2.data[0]
                fig.add_trace(line_trace)
            fig_dict = fig.to_dict()
            st.plotly_chart(fig_dict)

if __name__ == "__main__":
    app = Front()
    app.run()
