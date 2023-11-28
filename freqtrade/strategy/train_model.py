import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def create_target(df, n=1):
    """
    Create a binary target variable based on future price increase.
    :param df: DataFrame with at least a 'close' column.
    :param n: Number of periods to look ahead for price increase.
    :return: DataFrame with a new 'target' column.
    """
    # Shift the closing price by -n periods
    df['future_close'] = df['close'].shift(-n)

    # If future close is higher than current close, label as 1, else 0
    df['target'] = (df['future_close'] > df['close']).astype(int)

    # Drop the last n rows which will have NaN values for 'future_close'
    df = df[:-n]
    return df

def train_model(df):
    # Apply the target creation function
    df = create_target(df, n=1)  # Adjust 'n' as needed for your strategy

    # Define your features and target variable
    # Replace these feature names with the actual names from your dataset
    X = df[['open', 'high', 'low', 'close', 'volume']]
    y = df['target']

    # Initialize and train the model
    model = RandomForestClassifier()
    model.fit(X, y)
    return model

# Load your dataset
df = pd.read_csv('processed_data.csv')

# Train the model
model = train_model(df)

# Save the trained model to a file
joblib.dump(model, 'trading_model.pkl')
