import requests
import pandas as pd

def fetch_data(pair, since):
    url = f'https://api.kraken.com/0/public/OHLC?pair={pair}&since={since}&interval=1'
    response = requests.get(url)
    data = response.json()['result'][pair]
    df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
    return df

# Example usage
pair = 'XXBTZUSD'  # Bitcoin to USD pair
since = '1609459200'  # Unix timestamp (e.g., January 1, 2021)
df = fetch_data(pair, since)
df.to_csv('historical_data.csv', index=False)
