import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Load dataset
data = pd.read_csv("query (2).csv")

# Keep only numeric columns
data = data.select_dtypes(include=["number"])

print("\nColumns used for training:")
print(data.columns.tolist())

# Remove rows where OUTPUT (last column) is NaN
data = data.dropna(subset=[data.columns[-1]])

# Ensure no NaN in feature columns
data = data.fillna(0)

# Split features & target
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model creation
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate
pred = model.predict(X_test)
mae = mean_absolute_error(y_test, pred)

print(f"\nTraining successful! MAE = {mae:.4f}")

# Save model
joblib.dump(model, "eq_model_bundle_new.pkl")
print("\nModel saved → eq_model_bundle_new.pkl")