import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("images/background.jpg")

# Sound
mixer.music.load("sound/background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invasion")
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load("images/player.png")
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("images/enemy.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(2)  # Reduced speed for slower gameplay
    enemy_y_change.append(40)

# Bullet
bullet_img = pygame.image.load("images/bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10  # Reduced speed for slower gameplay
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Clock to control frame rate
clock = pygame.time.Clock()

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    return distance < 27

# Game Loop
running = True
while running:
    # Limit the frame rate to 60 FPS
    clock.tick(60)

    # Fill screen and add background
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystroke events for movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5  # Reduced speed for slower gameplay
            if event.key == pygame.K_RIGHT:
                player_x_change = 5  # Reduced speed for slower gameplay
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("sound/laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Player movement
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Enemy movement
    for i in range(num_of_enemies):
        # Game over condition
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000  # Move enemies off screen
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 4  # Reduced speed for slower gameplay
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -4  # Reduced speed for slower gameplay
            enemy_y[i] += enemy_y_change[i]

        # Collision detection
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound("sound/explosion.wav")
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    # Draw player and show score
    player(player_x, player_y)
    show_score(text_x, text_y)

    # Update the display
    pygame.display.update()

