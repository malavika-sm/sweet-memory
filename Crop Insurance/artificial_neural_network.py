import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.impute import SimpleImputer
import pickle

data = pd.read_csv("combined_PMFBY_data.csv")

# Define target variable and features
target_variable = "indemnityLevel"
features = [col for col in data.columns if col != target_variable]

# Drop rows with missing target values
data = data.dropna(subset=[target_variable])

# Split data into features and target variable
X = data[features]
y = data[target_variable]

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Impute missing values in training data
imputer = SimpleImputer(strategy='median')
X_train_imputed = imputer.fit_transform(X_train)

# Define the parameter grid for grid search
param_grid = {
    'hidden_layer_sizes': [(50,), (100,), (150,)],
    'activation': ['relu', 'tanh'],
    'solver': ['adam', 'sgd'],
}

# Initialize and perform grid search
grid_search = GridSearchCV(estimator=MLPClassifier(random_state=0), param_grid=param_grid, cv=3)
grid_search.fit(X_train_imputed, y_train)

# Get the best parameters and estimator
best_params = grid_search.best_params_
best_estimator = grid_search.best_estimator_

# Train the model with the best parameters
best_estimator.fit(X_train_imputed, y_train)

# Impute missing values in test data
X_test_imputed = imputer.transform(X_test)

# Make predictions on the test data
y_pred = best_estimator.predict(X_test_imputed)

# Calculate evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')
conf_matrix = confusion_matrix(y_test, y_pred)

# Print evaluation metrics and confusion matrix
print(f"Accuracy of the best ANN model: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-score: {f1:.2f}")
print("Confusion Matrix:")
print(conf_matrix)

# Save the best model
filename = 'best_ann_model.sav'
pickle.dump(best_estimator, open(filename, 'wb'))