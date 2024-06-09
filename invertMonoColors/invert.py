from PIL import Image, ImageOps

# Open the image file to invert
with Image.open("gitcodes.jpeg") as img:
    # Invert image colors
    inverted_image = ImageOps.invert(img.convert("RGB"))
    # Save the new inverted image
    inverted_image.save("gitcodesInverted.jpeg")