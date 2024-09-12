import cv2
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np

# Path to the folder containing images
input_folder = 'data/source'
output_folder = 'data/modified'

# Create output folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define the multiline watermark text
new_watermark_text = "Permission for publication of this image must be secured from the Research Centre for the East European Studies,\nUniversity of Bremen (Forschungsstelle Osteuropa an der Universität Bremen) at archiv.fso@uni-bremen.de"

# Path to the default font on macOS, replace with the font you choose
font_path = "/System/Library/Fonts/Helvetica.ttc"  # Example with Helvetica
font_size = 25  # Adjust based on image size
line_height = 7

# Loop through each image in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.jpg') or filename.endswith('.jp2'):  # Add other formats if needed
        # Load the image using OpenCV
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)
        
        # Convert the image to RGB format for PIL
        image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(image_pil)

        # Set font
        font = ImageFont.truetype(font_path, font_size)

        # Calculate the size of each line and total height for multiline text
        lines = new_watermark_text.split('\n')
        line_sizes = [draw.textbbox((0, 0), line, font=font) for line in lines]
        max_width = max(size[2] - size[0] for size in line_sizes)
        total_height = sum(size[3] - size[1] for size in line_sizes) + line_height * (len(lines) - 1)

        # Calculate the starting position for the watermark text at the bottom of the image
        padding = 10  # Padding around the text
        box_start_x = 0  # Start at the left edge of the image
        box_end_x = image_pil.width  # Extend to the right edge of the image
        box_end_y = image_pil.height  # Bottom edge of the image
        box_start_y = box_end_y - total_height - padding * 2  # Calculate top edge of the box

        # Draw the white background rectangle
        draw.rectangle([box_start_x, box_start_y, box_end_x, box_end_y], fill=(255, 255, 255))  # White background color

        # Draw each line of text
        y = box_start_y + padding
        for line in lines:
            line_width = draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0]
            x = (image_pil.width - line_width) / 2  # Center align text
            draw.text((x, y), line, (0, 0, 0), font=font)  # Black text; change color if needed
            y += draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] + line_height  # Move to the next line with additional line height

        # Save the modified image
        modified_image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, modified_image)

print("Watermark text alteration completed.")