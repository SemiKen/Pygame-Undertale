import pygame

class UIManager:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game

        # Fonts
        self.battle_font = pygame.font.Font("Fonts/undertale-in-battle.ttf", 16)
        self.small_battle_font = pygame.font.Font("Fonts/undertale-in-battle.ttf", 14)
        self.small_font = pygame.font.Font("Fonts/undertale-in-battle.ttf", 12)

        # Player Info Text
        self.update_player_info()

        # Position Text (ใช้ในการ Debug)
        self.position_txt = self.small_font.render("(0, 0)", True, (255, 255, 255))
        self.position_text_rect = self.position_txt.get_rect()
        self.position_text_rect.topleft = (55, 55)

        # Item Selection Image
        self.item = pygame.image.load("Images/placeholder_item.JPG")
        self.item_rect = self.item_rect()

    def update_player_info(self):
        player_info = self.game.get_player_info()
        
        self.name_txt = self.battle_font.render(player_info[0], True, (255, 255, 255))
        self.name_text_rect = self.name_txt.get_rect()
        self.name_text_rect.bottomleft(80, 500)

        self.level_txt = self.battle_font.render(f"LV {player_info[1]}", True, (255, 255, 255))
        self.level_text_rect = self.level_txt.get_rect()
        self.level_text_rect.bottomleft(180, 500)

        self.hp_label = self.small_battle_font.render("HP", True, (255, 255, 255))
        self.hp_label_rect = self.hp_label.get_rect()
        self.hp_label_rect.bottomleft = (315, 495)

        self.hp_txt = self.battle_font.render(f"{player_info[2]}" / {player_info[3]}, True, (255, 255, 255))
        self.hp_text_rect = self.hp_txt.get_rect()
        self.hp_text_rect.bottomleft = (395, 500)

    
    def update_mouse_position(self, mouse_x, mouse_y):
        self.position_txt = self.small_battle_font(f"({mouse_x}, {mouse_y})")
        self.position_text_rect.centerx = mouse_x
        self.position_text_rect.centery = mouse_y

    def draw_ui(self):
        # Layout
        self.create_layout()

        # Position
        self.screen.blit(self.position_txt, self.position_text_rect)

        # Update and วาด กลุ่ม player ลง
        self.game.player_group.draw(self.screen)

    def create_layout(self)
    pygame.draw.line(self.screen)