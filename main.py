import pygame
from game import SakuyaGame  # Assuming you name the concrete class SakuyaGame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sakuya Battle - Undertale")
icon = pygame.image.load("Images/heart_logo.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# Initialize the game
game = SakuyaGame(screen, True)

# Main game loop
game.run()

# Final cleanup
pygame.quit()
