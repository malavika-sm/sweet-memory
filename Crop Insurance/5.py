import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv("combined_PMFBY_data.csv")

# Group data by crop type and calculate average indemnity level
average_indemnity = data.groupby('cropTypeCode')['indemnityLevel'].mean().reset_index()

# Create bar chart
plt.figure(figsize=(10, 6))
plt.bar(average_indemnity['cropTypeCode'], average_indemnity['indemnityLevel'])
plt.xlabel('Crop Type')
plt.ylabel('Average Indemnity Level')
plt.title('Average Indemnity Level by Crop Type')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Display the chart
plt.show()


import pickle

# Load the trained model
model = pickle.load(open('rf_model.sav', 'rb'))

# Read user input for crop code
crop_code = input("Enter the crop code: ")

# Create a DataFrame with the user input
user_input_df = pd.DataFrame({"cropCode": [crop_code]})

# Perform prediction
predicted_indemnity_level = model.predict(user_input_df)

# Print the predicted indemnity level
print(f"Predicted indemnity level for crop code '{crop_code}': {int(predicted_indemnity_level[0])}")
