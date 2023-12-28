import unittest  # import the unittest module for creating test cases
from front import *  # import everything from the 'front' module
from graphs import aggregate_intervals
import pandas as pd
import plotly.graph_objs as go
from unittest.mock import patch
from math import gcd

def lcm(a, b):
    return abs(a * b) // gcd(a, b)


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

    def test_largest_divisor_lcm(self):
        # Sample pairs of numbers to test
        test_pairs = [(6, 8), (15, 25), (9, 14)]

        for a, b in test_pairs:
            product = a * b
            largest_divisor_product = find_largest_divisor(product)
            lcm_largest_divisors = lcm(find_largest_divisor(a), find_largest_divisor(b))

            self.assertEqual(largest_divisor_product, lcm_largest_divisors)

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

class TestAggregateIntervals(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up data that can be used across all tests
        data = {
            'Open': [100, 101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [95, 96, 97, 98, 99],
            'Close': [102, 103, 104, 105, 106],
            'SMA': [100, 100.5, 101, 101.5, 102],
            'EMA': [100, 100.25, 100.5, 100.75, 101],
            'Volume': [1000, 1500, 2000, 2500, 3000]
        }
        index = pd.date_range('2020-01-01', periods=5, freq='T')
        cls.df = pd.DataFrame(data, index=index)

    def test_aggregate_intervals_1min(self):
        interval = 1
        resampled_df = aggregate_intervals(interval, self.df)
        self.assertEqual(len(resampled_df), len(self.df.resample(f'{interval}T')))
        self.assertSetEqual(set(resampled_df.columns), set(self.df.columns))

    def test_aggregate_intervals_5min(self):
        interval = 5
        resampled_df = aggregate_intervals(interval, self.df)
        self.assertEqual(len(resampled_df), len(self.df.resample(f'{interval}T')))
        self.assertSetEqual(set(resampled_df.columns), set(self.df.columns))

    def test_aggregate_intervals_invalid(self):
        with self.assertRaises(ValueError):
            aggregate_intervals(-1, self.df)

# This block runs if the script is executed directly
if __name__ == '__main__':  
    unittest.main()  # Running the unittest main function which runs all test methods
