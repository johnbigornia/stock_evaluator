import unittest
import os
import configparser
from datetime import datetime
from src.api.polygon_api import PolygonAPI

class TestPolygonAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load the API key from the config/secrets.properties file
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), '../config/secrets.properties'))
        cls.api_key = config.get('DEFAULT', 'POLYGON_API_KEY')

    def setUp(self):
        # Initialize the API with the loaded API key
        self.api = PolygonAPI(self.__class__.api_key)

    def test_get_stock_data(self):
        # Fetch stock data for a known date range
        data, status_code = self.api.get_stock_data('AAPL', '2023-01-09', '2023-01-10')

        # Check that the response code is 200 (OK)
        self.assertEqual(status_code, 200, "Expected response code to be 200 OK")

        # Check that data is not None
        self.assertIsNotNone(data, "Expected data not to be None")

        # Ensure that data is a list and contains at least one result
        self.assertIsInstance(data, list, "Expected data to be a list")
        self.assertGreater(len(data), 0, "Expected data to contain at least one entry")

        # Check the structure of the first entry in the data list
        result = data[0]
        expected_keys = {'o', 'c', 'h', 'l', 'v', 't', 'n', 'vw'}
        self.assertTrue(expected_keys.issubset(result.keys()), f"Expected keys {expected_keys} in the result")
    
    def test_get_option_chain(self):
        symbol = 'AAPL'  # Test symbol for Apple

        # Fetch the option chain data without specifying expiration date
        data, status_code = self.api.get_option_chain(symbol)

        # Check if the status code is 200 (OK)
        self.assertEqual(status_code, 200, "Expected status code to be 200 OK")

        # Check that data is not None
        self.assertIsNotNone(data, "Expected data not to be None")

        # Ensure that data is a list
        self.assertIsInstance(data, list, "Expected data to be a list")

        # Check if any contracts were returned
        self.assertGreater(len(data), 0, "Expected data to contain at least one option contract")

        # Check the structure of the first contract
        contract = data[0]
        print("Contract keys:", contract.keys())

        # Update expected keys
        expected_keys = {'contract_type', 'strike_price', 'expiration_date', 'underlying_ticker'}
        self.assertTrue(expected_keys.issubset(contract.keys()), f"Expected keys {expected_keys} in the contract")


if __name__ == '__main__':
    unittest.main()

