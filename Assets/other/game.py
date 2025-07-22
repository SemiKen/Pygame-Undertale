import pygame
from player import Player
from object import *
from source.ui import UIManager
from source.audio import MusicManager



class Game:
    def __init__(self, screen):
        self._initialize_screen(screen)
        self._initialize_game_state()
        self._initialize_audio()
        self._initialize_object()
        self._initialize_player()
        self._initialize_ui(screen)

    def _initialize_screen(self, screen):
        """Initialize screen dimensions."""
        self.surface = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.debug = True

    def _initialize_object(self):
        self.objects = []
        self.sakuya = Character((self.screen_width // 2) - 75, (self.screen_height // 2) - 225 , 95*1.5, 151*1.5)
        self.sakuya.set_image("Images/characters/sakuya.png")
        
        # สร้าง rect ที่ครอบคลุมภาพ และตั้งค่าตำแหน่งเริ่มต้น
        self.knife = Knife(600, 322, 320//4, 100//4, 90, 5)
        self.debug_UI = Debug_UI(self.screen_width//2, -400, 123*2.5, 147*2.5, 0, "Images/menu_panel.png")
        self.debug_UI.target_pos = self.surface.get_rect().center
        self.objects.append(self.sakuya)
        self.objects.append(self.knife)
        self.objects.append(self.debug_UI)

    def _initialize_game_state(self):
        """Initialize the game's state-related attributes."""
        self._running = True
        

    def _initialize_player(self):
        """Create and initialize the player and player group."""
        self._player = Player(
            self.screen_width, self.screen_height, "Reimu", 7, 20 + (6 * 4), 20 + (6 * 4), self
        )
        self.player_group = pygame.sprite.GroupSingle(self._player)

    def _initialize_audio(self):
        """Load and initialize the game's audio."""
        self.music = MusicManager()
        

        # self.music.load_music("Music/sukuya_theme.mp3")
        # Uncomment to start playing the music immediately
        # self.music.play_music()

    def _initialize_ui(self, screen):
        """Initialize the UI components."""
        self.UI = UIManager(screen, self)
        self.UI_info = self.UI.info()


    def update(self, dt):
        self.player_group.update(self.UI.line_group)
        self.UI.update(dt)
        self.setting_object(self.objects)
        # self.UI.update_mouse_position(self.player_group.sprite.rect.x, self.player_group.sprite.rect.y)

    def setting_object(self, gameObject_array):  
        for gameObject in gameObject_array:  
            gameObject.draw(self.surface)
            gameObject.update()
            if gameObject.check_collision(self.player):
                self.player.take_damage(gameObject.damage)

    def handle_event(self, event):
        self.player.handle_event(event)
        

    # Getter , Setter
    @property
    def player(self):
        return self._player

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        if isinstance(value, bool):
            self._running = value
            if not value:
                print("Game is now stopping.")
        else:
            raise ValueError("running must be a boolean")
        
    
        
            
