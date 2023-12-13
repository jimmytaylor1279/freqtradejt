import requests
import pandas as pd
import os
from datetime import datetime

def fetch_data(pair, since):
    url = f'https://api.kraken.com/0/public/OHLC?pair={pair}&since={since}&interval=1'
    response = requests.get(url)
    data = response.json()['result'][pair]
    df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])

    # Convert Unix timestamp to datetime
    df['time'] = pd.to_datetime(df['time'], unit='s')

    # Select required columns and rename them
    df = df[['time', 'open', 'high', 'low', 'close', 'volume']]
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

    return df

# Example usage
pair = 'XXBTZUSD'  # Bitcoin to USD pair
since = '1609459200'  # Unix timestamp (e.g., January 1, 2021)
df = fetch_data(pair, since)
df.to_csv(r'A:\All_FIles_and_Folders\Documents\freqtradejt\freqtrade\user_data\data\kraken\BTC_USD-1m.csv', index=False)

print("Current Working Directory:", os.getcwd())
