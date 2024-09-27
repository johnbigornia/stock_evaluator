import requests

class PolygonAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_stock_data(self, symbol, start_date, end_date):
        url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?apiKey={self.api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()['results'], response.status_code
        else:
            print(f"Error fetching stock data: {response.status_code} - {response.text}")
            return None, response.status_code
        

    def get_option_chain(self, symbol, expiration_date=None, limit=100):
        url = f'https://api.polygon.io/v3/reference/options/contracts?underlying_ticker={symbol}&apiKey={self.api_key}'
        if expiration_date:
            url += f'&expiration_date={expiration_date}'
        url += f'&limit={limit}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['results'], response.status_code
        else:
            print(f"Error fetching option chain: {response.status_code} - {response.text}")
            return None, response.status_code
