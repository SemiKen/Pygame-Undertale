import pygame
from player import Player
from object import *
from source.ui import UIManager
from source.audio  import SoundManager, MusicManager



class Game:
    def __init__(self, screen):
        self._initialize_screen(screen)
        self._initialize_game_state()
        self._initialize_player()
        self._initialize_audio()
        self._initialize_object()
        self._initialize_ui(screen)

    def _initialize_screen(self, screen):
        """Initialize screen dimensions."""
        self.surface = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

    def _initialize_object(self):
        self.knife = Knife(600, 322, 320//4, 100//4, 90, 5)

    def _initialize_game_state(self):
        """Initialize the game's state-related attributes."""
        self._running = True
        # self._menu_index = 0
        # self._item_selection = 0

        # self.player_tween_completed = False
        # self.selection_name = ["spell", "act", "bag", "mercy"]

        # self.selection_menu = {"items" : [],
        #                        "length" : 0,
        #                        "current_selection" : 0}
        

    def _initialize_player(self):
        """Create and initialize the player and player group."""
        self._player = Player(
            self.screen_width, self.screen_height, "Reimu", 7, 20 + (6 * 4), 20 + (6 * 4), self
        )
        self.player_group = pygame.sprite.GroupSingle(self._player)

    def _initialize_audio(self):
        """Load and initialize the game's audio."""
        self.music = MusicManager()
        self.sound = SoundManager()
        self.music.load_music("Music/sukuya_theme.mp3")
        # Uncomment to start playing the music immediately
        # self.music.play_music()

    def _initialize_ui(self, screen):
        """Initialize the UI components."""
        self.UI = UIManager(screen, self)
        self.UI_info = self.UI.info()


    def update(self, dt):
        self.player_group.update(self.UI.line_group)
        self.setting_object(self.knife)
        self.UI.update(dt)
        # self.UI.update_mouse_position(self.player_group.sprite.rect.x, self.player_group.sprite.rect.y)

  

    def setting_object(self, gameObject: GameObject):    
        gameObject.draw(self.surface)
        if gameObject.check_collision(self.player):
            self.player.take_damage()




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
    @property
    def menu_index(self):
        return self._menu_index
    
    @menu_index.setter
    def menu_index(self, value):
        if 0 <= value < len(self.selection_name):
            self._menu_index = value
        else:
            raise ValueError("menu_index must be within valid range")


    @property
    def item_selection(self):
        return self._item_selection

    # Setter สำหรับ _item_selection
    @item_selection.setter
    def item_selection(self, value):
        if isinstance(value, int):  # ตรวจสอบเงื่อนไขของค่าที่กำหนด
            self._item_selection = value
            self._item_selection %= len(self.selection_name)
        else:
            raise ValueError("item_selection must be a non-negative integer")
        
    
        
            
