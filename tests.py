import unittest  # import the unittest module for creating test cases
from front import *  # import everything from the 'front' module
import pandas as pd
import plotly.graph_objs as go
from unittest.mock import patch

# Definition of a test case class for the 'front' module
class TestFront(unittest.TestCase):

    # Test method to test the initialization of the Front class
    @patch('streamlit.session_state', {'selected_option': None})
    def test_init(self):  
        with patch('streamlit.session_state', new_callable=lambda: {'selected_option': None}):

            front = Front()  # create an instance of the Front class

            # Asserting that the initial values of c1, c2, and select_graph are as expected
            self.assertEqual(front.currency_pair, None)  
            self.assertEqual(front.time_interval, None)
            self.assertEqual(front.since, None)
            self.assertEqual(front.until, None)
            self.assertEqual(front.select_graph, "Candlestick")

    # Test method to test the get_kraken_pairs function
    def test_get_kraken_pairs(self):
        result = get_kraken_pairs()  # Calling the get_kraken_pairs function and storing its result
        
        # Checking if the result is a tuple and has a length greater than 0
        self.assertIsInstance(result, tuple)
        self.assertTrue(len(result) > 0)

class TestGraph(unittest.TestCase):

    def test_find_largest_divisor(self):
        self.assertEqual(find_largest_divisor(60), 60)
        self.assertEqual(find_largest_divisor(61), 1)
        self.assertEqual(find_largest_divisor(120), 60)

    def test_obtain_data(self):
        graph = Graph(pair='XETHZUSD', interval=1440, divisor=1)
        df = graph.obtain_data()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)

    def test_candlestick(self):
        graph = Graph(pair='XETHZUSD', interval=1440, divisor=1)
        df = graph.obtain_data()
        fig = graph.candlestick(df)
        self.assertIsInstance(fig, go.Figure)

    def test_stochastic_mm(self):
        graph = Graph(pair='XETHZUSD', interval=1440, divisor=1)
        df = graph.obtain_data()
        fig = graph.stochastic(df)
        self.assertIsInstance(fig, go.Figure)

    # New test method to test the initialization of the Graph class
    def test_init(self):
        graph = Graph(pair='XETHZUSD', interval=1440, divisor=1)  # create an instance of the Graph class
        self.assertEqual(graph.pair, 'XETHZUSD')  # Asserting that the pair attribute is correctly set
        self.assertEqual(graph.interval, 1440)  # Asserting that the interval attribute is correctly set
        self.assertEqual(graph.divisor, 1)  # Asserting that the divisor attribute is correctly set

# This block runs if the script is executed directly
if __name__ == '__main__':  
    unittest.main()  # Running the unittest main function which runs all test methods
