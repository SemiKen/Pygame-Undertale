import pygame
from abc import ABC, abstractmethod
import os

class Audio(ABC):

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
    

class SoundManager:
    def __init__(self) -> None:
        pygame.mixer.init()
        # default setting sounds
        self.sounds = { "pullback": "sounds/mus-sfx-a-pullback.mp3",
                        "swipe": "sounds/mus-sfx-swipe.mp3",
                        "snd_b": "sounds/snd-b.mp3",
                        "battlefall": "sounds/snd-battlefall.mp3",
                        "bell": "sounds/snd-bell.mp3",
                        "damage_c": "sounds/snd-damage-c.mp3",
                        "hurt": "sounds/snd-hurt1.mp3",
                        "laz": "sounds/snd-laz.mp3",
                        "timestop": "sounds/timestop.mp3",
                        "damage_taken": "sounds/undertale-damage-taken.mp3",
                        "select": "sounds/undertale-select-sound.mp3"}

        self.update()
        # pygame.mixer.Sound(file_path)

    
    def load(self, key, file_path=None):
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
        
        self.sounds[key] = pygame.mixer.Sound(file_path)

    def play(self, key):
        if key in self.sounds:
            self.sounds[key].play()
        else:
            print(f"Sound key {key} not found.")
    
    def update(self):
        for key, file_path in self.sounds.items():
            self.load(key, file_path)

    def stop(self):
        pass
    
    def pause(self):
        pass
    
    def unpause(self):
        pass

class MusicManager:
    def __init__(self) -> None:
        pygame.mixer.init()
        self.musics = {"sakuya": "Music/sukuya_theme.mp3"}
        self.current_music = "sakuya"
    
    def update(self):
        pass

    def load(self, key, file_path=None):
        # Setting Current Music
        self.current_music = key
        if key not in self.musics:
            if file_path and os.path.isfile(file_path):
                self.musics[key] = file_path
            else:
                print(f"File not found: {file_path}")
        pygame.mixer.music.load(self.musics[self.current_music])

    def play(self, key, loops=-1):
        pygame.mixer.music.play(loops)

    def stop(self):
        pygame.mixer.music.stop()
    
    def pause(self):
        pygame.mixer.music.pause()
    
    def unpause(self):
        pygame.mixer.music.unpause()