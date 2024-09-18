import requests

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
