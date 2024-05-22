import cv2
import numpy as np
import matplotlib.pyplot as plt

def calculate_energy(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    energy = np.sqrt(grad_x**2 + grad_y**2)
    return energy

def find_seam(energy):
    rows, cols = energy.shape
    seam_energy = energy.copy()
    backtrack = np.zeros_like(seam_energy, dtype=int)

    for i in range(1, rows):
        for j in range(cols):
            if j == 0:
                idx = np.argmin(seam_energy[i-1, j:j+2])
                backtrack[i, j] = idx + j
                min_energy = seam_energy[i-1, idx + j]
            else:
                idx = np.argmin(seam_energy[i-1, j-1:j+2])
                backtrack[i, j] = idx + j - 1
                min_energy = seam_energy[i-1, idx + j - 1]
            seam_energy[i, j] += min_energy

    return seam_energy, backtrack

def remove_seam(image, backtrack):
    rows, cols, _ = image.shape
    mask = np.ones((rows, cols), dtype=bool)
    j = np.argmin(backtrack[-1])
    for i in range(rows-1, -1, -1):
        mask[i, j] = False
        j = backtrack[i, j]

    mask = np.stack([mask]*3, axis=2)
    image = image[mask].reshape((rows, cols-1, 3))
    return image

def seam_carve(image, num_seams):
    for _ in range(num_seams):
        energy = calculate_energy(image)
        seam_energy, backtrack = find_seam(energy)
        image = remove_seam(image, backtrack)
    return image

# Load the image
image = cv2.imread('C:\\Users\\cmcke\\OneDrive\\Desktop\\COS\\personal\\EarthClimateModel_VS\\FlemingsWisp_Gualco_960.jpg')
if image is None:
    raise ValueError("image error")

# Define the number of seams to remove
num_seams = 500

# Perform seam carving
carved_image = seam_carve(image, num_seams)

# Convert the result to RGB for displaying with matplotlib
carved_image_rgb = cv2.cvtColor(carved_image, cv2.COLOR_BGR2RGB)

# Display the original and carved images
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title('Original Image')
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title('Carved Image')
plt.imshow(carved_image_rgb)
plt.axis('off')

plt.show()
