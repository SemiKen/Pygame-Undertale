import pygame
from game import Game
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sakuya Battle - Undertale")
icon = pygame.image.load("Images/heart_logo.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# Initialize the game
game = Game(screen)

def update_game(dt):
    try:
        game.update(dt)
    except Exception as e:
        print(f"An error occurred: {e}")
        game.running = False

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            game.UI.update_mouse_position(mouse_x, mouse_y)

# Main game loop
while game.running:
    dt = clock.tick(FPS) / 1000.0
    screen.fill((0, 0, 0))

    if os.path.exists("debug.txt"):
        update_game(dt)
    else:
        game.update(dt)

    handle_events()

    pygame.display.update()

# Final cleanup
pygame.quit()