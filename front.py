import streamlit as st
#from graphs.Stochastic import generate_graph
from graphs.Stochastic import Stochastic

class Front:
    def __init__(self):
        st.title("Kraken graphs")
        c1 = "XETHZUSD"
        c2 = "21600"

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

        #dropdown to select interval
        #TODO curate input options to only include valid intervals
        self.c2 = st.selectbox(
            "Please select interval",
            ("1", "5", "15", "30", "60", "240", "1440", "10080", "21600"),
            index=None,
            placeholder="Select interval...",
        )

    #button to generate graph
    def display_graph(self):
        if st.button('Plot it!'):
            fig = Stochastic(pair=self.c1, interval=self.c2).generate_graph()
            #fig = generate_graph(pair=self.c1, interval=self.c2)
            fig_dict = fig.to_dict()
            st.plotly_chart(fig_dict)

if __name__ == "__main__":
    app = Front()
    app.run()
