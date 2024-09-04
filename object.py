from abstract import *

# ------------ 0 - UIObject - 0 ----------- #

# ----------- 0 - AudioObject - 0 ----------- #

class Sound(AudioObject):
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

class Music(AudioObject):
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

# ----------- 0 - SpriteObject - 0 ----------- #

class Player(SpriteObject):
    def __init__(self, x, y, width, height, angle=0):
        super().__init__(x, y, width, height, angle)
        # name, level, hp_current, hp_max
        
        # Game and Screen References
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_instance = game_instance
        self.sound = SoundManager()

        # Player State
        self._status = [name, level, hp_current, hp_max]
        self._started = False
        self.speed = 3
        self._damage_taken = False

    def update(self):
        pass

    
    def handle_events(self):
        pass

    
    def draw(self, surface):
        pass

    
    def check_collision(self, player):
        pass