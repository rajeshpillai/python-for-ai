from PIL import Image, ImageDraw

# Create a simple icon (e.g., a spaceship-like triangle) for the game
icon_size = 64  # 64x64 pixels
icon = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))

# Draw a triangle to represent a spaceship
draw = ImageDraw.Draw(icon)
triangle_points = [(32, 0), (0, 64), (64, 64)]
draw.polygon(triangle_points, fill=(255, 255, 255, 255))

# Save the icon as 'icon.png'
icon_path = "icon.png"
icon.save(icon_path, "PNG")

# Provide the generated icon file path
icon_path

