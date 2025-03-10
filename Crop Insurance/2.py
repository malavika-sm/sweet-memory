import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def descriptive_analysis(df, key_variables):
    # Calculate summary statistics
    summary_stats = df[key_variables].describe()
    print("Summary Statistics:\n", summary_stats)

    # Visualize distributions using histograms
    for variable in key_variables:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[variable], kde=True)
        plt.title(f'Histogram of {variable}')
        plt.xlabel(variable)
        plt.ylabel('Frequency')
        plt.show()

    # Visualize distributions using box plots
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df[key_variables])
    plt.title('Box plot of key variables')
    plt.show()

    # Explore temporal trends if 'year' column exists
    if 'year' in df.columns:
        for variable in key_variables:
            if variable != 'year':                              # Avoid plotting 'year' on y-axis
                plt.figure(figsize=(10, 6))
                sns.lineplot(x='year', y=variable, data=df)
                plt.title(f'Annual Trend of {variable}')
                plt.xlabel('Year')
                plt.ylabel(variable)
                plt.show()


def analyze(dataset):
    df = pd.read_csv(dataset)
    # Get the column names dynamically, excluding non-numeric columns for figures
    selected_columns = df.select_dtypes(include=['number']).columns.tolist()

    print("Descriptive Analysis for Numeric Columns in PMFBY Coverage Dataset:")
    descriptive_analysis(df, selected_columns)


analyze('cleaned_PMFBY coverage.csv')
analyze('cleaned_PMFBY statistics.csv')