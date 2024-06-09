from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np

# Load the image using Pillow
img_path = "gitcodesInverted.jpeg"
img = Image.open(img_path)

# Convert the image to grayscale
img = img.convert("L")

# Enhance the contrast
contrast_enhancer = ImageEnhance.Contrast(img)
img_enhanced = contrast_enhancer.enhance(2)  # Increase contrast by 2 times

# Convert the image to a format suitable for OpenCV
img_cv = np.array(img_enhanced)

# Use GaussianBlur to reduce noise
blurred = cv2.GaussianBlur(img_cv, (3, 3), 0)

# Use adaptive thresholding to sharpen the image
sharpened = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# Convert back to PIL Image for further enhancement
img_sharpened = Image.fromarray(sharpened)

# Further enhance sharpness using Pillow
sharpness_enhancer = ImageEnhance.Sharpness(img_sharpened)
img_final = sharpness_enhancer.enhance(2)  # Increase sharpness by 2 times

# Save the enhanced image
enhanced_img_path = "gitcodesEnhancedFinal.jpeg"
img_final.save(enhanced_img_path)

print(f"Enhanced image saved to {enhanced_img_path}")