from PIL import Image, ImageDraw

# Create a simple enemy icon (e.g., a red UFO-like shape) for the game
enemy_size = 64  # 64x64 pixels
enemy_icon = Image.new('RGBA', (enemy_size, enemy_size), (0, 0, 0, 0))

# Draw a UFO-like shape for the enemy
draw = ImageDraw.Draw(enemy_icon)
enemy_shape_top = [(16, 16), (48, 16), (32, 0)]  # Top triangle
draw.polygon(enemy_shape_top, fill=(255, 0, 0, 255))  # Red color for the top
enemy_shape_bottom = [(0, 32), (64, 32), (48, 48), (16, 48)]  # Bottom arc
draw.polygon(enemy_shape_bottom, fill=(255, 0, 0, 255))  # Red color for the bottom

# Save the enemy image as 'enemy.png'
enemy_icon_path = "enemy.png"
enemy_icon.save(enemy_icon_path, "PNG")

# Provide the generated enemy image file path
enemy_icon_path

