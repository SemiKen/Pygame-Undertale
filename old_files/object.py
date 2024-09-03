from abc import ABC, abstractmethod
import pygame


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

class GameObject(ABC, pygame.sprite.Sprite):
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
    def draw(self, surface):
        pass

    @abstractmethod
    def check_collision(self, player):
        pass

class Character(GameObject):
    def __init__(self, x, y, width, height, angle=0):
        super().__init__(x, y, width, height, angle)


    def update(self):
        # โค้ดสำหรับการอัพเดตพฤติกรรมของศัตรู เช่น การเคลื่อนที่
        pass

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def check_collision(self, player):
        # โค้ดสำหรับการตรวจสอบการชนกันกับผู้เล่น
        pass

    # ----------------0 ส่วนเสริม 0--------------------- #

    def attack(self, player):
        # โค้ดสำหรับการโจมตีหรือทำความเสียหายแก่ผู้เล่น
        # player.take_damage(self.damage)
        pass

    def set_image(self, image_path):
        pre_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(pre_image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

class Knife(GameObject):
    def __init__(self, x, y, width, height, angle=0, damage=0):
        super().__init__(x, y, width, height, angle)
        self.damage = damage
       

        # โหลดภาพ
        pre_image = pygame.image.load("Images/Knife.png")
        scale_image = pygame.transform.scale(pre_image, (width, height))
        self.image = pygame.transform.rotate(scale_image, angle)
        
        # สร้าง rect ที่ครอบคลุมภาพ และตั้งค่าตำแหน่งเริ่มต้น
        self.rect = self.image.get_rect(topleft=(x, y))
    


    def update(self):
        # โค้ดสำหรับการอัพเดตพฤติกรรมของศัตรู เช่น การเคลื่อนที่
        pass

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def check_collision(self, player):
        # โค้ดสำหรับการตรวจสอบการชนกันกับผู้เล่น
        return self.rect.colliderect(player.rect)
    
    # ----------------0 ส่วนเสริม 0--------------------- #
    def attack(self, player):
        # โค้ดสำหรับการโจมตีหรือทำความเสียหายแก่ผู้เล่น
        # player.take_damage(self.damage)
        pass

class Debug_UI(GameObject):
    def __init__(self, x, y, width, height, angle=0, image_path=None):
        super().__init__(x, y, width, height, angle)
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (width, height))
        self.rect = self.image.get_rect(center=(x, y))
        self.default_pos = [self.rect.centerx , y]
        self.speed = 10
        # ตำแหน่งเป้าหมาย (ตรงกลางหน้าจอ)
        self.target_pos = [0, 0]
        self.start_tween = False
        self.is_enabled = False
        self.is_reached = False


        # เพิ่มฟอนต์
        self.battle_font = pygame.font.Font("Fonts/undertale-in-battle.ttf", 24)
        # สร้างรายการเมนู
        self.menu_items = [
            {"text": "Edit Mode", "offset": (0, -50)},
            {"text": "Options", "offset": (0, 25)},
            {"text": "Exit", "offset": (0, 100)}
        ]

    def update(self):
        self.tween_position()
        

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.draw_menu(surface)

    def check_collision(self, player):
        # โค้ดสำหรับการตรวจสอบการชนกันกับผู้เล่น
        pass

    # ----------------0 ส่วนเสริม 0--------------------- #

    def draw_menu(self, surface):
       for item in self.menu_items:
            # คำนวณตำแหน่งจริงของเมนูโดยใช้ offset และตำแหน่งของ Debug_UI
            menu_x = self.rect.centerx + item["offset"][0]
            menu_y = self.rect.centery + item["offset"][1]
            
            # เรนเดอร์ข้อความ
            text_surface = self.battle_font.render(item["text"], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(menu_x, menu_y))
            
            # วาดข้อความลงบนพื้นผิว
            surface.blit(text_surface, text_rect)

    def tween_position(self):
        if self.start_tween:

            if not self.is_enabled:
                # คำนวณตำแหน่งเป้าหมายที่ถูกปรับด้วย offset (กึ่งกลางของภาพ)
                target_x = self.target_pos[0] - self.rect.width / 2
                target_y = self.target_pos[1] - self.rect.height / 2

                
                # เคลื่อนที่ภาพไปยังตำแหน่งเป้าหมายโดยใช้ linear interpolation (lerp)
                self.rect.x += (target_x - self.rect.x) * self.speed / 100
                self.rect.y += (target_y - self.rect.y) * self.speed / 100
            else:
                # คำนวณตำแหน่งเป้าหมายที่ถูกปรับด้วย offset (กึ่งกลางของภาพ)
                target_x = self.default_pos[0] - self.rect.width / 2
                target_y = self.default_pos[1] - self.rect.height / 2
                

                # เคลื่อนที่ภาพไปยังตำแหน่งเป้าหมายโดยใช้ linear interpolation (lerp)
                self.rect.x += (target_x - self.rect.x) * self.speed / 100
                self.rect.y += (target_y - self.rect.y) * self.speed / 100
            
            # print((self.rect.y//9), target_y//9)
            if (self.rect.y//9) == target_y//9:
                self.rect.x = target_x
                self.rect.y = target_y
                self.is_reached = True

class UIManager(GameObject):
    def __init__(self, screen, game_instance, x=0, y=0, width=0, height=0):
        super().__init__(x, y, width, height)  # เรียก super() เพื่อใช้ __init__ จาก GameObject
        self.screen = screen
        self.game_instance = game_instance

        # ข้อมูลผู้เล่น
        self.player = self.game_instance.player
        self.player_status = self.player.info()["player_status"]
        self.player_items = self.player.info()["player_items"]
        self.player_state = self.player.info()["player_state"]

        # ฟอนต์
        self.battle_font = pygame.font.Font("Fonts/undertale-in-battle.ttf", 16)
        self.small_battle_font = pygame.font.Font("Fonts/undertale-in-battle.ttf", 14)
        self.small_font = pygame.font.Font("Fonts/undertale-in-battle.ttf", 12)
        self.selection_font = pygame.font.Font("Fonts/DeterminationMonoWebRegular-Z5oq.ttf", 32)

        # ข้อมูลเมนู
        self.selection_name = ["spell", "act", "bag", "mercy"]
        self._spell = []
        self._act = []
        self._item = []
        self._mercy = []
        self.selection_menus = {"items": [self._spell, self._act, self._item, self._mercy]}

        self.update_player_info()

        # Line Group
        self.line_group = pygame.sprite.Group()
        self.create_lines()

    def update(self, dt):
        # อัปเดตการแสดงผล
        self.player_menu_index = self.player_state["menu_selection_index"]
        self.player_selection_index = self.player_state["item_selection_index"]
        self.is_selected_item = self.player_state["is_selected_item"]
        self.is_player_tween = self.player_state["player_tween_completed"]
        self.update_layout()
        self.update_player_info()
        self.game_instance.UI_info = self.info()

        # อัปเดตเส้นและกลุ่มผู้เล่น
        self.line_group.update(pygame.time.get_ticks())
        for sprite in self.line_group:
            sprite.show(self.screen)
        self.game_instance.player_group.draw(self.screen)

        self.draw_health_bar(self.player_status[2], self.player_status[3], 75)

    def draw(self, surface):
        # วาดข้อมูลต่างๆ ลงบน surface
        self.screen.blit(self.position_txt, self.position_text_rect)
        self.screen.blit(self.name_txt, self.name_text_rect)
        self.screen.blit(self.level_txt, self.level_text_rect)
        self.screen.blit(self.hp_label, self.hp_label_rect)
        self.screen.blit(self.hp_txt, self.hp_text_rect)

        if self.selection_menus["items"][self.player_menu_index] == [] or not self.is_selected_item:
            return
        menu_list = self.selection_menus["items"][self.player_menu_index]
        for i, (item, rect) in enumerate(menu_list[0]):
            if i == self.player_selection_index:
                items = menu_list[1][self.player_selection_index]
                self.screen.blit(items[0], items[1])
            else:
                self.screen.blit(item, rect)