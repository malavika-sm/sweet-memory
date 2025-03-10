import cv2
import numpy as np

# Read the segmented conjunctiva image
segmented_conjunctiva = cv2.imread('Segmented3.png')


# Apply morphological operations (dilation or erosion)
kernel = np.ones((5, 5), np.uint8)  # Kernel for morphological operations

# Perform dilation to enhance the detected conjunctiva area
dilated_conjunctiva = cv2.dilate(segmented_conjunctiva, kernel, iterations=1)

# Perform erosion to refine the conjunctiva area
eroded_conjunctiva = cv2.erode(segmented_conjunctiva, kernel, iterations=1)

# Display the original segmented conjunctiva and the morphologically processed versions
cv2.imshow('Segmented Conjunctiva', segmented_conjunctiva)
cv2.imshow('Dilated Conjunctiva', dilated_conjunctiva)
cv2.imshow('Eroded Conjunctiva', eroded_conjunctiva)
cv2.waitKey(0)
cv2.destroyAllWindows()
