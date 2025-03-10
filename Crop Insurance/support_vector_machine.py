import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np
import pickle

# Read the data
data = pd.read_csv("combined_PMFBY_data.csv")

target_variable = "indemnityLevel"
features = [col for col in data.columns if col != target_variable]

X = data[features]
y = data[target_variable]

# Check for missing values in y
if y.isnull().any():
    print("Target variable 'y' contains missing values. Dropping corresponding rows.")
    missing_index = np.where(y.isnull())[0]
    X = X.drop(index=missing_index)
    y = y.dropna()

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Impute missing values in features using the median of each feature
imputer = SimpleImputer(strategy='median')
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

# Scale features to have zero mean and unit variance
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imputed)
X_test_scaled = scaler.transform(X_test_imputed)

# Create SVC model
svc_model = SVC(kernel='rbf')

# Train the SVC model on the training data
svc_model.fit(X_train_scaled, y_train)

# Make predictions on the test data
y_pred = svc_model.predict(X_test_scaled)


# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy of the SVC model: {accuracy:.2f}")

# Calculate precision
precision = precision_score(y_test, y_pred, average='weighted')
print(f"Precision: {precision:.2f}")

# Calculate recall
recall = recall_score(y_test, y_pred, average='weighted')
print(f"Recall: {recall:.2f}")

# Calculate F1-score
f1 = f1_score(y_test, y_pred, average='weighted')
print(f"F1-score: {f1:.2f}")

# Calculate confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(conf_matrix)

# Save the model
filename = 'svm_model.sav'
pickle.dump(svc_model, open(filename, 'wb'))