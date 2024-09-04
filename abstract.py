from abc import ABC, abstractmethod
import pygame
import os
FPS = 60

class Game(ABC):
    def __init__(self, screen, running):
        GameConfig.set_screen(screen)  # Set the screen in the configuration
        self.screen = screen
        self.running = running
        self.dt = 0
        self.clock = pygame.time.Clock()
        # Additional game setup

    def run(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.screen.fill((0, 0, 0))

            self.handle_events()  # Handle input events
            self.update()       # Update game logic

            self.draw()     # Draw everything on the screen

            pygame.display.update()

            pygame.display.flip()
            # self.clock.tick(60)

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def handle_events(self):
        pass

class GameConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameConfig, cls).__new__(cls)
            cls._instance.screen = None
        return cls._instance

    @staticmethod
    def set_screen(screen):
        GameConfig()._instance.screen = screen

    @staticmethod
    def get_screen():
        return GameConfig()._instance.screen
    
# Sub Class


class UIObject(Game, ABC, pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.Surface((1, 1))  # Placeholder surface
        self.rect = self.image.get_rect()

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

class AudioObject(Game, ABC):
    @abstractmethod
    def load(self, key, file_path=None):
        pass

    @abstractmethod
    def play(self, key=None):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def stop(self):
        pass
    
    @abstractmethod
    def pause(self):
        pass
    
    @abstractmethod
    def unpause(self):
        pass

class SpriteObject(Game, ABC, pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, angle=0, *groups: pygame.sprite.AbstractGroup):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def handle_events(self):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

    @abstractmethod
    def check_collision(self, player):
        pass
