from PIL import Image, ImageDraw

# Create a simple, balanced player icon (e.g., a spaceship-like shape)
player_size = 64  # 64x64 pixels
player_icon = Image.new('RGBA', (player_size, player_size), (0, 0, 0, 0))

# Draw a symmetric triangle to represent a spaceship
draw = ImageDraw.Draw(player_icon)
player_shape = [(32, 0), (0, 64), (64, 64)]  # Symmetric triangle
draw.polygon(player_shape, fill=(0, 255, 0, 255))  # Green color for the player

# Save the corrected player image as 'player_corrected.png'
player_icon_path = "player.png"
player_icon.save(player_icon_path, "PNG")

# Provide the path for download
player_icon_path

