import pygame
from player import Player
from object import *
from fixed.ui import UIManager
from source.audio import MusicManager

class Game:
    def __init__(self, screen):
        self._initialize_screen(screen)
        self._initialize_audio()
        self._initialize_objects(screen)
        self._initialize_player()
        self._initialize_ui(screen)

    def _initialize_screen(self, screen):
        self.surface = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self._debug = True
        self._running = True        

    def _initialize_audio(self):
        self.music = MusicManager()
        # self.music.load_music("Music/sukuya_theme.mp3")
        # self.music.play_music() # Uncomment to start playing the music immediately

    def _initialize_objects(self, screen):
        self.objects = [
            Character((self.screen_width // 2) - 75, (self.screen_height // 2) - 225, 95*1.5, 151*1.5).set_image("Images/characters/sakuya.png"),
            Knife(600, 322, 320//4, 100//4, 90, 5),
            Debug_UI(self.screen_width//2, -400, 123*2.5, 147*2.5, 0, "Images/menu_panel.png")
        ]
        self.objects[-1].target_pos = screen.get_rect().center  # Set target position for Debug_UI

    def _initialize_player(self):
        self._player = Player(self.screen_width, self.screen_height, "Reimu", 7, 20 + (6 * 4), 20 + (6 * 4), self)
        self.player_group = pygame.sprite.GroupSingle(self._player)

    def _initialize_ui(self, screen):
        self.UI = UIManager(screen, self)
        self.UI_info = self.UI.info()

    def update(self, dt):
        self.player_group.update(self.UI.line_group)
        self.UI.update(dt)
        self._update_objects(self.objects)

    def _update_objects(self, objects):
        for obj in objects:
            obj.draw(self.surface)
            obj.update()
            if obj.check_collision(self.player):
                self.player.take_damage(obj.damage)

    def handle_event(self, event):
        self.player.handle_event(event)

    @property
    def player(self):
        return self._player
