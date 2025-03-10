import os
import pandas as pd
from sklearn.model_selection import train_test_split


dataset_dir = "A:\Datasets\news"
combined_data = pd.DataFrame()      # Dictionary

for subdir, dirs, files in os.walk(dataset_dir):
    for file_name in files:
        file_path = os.path.join(subdir, file_name)
        
        df = pd.read_csv(file_path, encoding='latin1') 
        
        combined_data = pd.concat([combined_data, df], ignore_index=True)

train_data, test_data = train_test_split(combined_data, test_size=0.2, random_state=42)

train_fake = train_data[train_data['label'] == 0]
train_true = train_data[train_data['label'] == 1]
test_fake = test_data[test_data['label'] == 0]
test_true = test_data[test_data['label'] == 1]

# Create new directory structure at the same level as the source directory
parent_dir = os.path.dirname(dataset_dir)
new_dataset_dir = os.path.join(parent_dir, 'new_news')
os.makedirs(new_dataset_dir, exist_ok=True)

# Save training and test datasets
train_data.to_csv(os.path.join(new_dataset_dir, 'train.csv'), index=False)
test_data.to_csv(os.path.join(new_dataset_dir, 'test.csv'), index=False)

# Save separate datasets for fake and true news
train_fake.to_csv(os.path.join(new_dataset_dir, 'train_fake.csv'), index=False)
train_true.to_csv(os.path.join(new_dataset_dir, 'train_true.csv'), index=False)
test_fake.to_csv(os.path.join(new_dataset_dir, 'test_fake.csv'), index=False)
test_true.to_csv(os.path.join(new_dataset_dir, 'test_true.csv'), index=False)
