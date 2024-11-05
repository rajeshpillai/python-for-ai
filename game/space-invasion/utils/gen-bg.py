from PIL import Image, ImageDraw
import random

# Create an 800x600 black canvas
width, height = 800, 600
background = Image.new('RGB', (width, height), (0, 0, 0))

# Draw random stars
draw = ImageDraw.Draw(background)
for _ in range(200):  # Number of stars
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)
    radius = random.randint(1, 3)  # Random star size
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(255, 255, 255))

# Save the image as 'background.jpg'
background_path = "background.jpg"
background.save(background_path)

# Provide the generated image path
background_path

