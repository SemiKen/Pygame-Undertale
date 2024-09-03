import pygame
# import random
import math
import time
from source.audio import SoundManager

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, name, level, hp_current, hp_max, game_instance):
        super().__init__()
        
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

        # Player Modes and Selection
        self._player_state = {
            "current_mode" : "normal",
            "mode_selection_index" : 0,
            "menu_selection_index" : 0,
            "item_selection_index" : 0,
            "is_selected_item" : False,
            "is_paused": False,
            "pause_menu": [],
            "player_tween_completed" : False,
        } # self._player_state["is_selected_item"]

        # Item Management
        self._player_items = ["Rice Balls", "Pancakes", "Soup", "Dango", "Bento Boxes"]

        # Physics Properties
        self.gravity = 0.5
        self.jump_force = -10
        self.velocity_y = 0
        self.on_ground = False
        self.image_alpha = 255
        self.image_change = False

        # Load Initial Assets and Set Position
        self.previous_mode = None
        self.set_player_image()
        self.set_initial_position()

        # Tweening Properties
        self.tween_speed = 0.25
        self.target_x = 87.5
        self.target_y = 529
        self.target_alpha = 0
        self.tween_alpha_speed = 50

        # Event
        self.event_info = {"events" : [],
                           "callback" : [],
                           "args" : []}

        # Time Manager
        self.last_key_press_time = time.time()

    def update(self, line_group):
        self.get_user_input() # 1
        if self._player_state['is_paused']: return
        self.constrain_movement(line_group) # 2
        self.update_tweening() # 3
        if self.image_change == True:
            self.tween_alpha(self.target_alpha)



    # Method หลักๆ ที่ใช้งาน
    def get_user_input(self):
        keys = pygame.key.get_pressed()
        def pause():
            if keys[pygame.K_q] and self.game_instance.debug and self.wait(1/6):
                self.pause_game()
            if self.game_instance.debug_UI.is_reached == True and self.game_instance.debug_UI.start_tween:
                self.game_instance.debug_UI.is_enabled = not self.game_instance.debug_UI.is_enabled
                self.game_instance.debug_UI.start_tween = False
                self.game_instance.debug_UI.is_reached = False
                if not self.game_instance.debug_UI.is_enabled:
                    self._player_state['is_paused'] = False
                print(self._player_state['is_paused'])

        if not self._player_state['is_paused']:
            pause()
        else:
            pause()
            self.handle_selection_menu(keys)
            return

        if self._started == False:
            self._started = True
            self.switch_mode()
            self.change_index(0)

        if self._player_state["is_selected_item"]:
            self.handle_item_selection(keys)
        
        elif self._player_state["current_mode"] == "selection":
            
            self.handle_selection_mode(keys)
        else:
            self.handle_movement(keys)

        if keys[pygame.K_e] and self.wait():
            self.switch_mode(1)

        

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

        self.change_index(type_mode=2)

        if keys[pygame.K_ESCAPE] and self.wait(0.25):
            self._player_state["item_selection_index"] = 0
            self._player_state["is_selected_item"] = False
            self.wait(0.1, self.change_index(0))

    # ตอน เลือก Menu
    def handle_selection_mode(self, keys):
        if keys[pygame.K_SPACE] and self.wait(0.25):
            self.sound.play("select")
            self.change_index(type_mode=2)
            self._player_state["is_selected_item"] = True

        if keys[pygame.K_RIGHT] and self.wait(0.25): self.change_index(1)
        if keys[pygame.K_LEFT] and self.wait(0.25): self.change_index(-1)
        
     # ตอน เลือก Menu
    def handle_selection_menu(self, keys):
        if keys[pygame.K_UP]: 
            self.change_index(1,1)
        if keys[pygame.K_DOWN]:
            self.change_index(-1,1)
        pass
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
    def delay(self, second=2.0, callback=None, callback_args=None):

        
        # เก็บข้อมูล callback และ arguments เพื่อใช้งานในการจัดการเหตุการณ์
        for i in range(0, len(self.event_info["events"])+1):
            if i not in self.event_info["events"]:
                # ตั้งค่าตัวจับเวลา
                pygame.time.set_timer(pygame.USEREVENT + i, math.floor(second * 1000))
                self.event_info["events"].insert(i, i)
                self.event_info["callback"].insert(i, callback)
                self.event_info["args"].insert(i, callback_args)
                

                break

    def handle_event(self, event):
        # ตรวจสอบเหตุการณ์จากตัวจับเวลา
        for i in self.event_info["events"]:
            if event.type == pygame.USEREVENT + i:
                index = self.event_info["events"].index(i)  # Get the correct index
                
                if self.event_info["callback"][index] is not None:
                    if self.event_info["args"][index] is not None:
                        self.event_info["callback"][index](*self.event_info["args"][index])
                    else:
                        self.event_info["callback"][index]()
                
                # Remove the event and corresponding callback and args
                self.event_info["events"].pop(index)
                self.event_info["callback"].pop(index)
                self.event_info["args"].pop(index)
                
                # Stop the timer for this event
                pygame.time.set_timer(pygame.USEREVENT + i, 0)

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
        if not self._player_state["is_selected_item"]:
            self._player_state["player_tween_completed"] = False
        self.target_x = x
        self.target_y = y
    
    def switch_mode(self, value=0):
        modes = ['normal', 'gravity', 'selection']
        self._player_state["mode_selection_index"] = (self._player_state["mode_selection_index"] + value) % len(modes)
        self._player_state["current_mode"] = modes[self._player_state["mode_selection_index"]]
        if self._player_state["mode_selection_index"] == 1:
            self.sound.play("bell")

        if self._player_state["current_mode"] != self.previous_mode:
            self.set_player_image()
            self.previous_mode = self._player_state["current_mode"]

        print(self._player_state["mode_selection_index"])
        self.change_index(0)

    def change_index(self, value=0, type_mode=0):
        if type_mode==0 or type_mode==1:
            if self._player_state["pause_menu"] == []:
                self.game_instance.debug_UI.player = self
                self._player_state["pause_menu"].extend(self.game_instance.debug_UI.menu_items)
                
            menus = [self.game_instance.UI_info["menu_list_name"],self._player_state["pause_menu"]]
            self._player_state["menu_selection_index"] += value
            self._player_state["menu_selection_index"] %= len(menus[type_mode])
            if not self._player_state["is_selected_item"] and not self._player_state['is_paused']:
                self.move(87.5 + (172 * self._player_state["menu_selection_index"]), 529)
        else:
            current_menu = self.game_instance.UI_info["items_menus"][self._player_state["menu_selection_index"]]
            rect = current_menu[self._player_state["item_selection_index"]][1]
            self.move(rect.x - 4 , 7 + rect.y)
       
    def pause_game(self):
        if self.game_instance.debug_UI.start_tween == True: return
        self._player_state['is_paused'] = not self._player_state['is_paused']
        if self._player_state['is_paused']:
            self.is_reached = False
            self.game_instance.debug_UI.start_tween = True
        pass
    
    # Other Method
    def tween_alpha(self, target_alpha):
        if self.image_alpha > target_alpha:
            self.image_alpha -= self.tween_alpha_speed
            if self.image_alpha < target_alpha:
                self.image_alpha = target_alpha
        elif self.image_alpha < target_alpha:
            self.image_alpha += self.tween_alpha_speed
            if self.image_alpha > target_alpha:
                self.image_alpha = target_alpha
        
        if self.wait(1/16):
            self.image.set_alpha(self.image_alpha)

    def set_player_image(self):
        if self._player_state["current_mode"] == "normal" or self._player_state["current_mode"] == "selection":
            image_path = "Assets/player.png"
        elif self._player_state["current_mode"] == "gravity":
            image_path = "Assets/player_blue.png"


        self.pre_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.pre_image, (20, 20)).convert_alpha()
        self.image.set_alpha(self.image_alpha)
    
    def set_initial_position(self):
        # ตั้งค่าตำแหน่งเริ่มต้นของตัวละครผู้เล่น
        self.rect = self.image.get_rect(midbottom=(self.screen_width // 2, self.screen_height // 1.5))

    def take_damage(self, damage=0):
       if not self._damage_taken:
        def reset():
            self.tween_alpha_speed = 125
            self._damage_taken = False
            self.image_change = False

        def create_show_callback(speed, alpha):
            def show():
                self.tween_alpha_speed = speed
                self.target_alpha = alpha
            return show

        # ลด HP หรือจัดการความเสียหายที่ได้รับ
        self._damage_taken = True
        self.sound.play("hurt")
        self._status[3] -= damage
        if self._status[3] <= 0:
            self._status[3] = 0

        # เริ่มกระพริบภาพด้วยความเร็วจากเร็วไปช้า
        self.tween_alpha_speed = 85
        self.image_change = True
        
        delay_times = [0.05, 0.125, 0.25, 0.5, 0.75]  # ช่วงเวลา delay
        speeds = [125, 90, 60, 32, 25]  # ความเร็วในการ tween
        alphas = [255, 0, 255, 0, 255]  # ค่า alpha ของภาพ

        for i in range(len(delay_times)):
            callback = create_show_callback(speeds[i], alphas[i])
            self.delay(delay_times[i], callback)
        
        # ตั้งเวลาเพื่อเปลี่ยน `_damage_taken` กลับเป็น False หลังจาก 2 วินาที
        self.delay(1.5, reset)

    def info(self):
        return {
            "player_status": self._status,
            "player_items": self._player_items,
            "player_state": self._player_state,
        }

 