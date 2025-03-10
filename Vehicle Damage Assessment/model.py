import os
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np


def split_data(train_path, val_path, image_height, image_width, channels, batch_size):
    # Train data generator with augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )
    train_generator = train_datagen.flow_from_directory(
        train_path,
        target_size=(image_height, image_width),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=True
    )

    # Validation data generator without augmentation
    val_datagen = ImageDataGenerator(rescale=1./255)
    val_generator = val_datagen.flow_from_directory(
        val_path,
        target_size=(image_height, image_width),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )

    return train_generator, val_generator


def create_cnn_model(input_shape, num_classes):
    # Model architecture
    model = tf.keras.Sequential([
        Input(shape=input_shape),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(256, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def train_and_evaluate_model(model, train_generator, val_generator, epochs):
    # Train the model
    history = model.fit(train_generator, epochs=epochs, validation_data=val_generator)

    # Evaluate the model
    val_loss, val_accuracy = model.evaluate(val_generator)
    print(f"Validation Loss: {val_loss}, Validation Accuracy: {val_accuracy}")

    # Confusion Matrix
    val_predictions = np.argmax(model.predict(val_generator), axis=-1)
    val_true_labels = val_generator.classes
    cm = confusion_matrix(val_true_labels, val_predictions)

    # Plot Confusion Matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=val_generator.class_indices, yticklabels=val_generator.class_indices)
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.title('Confusion Matrix')
    plt.show()

    # Save the model
    model.save('cnn_model_updated.h5')
    return history


# Define data directories
base_data_dir = "A:/Datasets/vehicle"  
train_path = os.path.join(base_data_dir, 'train')
val_path = os.path.join(base_data_dir, 'test') 

# Check if directories exist
if not os.path.exists(train_path) or not os.path.exists(val_path):
    raise ValueError("Training or validation data directory not found.")

# Define image dimensions and batch size
image_height, image_width, channels = 224, 224, 3
batch_size = 32

# Split data and create data generators
train_generator, val_generator = split_data(train_path, val_path, image_height, image_width, channels, batch_size)

num_classes = 7  # 7 classes for damage types
model = create_cnn_model(input_shape=(image_height, image_width, channels), num_classes=num_classes)

# Train and evaluate the model
epochs = 20  # Adjust as needed
history = train_and_evaluate_model(model, train_generator, val_generator, epochs)

# Plot training history
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
