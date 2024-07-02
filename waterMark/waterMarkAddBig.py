from PIL import Image, ImageDraw, ImageFont
import os
import math

# Define configurations at the beginning
base_path = os.path.dirname(os.path.abspath(__file__))
original_image_path = os.path.join(base_path, 'original_image.png')
big_output_image_path = os.path.join(base_path, 'big_output_image.png')
watermark_text = 'Watermark'
font_path = os.path.join(base_path, 'arial.ttf')
font_size = 100  # Increased font size
opacity = 128  # Adjust this value (0-255) to change the opacity of the watermark

def add_watermark(original_image_path, big_output_image_path, text, font_path, font_size, opacity):
    # Open the original image
    original = Image.open(original_image_path).convert('RGBA')
    
    # Create a transparent overlay the same size as the original image
    overlay = Image.new('RGBA', original.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Specify the font
    font = ImageFont.truetype(font_path, font_size)
    
    # Get the size of the text
    text_bbox = draw.textbbox((0, 0), text, font=font)
    textwidth = text_bbox[2] - text_bbox[0]
    textheight = text_bbox[3] - text_bbox[1]
    
    # Calculate how many times to repeat the text
    rows = math.ceil(original.size[1] / textheight) + 1
    cols = math.ceil(original.size[0] / textwidth) + 1
    
    # Draw the text multiple times
    for row in range(rows):
        for col in range(cols):
            x = col * textwidth - (textwidth / 2)
            y = row * textheight - (textheight / 2)
            draw.text((x, y), text, font=font, fill=(232, 232, 232, opacity))
    
    # Rotate the overlay
    overlay = overlay.rotate(45, expand=True)
    
    # Resize the overlay to match the original image size
    overlay = overlay.resize(original.size, Image.LANCZOS)
    
    # Ensure both images are in RGBA mode
    original = original.convert('RGBA')
    overlay = overlay.convert('RGBA')
    
    # Perform alpha composite
    result = Image.alpha_composite(original, overlay)
    
    # Convert back to RGB and save
    result.convert('RGB').save(big_output_image_path)

# Example usage
add_watermark(original_image_path, big_output_image_path, watermark_text, font_path, font_size, opacity)