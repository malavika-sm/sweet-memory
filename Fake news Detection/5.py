import tensorflow as tf
from tensorflow.keras.layers import Embedding, LSTM, Bidirectional, Dense # type: ignore

from text_preprocess import preprocesser



X_train, X_test, train_fake_df, train_true_df, test_fake_df, test_true_df = preprocesser()

# Check if preprocessing returned None (indicating errors)
if X_train is None:
    print("Error during preprocessing. Exiting...")
    exit()

# Define hyperparameters (adjust as needed)
max_len = 100  # Maximum sequence length
vocab_size = 500  # Based on TfidfVectorizer parameter

# Embedding layer (adapt based on vocabulary size)
embedding_dim = 128  # Embedding dimension
embedding_layer = Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_len)

# Bi-LSTM layers
lstm_layer = Bidirectional(LSTM(64, return_sequences=True))

# Model definition
model = tf.keras.Sequential([
    embedding_layer,
    lstm_layer,
    Bidirectional(LSTM(32)),
    Dense(1, activation="sigmoid")  # Output layer for binary classification
])

# Compile model
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy", "precision", "recall", "AUC"])

# Access labels from DataFrames (assuming 'label' column)
y_train = train_fake_df['label'].values
y_test = test_fake_df['label'].values

# Train model
model.fit(X_train, y_train, epochs=10)
model.save('model.h5')

# Evaluate model
loss, accuracy = model.evaluate(X_test, y_test)
print("Test Loss:", loss)
print("Test Accuracy:", accuracy)
