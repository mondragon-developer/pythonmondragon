from PIL import Image
import os

# Function to resize images in the specified directory
def resize_images(input_dir, output_dir, size):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create the output directory if it doesn't exist
    for filename in os.listdir(input_dir):
        # Check if the file is an image based on its extension
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            with Image.open(os.path.join(input_dir, filename)) as img:
                img = img.resize(size, Image.LANCZOS)  # Resize the image to the specified size
                img.save(os.path.join(output_dir, filename))  # Save the resized image
                print(f"Resized and saved: {filename}")

if __name__ == "__main__":
    input_dir = "input_images"  
    output_dir = "resized_images"  
    size = (800, 400)  # Target size for resizing (width, height)
    resize_images(input_dir, output_dir, size)  # Call the function to resize images
    print("All images have been resized!") 
