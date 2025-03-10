import cv2
import numpy as np
import tensorflow as tf
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont


def predict_and_get_roi(image_path, model):
    """
    Predicts damage severity, type, and extracts ROI from an image.

    Args:
        image_path (str): Path to the image file.
        model (keras.Model): The trained CNN model.

    Returns:
        tuple: A tuple containing the predicted damage severity (str), type of damage (str), and ROI (bounding box or mask).
    """
    # Load and preprocess the image
    image = cv2.imread(image_path)
    print("Image size:", image.shape)
    if image is None or image.size == 0:
        print("Error: The source image is empty.")
        return None, None, None

    # Resize and normalize image
    resized_image = cv2.resize(image, (224, 224))
    normalized_image = resized_image / 255.0

    # Predict damage severity and type
    predicted_probs = model.predict(np.expand_dims(normalized_image, axis=0))
    print("Predicted probabilities:", predicted_probs) 
    print("Shape of predicted_probs:", predicted_probs.shape)

    # Extract predicted severity (mild or severe)
    severity_class_index = np.argmax(predicted_probs[0, :3])
    severity_classes = ["severe", "medium", "mild"]
    predicted_severity = severity_classes[severity_class_index]
    print("Predicted severity:", predicted_severity)

    # Extract predicted damage type (crack, dent, etc.)
    damage_probs = predicted_probs[0, 2:]
    damage_class_index = np.argmax(damage_probs)
    damage_classes = ["crack", "dent", "glass shatter", "lamp broken", "mud", "scratch", "tire flat"]
    predicted_damage_type = damage_classes[damage_class_index]
    print("Predicted damage type:", predicted_damage_type)

    # Extract ROI using contours (assuming binary mask output) assuming channel 1 corresponds to the mask
    binary_mask = None

    if binary_mask is not None:
        # Threshold the mask using Otsu's method
        _, binary_mask = cv2.threshold(binary_mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Find contours
        contours, _ = cv2.findContours(binary_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # Get the bounding box coordinates for the largest contour
            x, y, w, h = cv2.boundingRect(contours[0])
            roi_bbox = (x, y, w, h)
        else:
            roi_bbox = None
    else:
        roi_bbox = None

    return predicted_severity, predicted_damage_type, roi_bbox


def handle_upload():
    file_path = filedialog.askopenfilename()
    if file_path:
        predicted_class, predicted_damage_type, roi = predict_and_get_roi(file_path, model)
        if predicted_class is not None:
            image = cv2.imread(file_path)
            if roi:
                roi_x, roi_y, roi_width, roi_height = map(int, roi)
                roi_x_scaled = int(roi_x * 800 / image.shape[1])  # Scale ROI coordinates to match resized image
                roi_y_scaled = int(roi_y * 600 / image.shape[0])
                roi_width_scaled = int(roi_width * 800 / image.shape[1])
                roi_height_scaled = int(roi_height * 600 / image.shape[0])
                cv2.rectangle(image, (roi_x_scaled, roi_y_scaled), (roi_x_scaled + roi_width_scaled, roi_y_scaled + roi_height_scaled), (255, 0, 0), 2)

            # Resize the image to a fixed size
            image = cv2.resize(image, (800, 600))  # Adjust width and height as needed

            # Convert the image to RGB format for displaying in Tkinter
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_rgb)

            # Draw the predicted class (severity and damage type) on top of the image
            predicted_text = f"Predicted Class: {predicted_class}, Damage Type: {predicted_damage_type}"
            draw = ImageDraw.Draw(image_pil)
            draw.text((10, 10), predicted_text, fill=(0, 255, 0), font=ImageFont.truetype("arial.ttf", 16))

            # Convert the image back to BGR format for OpenCV operations
            image_with_text = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

            # Display the image with predicted class in the Tkinter label
            image_tk = ImageTk.PhotoImage(image=Image.fromarray(image_with_text))
            label.config(image=image_tk)
            label.image = image_tk

            # Resize window to fit the image
            window.geometry(f"{image_pil.width}x{image_pil.height}")


# Load the trained model
model = tf.keras.models.load_model('cnn_model_updated.h5')

# Create a Tkinter window
window = tk.Tk()
window.title("Image Upload")

# Create a button for uploading an image
upload_button = tk.Button(window, text="Upload Image", command=handle_upload)
upload_button.pack()

# Create a label to display the image
label = tk.Label(window)
label.pack()

# Start the Tkinter event loop
window.mainloop()
