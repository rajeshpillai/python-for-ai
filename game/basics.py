import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Coordinate Scale")

# Font for text
font = pygame.font.Font(None, 24)

# Function to draw the coordinate scales
def draw_scales():
    # Draw x-axis scale (top)
    for x in range(0, SCREEN_WIDTH, 50):
        pygame.draw.line(screen, GREEN, (x, 0), (x, 10), 1)  # Small vertical tick
        coord_text = font.render(str(x), True, GREEN)
        screen.blit(coord_text, (x + 2, 12))  # Offset text slightly below the line

    # Draw y-axis scale (left)
    for y in range(0, SCREEN_HEIGHT, 50):
        pygame.draw.line(screen, GREEN, (0, y), (10, y), 1)  # Small horizontal tick
        coord_text = font.render(str(y), True, GREEN)
        screen.blit(coord_text, (12, y - 8))  # Offset text slightly to the right of the line

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw coordinate scales
    draw_scales()

    # Get mouse position and draw coordinates
    mouse_pos = pygame.mouse.get_pos()
    coord_text = font.render(f"x: {mouse_pos[0]}, y: {mouse_pos[1]}", True, GREEN)
    screen.blit(coord_text, (mouse_pos[0] + 10, mouse_pos[1] - 20))  # Text near mouse

    # Draw a crosshair at the mouse position
    pygame.draw.line(screen, GREEN, (mouse_pos[0] - 10, mouse_pos[1]), (mouse_pos[0] + 10, mouse_pos[1]), 1)  # Horizontal line
    pygame.draw.line(screen, GREEN, (mouse_pos[0], mouse_pos[1] - 10), (mouse_pos[0], mouse_pos[1] + 10), 1)  # Vertical line

    # Refresh the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

