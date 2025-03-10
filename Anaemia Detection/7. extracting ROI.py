import cv2
import numpy as np

# Read the eye image
eye_image = cv2.imread('Dilated3.png')

# Convert BGR to HSV
hsv = cv2.cvtColor(eye_image, cv2.COLOR_BGR2HSV)

# Define range of conjunctiva color in HSV (may vary based on anemia detection criteria)
# Example values; adjust as needed
lower_conjunctiva = np.array([0, 20, 100])  # Define the lower bound of conjunctiva color
upper_conjunctiva = np.array([20, 150, 255])  # Define the upper bound of conjunctiva color

# Threshold the HSV image to get only conjunctiva colors
mask = cv2.inRange(hsv, lower_conjunctiva, upper_conjunctiva)

# Apply the mask to the original image to isolate the conjunctiva region
conjunctiva_roi = cv2.bitwise_and(eye_image, eye_image, mask=mask)

# Display the isolated conjunctiva region
cv2.imshow('Isolated Conjunctiva ROI', conjunctiva_roi)
cv2.waitKey(0)
cv2.destroyAllWindows()
