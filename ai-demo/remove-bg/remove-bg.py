import os
from rembg import remove
from PIL import Image
import io

# Load the input image
script_dir = os.path.dirname(os.path.abspath(__file__))

print (script_dir)

# Define the model path relative to the script directory
model_path = os.path.join(script_dir, "images")

input_path =  model_path + '/image-input-1.jpg'  # Replace with your image path
output_path = model_path + '/image-input-1.output.png'  # Output path for the image with removed background

# Open the image file
with open(input_path, 'rb') as input_file:
    input_image = input_file.read()

# Remove the background
output_image = remove(input_image)

# Save the output image
with open(output_path, 'wb') as output_file:
    output_file.write(output_image)

print(f"Background removed! Saved as {output_path}")
