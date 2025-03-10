import os
import pandas as pd


dataset_dir = "A:/Datasets/new_news"
modified_dataframes = {}  # Dictionary 

# Loop through all files in the dataset directory and its subdirectories
for subdir, dirs, files in os.walk(dataset_dir):
    for file_name in files:
        file_path = os.path.join(subdir, file_name)
        df = pd.read_csv(file_path, encoding='latin1')
        
        # Check conditions to modify the DataFrame
        if ('ifnd-dataset' in subdir and file_name == 'IFND.csv') or ('1' in subdir and file_name == 'train.csv'):
            if 'id' in df.columns:  
                df.drop(columns=['id'], inplace=True)  # Remove 'id' column
                df.to_csv(file_path, index=False)  # Save modified DataFrame back to the same file
        
        modified_dataframes[file_name] = df        # Add modified DataFrame to dictionary

# Verification
for file_name, df in modified_dataframes.items():
    print(f"\n{file_name}:")
    print(df.head())
