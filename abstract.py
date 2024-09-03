from abc import ABC, abstractmethod
import pygame
import os


class UIObject(ABC, pygame.sprite.Sprite):
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

class AudioObject(ABC):
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

class SpriteObject(ABC, pygame.sprite.Sprite):
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
