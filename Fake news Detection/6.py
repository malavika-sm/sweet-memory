import tensorflow as tf
from text_preprocess import preprocesser
from tensorflow.keras.preprocessing.text import Tokenizer


X_train, X_test, train_fake_df, train_true_df, test_fake_df, test_true_df = preprocesser()
model = tf.keras.models.load_model('model.h5')  


input_text = ["This is a sample input text to be classified.", "Another input text for classification."]

# Tokenize input text
tokenizer = Tokenizer()

# Fit tokenizer on training text data
all_text = train_fake_df['text'].tolist() + train_true_df['text'].tolist()
tokenizer.fit_on_texts(all_text)

max_len = 100  # Maximum sequence length used in training
input_sequences = tokenizer.texts_to_sequences(input_text)
padded_input_sequences = tf.keras.preprocessing.sequence.pad_sequences(input_sequences, maxlen=max_len)

predictions = model.predict(padded_input_sequences)

# Output predictions
for i, prediction in enumerate(predictions):
    print(f"Input Text: {input_text[i]}")
    print(f"Predicted Probability: {prediction}")
    # Convert probabilities to classes (assuming binary classification)
    predicted_class = 1 if prediction > 0.5 else 0
    print(f"Predicted Class: {predicted_class}")
