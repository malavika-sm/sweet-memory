import pandas as pd

# Read the cleaned datasets
coverage_data = pd.read_csv("cleaned_PMFBY coverage.csv")
statistics_data = pd.read_csv("cleaned_PMFBY statistics.csv")

# Combine the datasets along rows
combined_data = pd.concat([coverage_data, statistics_data], ignore_index=True)

# Save the combined dataset
combined_data.to_csv("combined_PMFBY_data.csv", index=False)

print("Combined dataset saved as 'combined_PMFBY_data.csv'")
