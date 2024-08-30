from abc import ABC, abstractmethod
import pygame

class GameObject(ABC, pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, angle):
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

    @abstractmethod
    def attack(self, player):
        """
        วิธีการโจมตีหรือทำความเสียหายแก่ผู้เล่น
        """
        pass

class Knife(GameObject):
    def __init__(self, x, y, width, height, angle, damage):
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

    def attack(self, player):
        # โค้ดสำหรับการโจมตีหรือทำความเสียหายแก่ผู้เล่น
        # player.take_damage(self.damage)
        pass
    