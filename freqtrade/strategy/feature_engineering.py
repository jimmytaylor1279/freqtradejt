import pandas as pd

def add_technical_indicators(df):
    df['sma'] = df['close'].rolling(window=20).mean()
    # Add more technical indicators as needed
    return df

# Load data
df = pd.read_csv('historical_data.csv')
df = add_technical_indicators(df)
df.to_csv('processed_data.csv', index=False)
