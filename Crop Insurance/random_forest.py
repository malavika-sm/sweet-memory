import pandas as pd
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

data = pd.read_csv("combined_PMFBY_data.csv")

# Drop rows with missing target values
data = data.dropna(subset=["indemnityLevel"])

target_variable = "indemnityLevel"

# Get all features excluding the target variable
features = [col for col in data.columns if col != target_variable]

X = data[features]
y = data[target_variable]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_regressor = HistGradientBoostingRegressor(random_state=42)
rf_regressor.fit(X_train, y_train)

y_pred = rf_regressor.predict(X_test)

# Evaluate model performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("Mean Squared Error:", mse)
print("R-squared:", r2)

import pickle

filename = 'rf_model.sav'
pickle.dump(rf_regressor, open(filename, 'wb'))