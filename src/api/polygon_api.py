import requests
from datetime import datetime, timedelta

class PolygonAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_stock_data(self, symbol, start_date, end_date):
        url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?apiKey={self.api_key}'
        response = requests.get(url)
        
        # Print or return the status code for debugging
        print(f"Response Code: {response.status_code}")
        
        # Return both status code and the data (for use in tests)
        return response.json(), response.status_code

import requests
from datetime import datetime, timedelta

class PolygonAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_stock_data(self, symbol, start_date, end_date):
        url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?apiKey={self.api_key}'
        response = requests.get(url)
        
        # Print or return the status code for debugging
        print(f"Response Code: {response.status_code}")
        
        # Return both status code and the data (for use in tests)
        return response.json(), response.status_code

    def get_option_chain(self, symbol, expiration_date=None, limit=100):
        url = f'https://api.polygon.io/v3/reference/options/contracts?underlying_ticker={symbol}&apiKey={self.api_key}'
        
        # Optionally, add expiration date if provided
        if expiration_date:
            url += f'&expiration_date={expiration_date}'
        
        # Limit the number of results
        url += f'&limit={limit}'

        response = requests.get(url)
        
        # Print the status code for debugging
        print(f"Response Code: {response.status_code}")
        
        # Return both the response JSON and status code for debugging or further use
        return response.json(), response.status_code

