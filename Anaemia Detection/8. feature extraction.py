import cv2
import numpy as np

# Read the image
image = cv2.imread(' Isolated Conjunctiva ROI3.png')  # Replace 'eye_image.jpg' with your image file

# Convert the image from BGR to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Apply Canny edge detection on the entire image
edges = cv2.Canny(image_rgb, 50, 150)  # Adjust the thresholds as needed

# Display the original image and the edges
cv2.imshow('Original Image', image_rgb)
cv2.imshow('Edge Detection', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
