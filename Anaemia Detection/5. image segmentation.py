import cv2
import numpy as np
from sklearn.cluster import KMeans
def kmeans_segmentation(image_path, num_clusters, window_size):
# Read the image
    img = cv2.imread(image_path)
    # Reshape the image to a 2D array of pixels
    pixels = img.reshape((-1, 3))
    # Convert the data type to float32
    pixels = np.float32(pixels)
    # Set a random seed for reproducibility
    np.random.seed(42)
    # Apply K-means clustering
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(pixels)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_
    # Convert back to 8-bit values
    centers = np.uint8(centers)
    # Map the labels to the centers
    segmented_img = centers[labels.flatten()]
    # Reshape the segmented image to the original shape
    segmented_img = segmented_img.reshape(img.shape)
    # Resize the windows to a smaller size
    cv2.namedWindow('Original Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Original Image', window_size[0], window_size[1])
    cv2.namedWindow('Segmented Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Segmented Image', window_size[0], window_size[1])
    # Display the original image labeled by cluster index
    cv2.imshow('Original Image', img)
    cv2.imshow('Segmented Image', segmented_img)
    # Display separate images for each cluster
    for i in range(num_clusters):
        cluster_mask = np.zeros_like(labels, dtype=np.uint8)
        cluster_mask[labels.flatten() == i] = 255
        cluster_objects = cv2.bitwise_and(img, img,
        mask=cluster_mask.reshape(img.shape[:2]))
        cv2.namedWindow(f'Objects in Cluster {i}', cv2.WINDOW_NORMAL)
        cv2.resizeWindow(f'Objects in Cluster {i}', window_size[0],window_size[1])
        cv2.imshow(f'Objects in Cluster {i}', cluster_objects)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
        # Replace 'your_image_path.jpg' with the path to the image you want tosegment
image_path = 'Extracted Anterior Conjunctiva3.png'
num_clusters = 3 # You can adjust the number of clusters based on yourneeds
window_size = (400, 300) # Adjust the window size as needed
kmeans_segmentation(image_path, num_clusters, window_size)
