import pygame
from object import *
from abstract import Game

class SakuyaGame(Game):
    def __init__(self, screen, running):
        super().__init__(screen, running)
        self._initialize_screen(screen)
        self._initialize_object()

        # self._initialize_screen(screen)
        # Initialize game-specific attributes, like player, enemies, etc.

    def update(self):
        # Update game logic here, e.g., player movement, enemy AI
        pass

    def draw(self):
        # Draw game objects here, e.g., player, enemies, UI
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Handle other events (keyboard, mouse, etc.)
            # Implement game-specific input handling here
        
    def _initialize_screen(self, screen):
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self._debug = True
        self.running = True

    def _initialize_object(self):
        self.music = Music()
        self.sound = Sound()

        self.player = Player()
        self.enemy = None()
        pass