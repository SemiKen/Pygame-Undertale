import pygame
# import random
import math
import time

class Player(pygame.sprite.Sprite):

    def __init__(self, screen_width, screen_height, name, level, hp_current, hp_max, game_instance):
        super().__init__()
        
        # Game and Screen References
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_instance = game_instance

        # Player State
        self._status = [name, level, hp_current, hp_max]
        self.speed = 3
        self._damage_taken = False

        # Player Modes and Selection
        self._player_state = {
            "current_mode" : "normal",
            "mode_selection_index" : 1,
            "menu_selection_index" : 0,
            "item_selection_index" : 0,
            "is_selected_item" : False,
            "player_tween_completed" : False,
        } # self._player_state["menu_selection_index"]

        # Item Management
        self._player_items = ["Rice Balls", "Pancakes", "Soup", "Dango", "Bento Boxes"]

        # Physics Properties
        self.gravity = 0.5
        self.jump_force = -10
        self.velocity_y = 0
        self.on_ground = False

        # Load Initial Assets and Set Position
        self.previous_mode = None
        self.load_player_image()
        self.set_initial_position()

        # Tweening Properties
        self.tween_speed = 0.25
        self.target_x = 87.5
        self.target_y = 529

        # Time Manager
        self.last_key_press_time = time.time()

    def update(self, line_group):
        self.get_user_input() # 1
        self.constrain_movement(line_group) # 2
        self.update_tweening() # 3



    # Method หลักๆ ที่ใช้งาน
    def get_user_input(self):
        keys = pygame.key.get_pressed()

        if self._player_state["is_selected_item"]:
            self.handle_item_selection(keys)
        elif self._player_state["current_mode"] == "selection":
            self.handle_selection_mode(keys)
        else:
            self.handle_movement(keys)

        if keys[pygame.K_e] and self.wait():
            self.switch_mode()

    def constrain_movement(self, line_group):
        collisions = pygame.sprite.spritecollide(self, line_group, False)

        if self._player_state["current_mode"] == "gravity":
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

        for line in collisions:
            if line.name == "Top":
                self.rect.y += self.speed
            if line.name == "Right":
                self.rect.x -= self.speed
            if line.name == "Left":
                self.rect.x += self.speed
            if line.name == "Bottom":
                if self._player_state["current_mode"] == "gravity":
                    self.rect.bottom = line.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                else:
                    self.rect.y -= self.speed

    def update_tweening(self):
        if self._player_state["current_mode"] == "selection":
            self.rect.x += (self.target_x - self.rect.x) * self.tween_speed
            self.rect.y += (self.target_y - self.rect.y) * self.tween_speed

            if math.floor(self.rect.x / 40) == math.floor(self.target_x / 40):
                self._player_state["player_tween_completed"] = True
    


    # sub-method ของ get_user_input 
    # ตอนเลือก Item
    def handle_item_selection(self, keys):
        items_amount = len(self.game_instance.UI_info["items_menus"][self._player_state["menu_selection_index"]])
        num_columns = 3

        if keys[pygame.K_LEFT] and self.wait(1/4):
            if self._player_state["item_selection_index"] - num_columns >= 0:
                self._player_state["item_selection_index"] -= num_columns

        elif keys[pygame.K_RIGHT] and self.wait(1/4):
            if self._player_state["item_selection_index"] + num_columns < items_amount:
                self._player_state["item_selection_index"] += num_columns

        elif keys[pygame.K_UP] and self.wait(1/4):
            if self._player_state["item_selection_index"] % num_columns > 0:
                self._player_state["item_selection_index"] -= 1

        elif keys[pygame.K_DOWN] and self.wait(1/4):
            if (self._player_state["item_selection_index"] % num_columns) < (num_columns - 1):
                if self._player_state["item_selection_index"] < items_amount-1:
                    self._player_state["item_selection_index"] += 1

        self.set_position_menu()

        if keys[pygame.K_ESCAPE] and self.wait(0.25):
            # self.game_instance.reset_menu()
            self._player_state["item_selection_index"] = 0
            self._player_state["is_selected_item"] = False
            self.wait(0.1, self.change_index(0))

    # ตอน เลือก Menu
    def handle_selection_mode(self, keys):
        if keys[pygame.K_SPACE] and self.wait(0.25):
            self.game_instance.sound.play_sound("select")
            self.set_position_menu()
            self._player_state["is_selected_item"] = True

        if keys[pygame.K_RIGHT] and self.wait(0.25): self.change_index(1)
        if keys[pygame.K_LEFT] and self.wait(0.25): self.change_index(-1)

    # ตอน Movement (State : Normal หรือ Blue)
    def handle_movement(self, keys):
        def handle_gravity_jump():
            if self.on_ground:
                self.velocity_y = self.jump_force
                self.on_ground = False
        
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_UP]:
            if self._player_state["current_mode"] != "gravity":
                self.rect.y -= self.speed  
            else: handle_gravity_jump()
        if keys[pygame.K_DOWN] and self._player_state["current_mode"] != "gravity":
            self.rect.y += self.speed



    # เครื่องมือ Method ที่ได้ใช้
    def wait(self, timeset=1, callback=None, callback_args=None):
        current_time = time.time()
        if current_time - self.last_key_press_time > timeset:
            self.last_key_press_time = current_time
            if callback is not None:
                if callback_args is not None:
                    callback(*callback_args)
                else:
                    callback()
            return True
        return False

    def move(self, x, y):
        self._player_state["player_tween_completed"] = False
        self.target_x = x
        self.target_y = y
    
    def switch_mode(self, set=None):
        modes = ['normal', 'gravity', 'selection']
        self._player_state["mode_selection_index"] = (self._player_state["mode_selection_index"] + 1) % len(modes)
        self._player_state["current_mode"] = modes[self._player_state["mode_selection_index"]]
        

        if self._player_state["current_mode"] != self.previous_mode:
            self.load_player_image()
            self.previous_mode = self._player_state["current_mode"]

        print(self._player_state["mode_selection_index"])
        self.change_index(0)

    def change_index(self, value=0, type_mode=0):
        if type_mode==0:
            self._player_state["menu_selection_index"] += value
            self._player_state["menu_selection_index"] %= len(self.game_instance.UI_info["menu_list_name"])
            if not self._player_state["is_selected_item"]:
                self.move(87.5 + (172 * self._player_state["menu_selection_index"]), 529)
        else:
            pass

    def set_position_menu(self):
        current_menu = self.game_instance.UI_info["items_menus"][self._player_state["menu_selection_index"]]
        
        rect = current_menu[self._player_state["item_selection_index"]][1]
        self.move(rect.x - 4 , 7 + rect.y)
    
    # Other Method
    def load_player_image(self):
        if self._player_state["current_mode"] == "normal" or self._player_state["current_mode"] == "selection":
            image_path = "Assets/player.png"
        elif self._player_state["current_mode"] == "gravity":
            image_path = "Assets/player_blue.png"

        self.pre_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.pre_image, (20, 20))
    
    def set_initial_position(self):
        # ตั้งค่าตำแหน่งเริ่มต้นของตัวละครผู้เล่น
        self.rect = self.image.get_rect(midbottom=(self.screen_width // 2, self.screen_height // 1.5))

    def info(self):
        return {
            "player_status": self._status,
            "player_items": self._player_items,
            "player_state": self._player_state,
        }

 