import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from textblob import TextBlob
import spacy


def preprocesser(text):
    # Check if the input is NaN
    if pd.isna(text):
        return ""
    text = text.lower()  # Convert text to lowercase
    text = " ".join(text.split())  # Remove extra whitespaces
    return text

# Load the datasets
train_fake = pd.read_csv("A:/Datasets/new_news/train_fake.csv")
train_true = pd.read_csv("A:/Datasets/new_news/train_true.csv")
test_fake = pd.read_csv("A:/Datasets/new_news/test_fake.csv")
test_true = pd.read_csv("A:/Datasets/new_news/test_true.csv")

# Combine the train and test data for preprocessing
train_data = pd.concat([train_fake, train_true], ignore_index=True)
test_data = pd.concat([test_fake, test_true], ignore_index=True)

text_data = train_data['text'].tolist() + test_data['text'].tolist()

processed_text_data = [preprocesser(text) for text in text_data]

# Bag-of-Words (BoW) representation
vectorizer = CountVectorizer()
bow_matrix = vectorizer.fit_transform(processed_text_data)

top_features_indices = np.argsort(bow_matrix.sum(axis=0))[-5:]  # Get indices of top 5 words
top_features = vectorizer.get_feature_names_out()[top_features_indices]

# Sum along the axis=0 of the BoW matrix
bow_sum = bow_matrix.sum(axis=0)
top_feature_counts = bow_sum[0, top_features_indices]

# Convert arrays to lists
top_features_list = top_features.tolist()
top_feature_counts_list = top_feature_counts.tolist()
df_top_features = pd.DataFrame({'word': top_features_list, 'count': top_feature_counts_list})
print(df_top_features)


# TF-IDF representation
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(processed_text_data)
print("\nTF-IDF matrix:")
tfidf_df = pd.DataFrame.sparse.from_spmatrix(tfidf_matrix, columns=tfidf_vectorizer.get_feature_names_out())
print(tfidf_df.head())

# Sentiment analysis
sentiment_scores = []
for text in text_data:
    if isinstance(text, str):  # Check if the element is a string
        sentiment_score = TextBlob(text).sentiment.polarity
        sentiment_scores.append(sentiment_score)
    else:
        sentiment_scores.append(None)  # for non-string elements

print("Sentiment scores:")
print(sentiment_scores)

# Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")
for text in text_data:
    if not isinstance(text, str):
        print("Non-string element found in text_data:", text)
try:
    ner_tags = [[(ent.text, ent.label_) for ent in nlp(text).ents] for text in text_data]
    print("\nNamed Entity Recognition (NER) tags:")
    print(ner_tags)
except Exception as e:
    print("Error processing text data with spaCy:", e)
