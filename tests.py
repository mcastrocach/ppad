import unittest
from front import *

class TestFront(unittest.TestCase):
    def test_init(self):
        front = Front()
        self.assertEqual(front.c1, "XETHZUSD")
        self.assertEqual(front.c2, "21600")
        self.assertEqual(front.select_graph, "Stochastic")
    def test_get_kraken_pairs(self):
        result = get_kraken_pairs()
        self.assertIsInstance(result, tuple)
        self.assertTrue(len(result) > 0)
    # Add more test cases as needed...

if __name__ == '__main__':
    unittest.main()