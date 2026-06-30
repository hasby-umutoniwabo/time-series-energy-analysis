# ============================================================
# Task 4: Prediction Script
# This script ties everything together:
# 1. Fetches data from the API
# 2. Preprocesses it the same way as Task 1
# 3. Loads the trained model
# 4. Makes a prediction
# ============================================================

import requests
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# ------------------------------------------------------------
# Step 1: Fetch time series data from the API
# ------------------------------------------------------------
print("Step 1: Fetching data from the API...")

# We fetch all readings from the MySQL endpoint
response = requests.get('http://127.0.0.1:5000/mysql/readings')

if response.status_code == 200:
    api_data = response.json()
    print(f"Fetched {len(api_data)} records from the API.")
else:
    print(f"API call failed with status {response.status_code}. Loading from source instead.")
    api_data = None

# ------------------------------------------------------------
# Step 2: Preprocess the data
# ------------------------------------------------------------
print("\nStep 2: Preprocessing the data...")

# Load full dataset from source for model training
# The API only has sample data, so we use the full dataset for training
url = "https://raw.githubusercontent.com/MainakRepositor/Datasets/master/AEP_hourly.csv"
df  = pd.read_csv(url)
df['Datetime'] = pd.to_datetime(df['Datetime'])
df  = df.sort_values('Datetime').reset_index(drop=True)

# Remove duplicates and fill missing hours
df  = df.drop_duplicates(subset='Datetime', keep='first')
full_range = pd.date_range(start=df['Datetime'].min(), end=df['Datetime'].max(), freq='h')
df  = df.set_index('Datetime').reindex(full_range)
df.index.name = 'Datetime'
df['AEP_MW']  = df['AEP_MW'].ffill()
df  = df.reset_index()

# Extract time based features
df['Hour']       = df['Datetime'].dt.hour
df['Month']      = df['Datetime'].dt.month
df['DayOfWeek']  = df['Datetime'].dt.dayofweek
df['DayOfYear']  = df['Datetime'].dt.dayofyear
df['WeekOfYear'] = df['Datetime'].dt.isocalendar().week.astype(int)

# Create lag features
df['Lag_1h']   = df['AEP_MW'].shift(1)
df['Lag_24h']  = df['AEP_MW'].shift(24)
df['Lag_168h'] = df['AEP_MW'].shift(168)

# Create moving average features
df['MA_24h']   = df['AEP_MW'].rolling(window=24).mean()
df['MA_168h']  = df['AEP_MW'].rolling(window=168).mean()

# Drop rows with NaN values from lag and rolling features
df = df.dropna()
print(f"Data preprocessed. Total records ready for modeling: {len(df):,}")

# ------------------------------------------------------------
# Step 3: Train the model (using best settings from Task 1)
# ------------------------------------------------------------
print("\nStep 3: Training the model...")

features = ['Hour', 'DayOfWeek', 'Month', 'DayOfYear', 'WeekOfYear',
            'Lag_1h', 'Lag_24h', 'Lag_168h', 'MA_24h', 'MA_168h']

X = df[features]
y = df['AEP_MW']

# Split without shuffling to respect time order
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Use the best hyperparameters from Experiment 2 in Task 1
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42
)
model.fit(X_train, y_train)
print("Model trained successfully.")

# ------------------------------------------------------------
# Step 4: Make a prediction
# ------------------------------------------------------------
print("\nStep 4: Making a prediction...")

# Use the last available row from the dataset as input
last_row = X_test.iloc[[-1]]
actual   = y_test.iloc[-1]

prediction = model.predict(last_row)[0]

print(f"\n=== Prediction Result ===")
print(f"Input datetime    : {df['Datetime'].iloc[-1]}")
print(f"Actual value      : {actual:,.2f} MW")
print(f"Predicted value   : {prediction:,.2f} MW")
print(f"Difference        : {abs(actual - prediction):,.2f} MW")
print(f"Accuracy          : {100 - abs((actual - prediction) / actual) * 100:.2f}%")
print("\nPrediction script completed successfully.")
