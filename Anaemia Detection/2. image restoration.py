import cv2
import numpy as np

# Read the damaged eye image
damaged_eye = cv2.imread('Enhanced3.png')

# Apply denoising
denoised_eye = cv2.fastNlMeansDenoisingColored(damaged_eye, None, h=10, hColor=10, templateWindowSize=7, searchWindowSize=21)

# Create a mask for inpainting
mask = np.zeros(damaged_eye.shape[:2], np.uint8)
radius = 50
center = (150, 150)
cv2.circle(mask, center, radius, 255, -1)

# Apply inpainting to restore damaged parts
restored_eye = cv2.inpaint(damaged_eye, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

# Display the original, denoised, and restored images
cv2.imshow('Enhanced Eye', damaged_eye)
cv2.imshow('Denoised Eye', denoised_eye)
cv2.imshow('Restored Eye', restored_eye)
cv2.waitKey(0)
cv2.destroyAllWindows()
