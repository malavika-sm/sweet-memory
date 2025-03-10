import cv2
import numpy as np

# Read the image
image = cv2.imread('Sharpened3.png')  # Replace 'eye_image.jpg' with your image file

# Convert the image from BGR to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Define lower and upper bounds for the color range of anterior conjunctiva (adjust these values accordingly)
lower_bound = np.array([150, 100, 100], dtype=np.uint8)
upper_bound = np.array([255, 200, 200], dtype=np.uint8)

# Create a mask to extract the anterior conjunctiva based on color range
mask = cv2.inRange(image_rgb, lower_bound, upper_bound)

# Apply the mask to the original image to extract the anterior conjunctiva
anterior_conjunctiva = cv2.bitwise_and(image_rgb, image_rgb, mask=mask)

# Display the original image and the extracted anterior conjunctiva
cv2.imshow('Original Image', image_rgb)
cv2.imshow('Extracted Anterior Conjunctiva', anterior_conjunctiva)
cv2.waitKey(0)
cv2.destroyAllWindows()
