import cv2
import numpy as np

# Read the image
image = cv2.imread('Dilated3.png')  # Replace 'eye_image.jpg' with your image file

# Convert the image from BGR to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Define the region of interest (ROI) for the anterior conjunctiva
# You can adjust these coordinates to focus on the specific area of interest
x, y, w, h = 100, 150, 200, 100  # Example coordinates for the ROI
roi = image_rgb[y:y + h, x:x + w]

# Calculate the mean color of the ROI
mean_color = np.mean(roi, axis=(0, 1))

# Define thresholds for potential signs of anemia based on color characteristics
anemia_threshold = 100  # Example threshold value for detecting potential signs of anemia

# Check for potential signs of anemia based on mean color values
signs_of_anemia = (mean_color[0] < anemia_threshold) or (mean_color[1] < anemia_threshold) or (mean_color[2] < anemia_threshold)

# Display the mean color and potential signs of anemia
print("Mean Color (R, G, B):", mean_color)

if signs_of_anemia:
    print("Potential signs of anemia detected.")
else:
    print("No significant signs of anemia detected.")

