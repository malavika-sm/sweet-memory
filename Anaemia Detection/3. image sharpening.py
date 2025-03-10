import cv2
import numpy as np

# Read the eye image
eye_image = cv2.imread('Denoised3.png')

# Create a sharpening kernel
kernel = np.array([[-1, -1, -1],
                   [-1, 9, -1],
                   [-1, -1, -1]])

# Apply the kernel to perform sharpening
sharpened_eye = cv2.filter2D(eye_image, -1, kernel)
# Display the original and sharpened images
cv2.imshow('Original Eye', eye_image)
cv2.imshow('Sharpened Eye', sharpened_eye)
cv2.waitKey(0)
cv2.destroyAllWindows()
