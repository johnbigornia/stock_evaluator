from datetime import datetime, timedelta  # Import the datetime class, not the module

import unittest
import os
import configparser
from src.api.polygon_api import PolygonAPI

class TestPolygonAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load the API key from the config/secrets.properties file
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), '../config/secrets.properties'))
        cls.api_key = config.get('DEFAULT', 'POLYGON_API_KEY')

    def setUp(self):
        # Use the API key loaded from the config file
        self.api = PolygonAPI(self.__class__.api_key)
        # Get current date in the correct format
        self.expiration_date = datetime.now().strftime('%Y-%m-%d')

    def test_get_stock_data(self):
        data, status_code = self.api.get_stock_data('AAPL', '2023-01-09', '2023-01-10')

        # Check that the response code is 200 (OK)
        self.assertEqual(status_code, 200, "Expected response code to be 200 OK")

        # Check that 'results' is in the response data
        self.assertIn('results', data, "Expected 'results' to be in the API response")
        print(data)
        
        # Ensure that the results are a list and contain at least one result
        self.assertIsInstance(data['results'], list, "Expected 'results' to be a list")
        self.assertGreater(len(data['results']), 0, "Expected 'results' to contain at least one entry")
        
        # Check the structure of the first entry in the 'results' list
        result = data['results'][0]
        self.assertIn('o', result, "Expected 'o' (open price) in the result")
        self.assertIn('c', result, "Expected 'c' (close price) in the result")
        self.assertIn('h', result, "Expected 'h' (high price) in the result")
        self.assertIn('l', result, "Expected 'l' (low price) in the result")
        self.assertIn('v', result, "Expected 'v' (volume) in the result")

    def test_get_option_chain(self):
        symbol = 'AAPL'  # Test symbol for Apple

        # Fetch the option chain data without specifying expiration date
        data, status_code = self.api.get_option_chain(symbol)

        # Check if the status code is 200 (OK)
        self.assertEqual(status_code, 200, "Expected status code to be 200 OK")

        # Ensure that 'results' is in the response
        self.assertIn('results', data, "Expected 'results' in the response data")

        # Ensure that the results are a list
        self.assertIsInstance(data['results'], list, "Expected 'results' to be a list")

        # Print the available options or expiration dates for debugging
        print(data)

        # Check if any contracts were returned
        self.assertGreater(len(data['results']), 0, "Expected 'results' to contain at least one option contract")


if __name__ == '__main__':
    unittest.main()
