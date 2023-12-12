import pandas as pd
import talib

def add_technical_indicators(df):
    # Simple Moving Average
    df['sma'] = df['close'].rolling(window=20).mean()

    # Exponential Moving Average
    df['ema'] = df['close'].ewm(span=20, adjust=False).mean()

    # Relative Strength Index
    df['rsi'] = talib.RSI(df['close'], timeperiod=14)

    # Moving Average Convergence Divergence
    macd, macdsignal, macdhist = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['macd'] = macd
    df['macdsignal'] = macdsignal
    df['macdhist'] = macdhist

    # Bollinger Bands
    upperband, middleband, lowerband = talib.BBANDS(df['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    df['upperband'] = upperband
    df['middleband'] = middleband
    df['lowerband'] = lowerband

    # Add more indicators as needed

    return df

# Load data
df = pd.read_csv('historical_data.csv')
df = add_technical_indicators(df)
df.to_csv('processed_data.csv', index=False)
