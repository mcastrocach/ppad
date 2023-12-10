import unittest  # import the unittest module for creating test cases
from front import *  # import everything from the 'front' module


# Definition of a test case class for the 'front' module
class TestFront(unittest.TestCase):  

    # Test method to test the initialization of the Front class
    def test_init(self):  
        front = Front()  # create an instance of the Front class

        # Asserting that the initial values of c1, c2, and select_graph are as expected
        self.assertEqual(front.c1, "XETHZUSD")  
        self.assertEqual(front.c2, None)
        self.assertEqual(front.select_graph, "Stochastic")

    # Test method to test the get_kraken_pairs function
    def test_get_kraken_pairs(self):
        result = get_kraken_pairs()  # Calling the get_kraken_pairs function and storing its result
        
        # Checking if the result is a tuple and has a length greater than 0
        self.assertIsInstance(result, tuple)
        self.assertTrue(len(result) > 0)

    # Additional test methods can be added here as needed


# This block runs if the script is executed directly
if __name__ == '__main__':  
    unittest.main()  # Running the unittest main function which runs all test methods