import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.impute import SimpleImputer
import joblib

def create_target(df, n=1):
    """
    Create a binary target variable based on future price increase.
    :param df: DataFrame with at least a 'close' column.
    :param n: Number of periods to look ahead for price increase.
    :return: DataFrame with a new 'target' column.
    """
    df['future_close'] = df['close'].shift(-n)
    df['target'] = (df['future_close'] > df['close']).astype(int)
    df = df[:-n]  # Drop the last n rows with NaN values
    return df

def train_model(df):
    df = create_target(df, n=1)  # Adjust 'n' as needed

    # Define your features and target variable
    feature_columns = ['open', 'high', 'low', 'close', 'volume', 'sma', 'ema', 'rsi', 'macd', 'macdsignal', 'macdhist', 'upperband', 'middleband', 'lowerband']
    X = df[feature_columns]
    y = df['target']

    # Initialize the imputer with a strategy (e.g., mean, median, or most_frequent)
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

    # Fit and transform the imputer on your X data
    X_imputed = imputer.fit_transform(X)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

    # Initialize and train the model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Evaluate the model
    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions))

    return model

# Load your dataset
df = pd.read_csv(r'A:\All_FIles_and_Folders\Documents\freqtradejt\freqtrade\user_data\data\processed_data.csv')

# Train the model
model = train_model(df)

# Save the trained model to a file
joblib.dump(model, r'A:\All_FIles_and_Folders\Documents\freqtradejt\freqtrade\user_data\data\trading_model.pkl')
