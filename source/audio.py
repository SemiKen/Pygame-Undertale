import pygame


# สร้าง dict สำหรับไฟล์เสียง
sounds = {
            "pullback": "sounds/mus-sfx-a-pullback.mp3",
            "swipe": "sounds/mus-sfx-swipe.mp3",
            "snd_b": "sounds/snd-b.mp3",
            "battlefall": "sounds/snd-battlefall.mp3",
            "bell": "sounds/snd-bell.mp3",
            "damage_c": "sounds/snd-damage-c.mp3",
            "hurt1": "sounds/snd-hurt1.mp3",
            "laz": "sounds/snd-laz.mp3",
            "timestop": "sounds/timestop.mp3",
            "damage_taken": "sounds/undertale-damage-taken.mp3",
            "select": "sounds/undertale-select-sound.mp3"
        }

class SoundManager:
    def __init__(self) -> None:
        pygame.mixer.init()
        # default setting sounds
        
        self.sounds = {}
        for key, file_path in sounds.items():
            self.load_sound(key, file_path)
        
        # pygame.mixer.Sound(file_path)

    
    def load_sound(self, key, file_path):
        self.sounds[key] = pygame.mixer.Sound(file_path)

    def play_sound(self, key):
        if key in self.sounds:
            self.sounds[key].play()
        else:
            print(f"Sound key {key} not found.")
        

class MusicManager:
    def __init__(self) -> None:
        pygame.mixer.init()
    
    def load_music(self, file_path):
        pygame.mixer.music.load(file_path)

    def play_music(self, loops=-1):
        pygame.mixer.music.play(loops)

    def stop_music(self):
        pygame.mixer.music.stop()
    
    def pause_music(self):
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        pygame.mixer.music.unpause()