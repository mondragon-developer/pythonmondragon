from PIL import Image, ImageDraw, ImageFont
import os

# Define configurations at the beginning
base_path = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
original_image_path = os.path.join(base_path, 'original_image.png')
output_image_path = os.path.join(base_path, 'output_image.png')
watermark_text = 'Watermark'
font_path = os.path.join(base_path, 'arial.ttf')  # Ensure this font file is available in the watermark directory
font_size = 50
margin = 10

def add_watermark(input_image_path, output_image_path, text, font_path, font_size, margin):
    # Open the original image
    original = Image.open(original_image_path)
    
    # Get an ImageDraw object so we can draw on the image
    draw = ImageDraw.Draw(original)
    
    # Specify the font and size
    font = ImageFont.truetype(font_path, font_size)
    
    # Get the size of the text to be added as watermark
    text_bbox = draw.textbbox((0, 0), text, font=font)
    textwidth = text_bbox[2] - text_bbox[0]
    textheight = text_bbox[3] - text_bbox[1]

    # Calculate the position to place the text at the bottom right
    width, height = original.size
    x = width - textwidth - margin
    y = height - textheight - margin
    
    # Draw the text on the original image
    draw.text((x, y), text, font=font, fill=(232,232,232))  # White text with transparency
    
    # Save the result
    original.save(output_image_path)

# Example usage
add_watermark(original_image_path, output_image_path, watermark_text, font_path, font_size, margin)


