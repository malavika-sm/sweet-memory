import os
import pandas as pd
from sklearn.impute import SimpleImputer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer


def preprocesser():
    """
    Reads fake and true news data, preprocesses them, and returns separate dataframes.

    - Handles potential errors (missing files, missing columns)
    - Provides informative messages during preprocessing steps.
    - Returns separate dataframes for training and testing to avoid contamination.
    - Considers alternative approaches for missing value handling (e.g., imputation)
    """

    dataset_dir = "A:/Datasets/new_news"

    # Check if the dataset directory exists
    if not os.path.exists(dataset_dir):
        print(f"Error: The dataset directory {dataset_dir} does not exist.")
        return None, None, None, None, None, None

    try:
        dataset_files = os.listdir(dataset_dir)
    except Exception as e:
        print(f"Error: Unable to list files in the dataset directory. {e}")
        return None, None, None, None, None, None

    df = {}

    # Load each dataset into a DataFrame
    for file in dataset_files:
        dataset_name = os.path.splitext(file)[0]  # Extract the dataset name from the file name
        try:
            df[dataset_name] = pd.read_csv(os.path.join(dataset_dir, file), encoding='latin1')
        except Exception as e:
            print(f"Error: Unable to load {file}. {e}")
            return None, None, None, None, None, None

    # Check for missing columns (text and label)
    for key in ['train_fake', 'train_true', 'test_fake', 'test_true']:
        if 'text' not in df[key].columns or 'label' not in df[key].columns:
            print(f"Error: 'text' or 'label' column missing in {key} data.")
            return None, None, None, None, None, None

    print('Loading data...')

    # Concatenate text data for preprocessing (separate for training and testing)
    train_text = df['train_fake']['text'].copy()
    test_text = df['test_fake']['text'].copy()

    # Handle missing values using constant imputation
    print('Handling missing values...')
    imputer = SimpleImputer(strategy='constant', fill_value='missing')
    train_text = imputer.fit_transform(train_text.values.reshape(-1, 1))
    test_text = imputer.transform(test_text.values.reshape(-1, 1))

    # Preprocessing text data
    print('Preprocessing text data...')
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    
    train_text_processed = []
    for text in train_text.ravel():
        tokens = word_tokenize(text.lower())
        tokens = [word for word in tokens if word not in stop_words]
        tokens = [stemmer.stem(word) for word in tokens]
        train_text_processed.append(' '.join(tokens))

    test_text_processed = []
    for text in test_text.ravel():
        tokens = word_tokenize(text.lower())
        tokens = [word for word in tokens if word not in stop_words]
        tokens = [stemmer.stem(word) for word in tokens]
        test_text_processed.append(' '.join(tokens))

    # Vectorization (using TfidfVectorizer for better weighting)
    print('Vectorizing text data...')
    vectorizer = TfidfVectorizer(max_features=5000, min_df=5, max_df=0.7)
    X_train = vectorizer.fit_transform(train_text_processed)
    X_test = vectorizer.transform(test_text_processed)

    return X_train, X_test, df['train_fake'], df['train_true'], df['test_fake'], df['test_true']

