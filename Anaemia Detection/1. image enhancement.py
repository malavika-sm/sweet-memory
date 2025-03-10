import cv2
import numpy as np

def enhance_eye(image):
    # Convert the image to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    # Split the LAB image into channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) on the L channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    
    # Merge the enhanced L channel with the original A and B channels
    enhanced_lab = cv2.merge((cl, a, b))
    
    # Convert the LAB image back to BGR color space
    enhanced_image = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    return enhanced_image

# Read the eye image
input_image = cv2.imread('3.jpg')  # Replace 'eye_image.jpg' with your image path

# Apply enhancement
enhanced_eye = enhance_eye(input_image)

# Display the original and enhanced images
cv2.imshow('Original Eye', input_image)
cv2.imshow('Enhanced Eye', enhanced_eye)
cv2.waitKey(0)
cv2.destroyAllWindows()
