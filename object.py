from abc import ABC, abstractmethod
import pygame

class GameObject(ABC, pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, angle=0):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))  # กำหนดพื้นฐานสำหรับ image
        self.rect = self.image.get_rect(topleft=(x, y))

    @abstractmethod
    def update(self):
        """
        อัพเดตสถานะของวัตถุในแต่ละเฟรม
        """
        pass

    @abstractmethod
    def draw(self, surface):
        """
        แสดงผลวัตถุบนหน้าจอ
        """
        pass

    @abstractmethod
    def check_collision(self, player):
        """
        ตรวจสอบการชนกันกับผู้เล่น
        """
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
