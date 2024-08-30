import pygame
# import random
import math
from source.util import wait

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, name, level, hp_current, hp_max, game_instance):
        super().__init__()

        # Game and Screen References
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_instance = game_instance

        # Player State
        self._name = name
        self._level = level
        self._hp_current = hp_current
        self._hp_max = hp_max
        self.speed = 3
        self._damage_taken = False

        # Player Modes and Selection
        self._player_mode = "normal"
        self.selection = 1
        self._selected_index = 0  
        self.on_using_item = False

        # Item Management
        self._player_items = ["Rice Balls", "Pancakes", "Soup", "Dango", "Bento Boxes"] #, "Fruit Pies"]

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

    def set_initial_position(self):
        # ตั้งค่าตำแหน่งเริ่มต้นของตัวละครผู้เล่น
        self.rect = self.image.get_rect(midbottom=(self.screen_width // 2, self.screen_height // 1.5))

    def move(self, x, y):
        self.game_instance.player_tween_completed = False
        self.target_x = x
        self.target_y = y

    def change_index(self, value=0):
        self.game_instance.item_selection += value
        if self.on_using_item == False:
            offsetX, offsetY = 7.5, 14
            self.move(offsetX + 80 + (172 * self.game_instance.item_selection),
                                offsetY + 515)

    def get_user_input(self):
        keys = pygame.key.get_pressed()
        # item_selection = self.game_instance.item_selection

        if self.on_using_item == True:
            items_amount = self.game_instance.selection_menu["length"]
            num_columns = 3
            # print(num_columns)
            # count = 0
            # i = items_amount
            # while True:
            #     if i % 3 == 0:
            #         count += 1
            #         i -= 3
                
            #     if i <= 0:
            #         break

            # num_columns = count   # จำนวนคอลัมน์ในรายการ
            # num_rows = items_amount // num_columns  # คำนวณจำนวนแถวจากจำนวนไอเทม
            if keys[pygame.K_LEFT] and wait(1/4):
                if self._selected_index - num_columns >= 0:
                    self._selected_index -= num_columns
                    
            elif keys[pygame.K_RIGHT] and wait(1/4):
                if self._selected_index + num_columns < items_amount:
                    self._selected_index += num_columns
                    
            elif keys[pygame.K_UP] and wait(1/4):
                if self._selected_index % num_columns > 0:
                    self._selected_index -= 1

                    # self._selected_index += (num_columns - 1)

            elif keys[pygame.K_DOWN] and wait(1/4):
                if (self._selected_index % num_columns) < (num_columns - 1):
                    if self._selected_index < items_amount-1:
                        self._selected_index += 1
            
            self.game_instance.set_position_menu()

            if keys[pygame.K_ESCAPE] and wait(0.25):
                self.game_instance.reset_menu()
                self._selected_index = 0
                self.on_using_item = False
                wait(0.1)
                self.change_index(0)
                
        elif self._player_mode == "selection":
            if keys[pygame.K_SPACE] and wait(0.25):
                self.game_instance.sound.play_sound("select")
                self.game_instance.set_position_menu()
                self.on_using_item = True

            if keys[pygame.K_RIGHT] and wait(0.25): self.change_index(1)
            if keys[pygame.K_LEFT] and wait(0.25): self.change_index(-1)
            # if self.target_x == self.rect.x and self.target_y == self.rect.y:
            #     self.change_index(0)

        else:
            self.handle_movement(keys)

        if keys[pygame.K_e] and wait():
            self.switch_mode()
            

    def handle_movement(self, keys):
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed if self._player_mode != "gravity" else self.handle_gravity_jump()
        if keys[pygame.K_DOWN] and self._player_mode != "gravity":
            self.rect.y += self.speed

    def handle_gravity_jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_force
            self.on_ground = False

    def switch_mode(self, set=None):
        modes = ['normal', 'gravity', 'selection']
        self.selection = (self.selection + 1) % len(modes)
        
        
        self._player_mode = modes[self.selection]
        print(self._player_mode)

        if self._player_mode != self.previous_mode:
            self.load_player_image()
            self.previous_mode = self._player_mode

        if self.selection == len(modes)-1 and wait(1):
            self.change_index(0)

    def load_player_image(self):
        if self._player_mode == "normal" or self._player_mode == "selection":
            image_path = "Assets/player.png"
        elif self._player_mode == "gravity":
            image_path = "Assets/player_blue.png"

        self.pre_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.pre_image, (20, 20))

    def update(self, line_group):
        self.get_user_input()
        self.constrain_movement(line_group)
        self.update_tweening()

    def update_tweening(self):
        if self._player_mode == "selection":
            self.rect.x += (self.target_x - self.rect.x) * self.tween_speed
            self.rect.y += (self.target_y - self.rect.y) * self.tween_speed

            if math.floor(self.rect.x / 40) == math.floor(self.target_x / 40):
                self.game_instance.player_tween_completed = True

    def constrain_movement(self, line_group):
        collisions = pygame.sprite.spritecollide(self, line_group, False)

        if self._player_mode == "gravity":
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

        for line in collisions:
            self.handle_collision(line)

    def handle_collision(self, line):
        if line.name == "Top":
            self.rect.y += self.speed
        if line.name == "Right":
            self.rect.x -= self.speed
        if line.name == "Left":
            self.rect.x += self.speed
        if line.name == "Bottom":
            self.handle_bottom_collision(line)

    def handle_bottom_collision(self, line):
        if self._player_mode == "gravity":
            self.rect.bottom = line.rect.top
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.rect.y -= self.speed

    def info(self):
        return {
            "player_status": [self._name, self._level, self._hp_current, self._hp_max],
            "player_items": self._player_items,
            "player_mode": self._player_mode,
            "player_selection": self._selected_index,
            # "on_using_item": self.on_using_item,
        }
    
    def take_damage(self):
        def reset():
            self._damage_taken = False
            print("no ouchie")
            
        if self._damage_taken == False:
            self._damage_taken = True
            self.start_time = time.time()  # บันทึกเวลาที่เริ่มการหน่วงเวลา
        
        # ตรวจสอบเวลาที่ผ่านไปใน loop หลัก
        self.start_time = wait(2, reset, start_time=self.start_time)

        print(True)
        wait(2, reset)

    
    @property
    def selected_index(self):
        return self._selected_index

    # Setter สำหรับ _selected_index
    @selected_index.setter
    def selected_index(self, value):
        if isinstance(value, int):  # ตรวจสอบเงื่อนไขของค่าที่กำหนด
            self._selected_index = value
            print(self._selected_index)
            self._selected_index %= len(self.selection_name)
        else:
            raise ValueError("selected_index must be a non-negative integer")
        
    @property
    def player_items(self):
        return self._player_items

    @player_items.setter
    def player_items(self, value):
        if isinstance(value, list) and all(isinstance(item, str) for item in value):
            self._player_items = value
        else:
            raise ValueError("player_items must be a list of strings")

    def remove_item(self, item):
        if item in self._player_items:
            self._player_items.remove(item)
        else:
            raise ValueError("Item not found in player_items")