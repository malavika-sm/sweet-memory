import pandas as pd
import os


def clean(dataset):
    df = pd.read_csv(dataset)

    print("Dataset Info:")
    print(df.info())

    print("\nFirst 5 rows of the dataset:")
    print(df.head())

    # Convert all columns to numeric, coercing errors to NaN
    df = df.apply(pd.to_numeric, errors='coerce')

    # Calculate quartiles (Q1, Q3) for numeric columns only
    numeric_columns = df.select_dtypes(include=['number']).columns
    Q1 = df[numeric_columns].quantile(0.25)
    Q3 = df[numeric_columns].quantile(0.75)
    IQR = Q3 - Q1

    # Check for outliers using IQR (Interquartile Range)
    print("\nOutliers (values outside 1.5 * IQR):")
    outliers = ((df[numeric_columns] < (Q1 - 1.5 * IQR)) | (df[numeric_columns] > (Q3 + 1.5 * IQR))).sum()
    print(outliers[outliers > 0])

    # Handling missing values by filling with median
    df = df.fillna(df.median())

    # Check for inconsistencies (e.g., negative values in numeric columns)
    print("\nInconsistencies (negative values):")
    negative_values = (df[numeric_columns] < 0).sum()
    print(negative_values[negative_values > 0])

    # Handle inconsistencies by setting negative values to NaN and then filling with the median
    for column in negative_values[negative_values > 0].index:
        df.loc[df[column] < 0, column] = pd.NA
    df = df.fillna(df.median())

    print("\nCleaned Dataset Info:")
    print(df.info())

    # Save the cleaned dataset to a new CSV file
    base_name = os.path.splitext(os.path.basename(dataset))[0]
    cleaned_file = f'cleaned_{base_name}.csv'
    df.to_csv(cleaned_file, index=False)
    print("\nCleaned dataset saved to", cleaned_file)

    print(f"\nThe dataset has been cleaned and saved as '{cleaned_file}'.")



def remove_columns(dataset):
    df = pd.read_csv(dataset)
    # Remove all empty columns (all NaN values)
    df = df.dropna(axis=1, how='all')
    df.dropna(inplace=True)

    # Remove columns with same value in all rows
    constant_value_columns = (df.nunique() == 1) | (df.sum() == 0)
    df = df.drop(columns=constant_value_columns.index[constant_value_columns])

    print("Updated Column Names:")
    print(df.columns.tolist())

    # Save the cleaned dataset to a new CSV file
    base_name = os.path.splitext(os.path.basename(dataset))[0]
    cleaned_file = f'{base_name}.csv'
    df.to_csv(cleaned_file, index=False)
    print("\nCleaned dataset saved to", cleaned_file)

    print(f"\nThe dataset has been cleaned and saved as '{cleaned_file}'.")



clean("A:/Datasets/insurance/PMFBY statistics.csv")
clean("A:/Datasets/insurance/PMFBY coverage.csv")

remove_columns('cleaned_PMFBY coverage.csv')
remove_columns('cleaned_PMFBY statistics.csv')