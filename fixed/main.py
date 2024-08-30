import pygame
from game import Game

pygame.init()

# ตัวแปรต่างๆ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# setting window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Undertale")
icon = pygame.image.load("Images/heart_logo.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


# Color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)


# Font
ut_font = pygame.font.Font("Fonts/DeterminationMonoWebRegular-Z5oq.ttf", 32)
battle_font = pygame.font.Font("Fonts/undertale-in-battle.ttf", 16)
small_battle_font = pygame.font.Font("Fonts/undertale-in-battle.ttf", 14)

player_info = game.get_player_info

name_txt = battle_font.render(player_info[0], True, WHITE)
name_text_rect = name_txt.get_rect()
name_text_rect.bottomleft=(80, 500)

level_txt = battle_font.render(f"LV {player_info[1]}", True, WHITE)
level_text_rect = level_txt.get_rect()
level_text_rect.bottomleft=(180, 500)

hp_label = small_battle_font.render("HP", True, WHITE)
hp_label_rect = hp_label.get_rect()
hp_label_rect.bottomleft=(315, 495)

hp_txt = battle_font.render(f"{player_info[2]} / {player_info[3]}", True, WHITE)
hp_text_rect = hp_txt.get_rect()
hp_text_rect.bottomleft=(395, 500)

# Image
pre_sketch = pygame.image.load("Images/Enemy_Approaching_soundtrack.JPG")
sketch = pygame.transform.scale(pre_sketch,(800//1.125, 600//1.125))
sketch_rect = sketch.get_rect()
sketch_rect.centerx = SCREEN_WIDTH // 2
sketch_rect.centery = SCREEN_HEIGHT // 2

item = pygame.image.load("Images/placeholder_item.JPG")
item_rect = item.get_rect()

def create_layout():
    pygame.draw.line(screen, WHITE, (80, 465), (720, 465), 4)
    pygame.draw.line(screen, WHITE, (80, 310+1), (720, 310+1), 4)

    pygame.draw.line(screen, WHITE, (80, 310), (80, 465+2), 4)
    pygame.draw.line(screen, WHITE, (720, 310), (720, 465+2), 4)

    
    for i in range(0,4):
        screen.blit(item, ((80 + (172 * i)), 515))

    screen.blit(name_txt, (name_text_rect))
    screen.blit(level_txt, (level_text_rect))
    screen.blit(hp_label, (hp_label_rect))

    pygame.draw.rect(screen, YELLOW, (350, 480, 30+(player_info[3]//2), 25), 99)

    screen.blit(hp_txt, ((hp_label_rect.x + 100), 480))
# Font
small_font = pygame.font.Font("Fonts/TAGameboy-Regular.ttf", 12)

position_txt = small_font.render("(0, 0)", True, WHITE)
position_text_rect = position_txt.get_rect()
position_text_rect.topleft=(55, 55)

while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            position_txt = small_font.render("({}, {})".format(mouse_x, mouse_y), True, RED)
            position_text_rect.centerx = mouse_x
            position_text_rect.centery = mouse_y

    if game.running:
        game.player_group.update()
        pass
            
    
    # screen.blit(sketch, (sketch_rect))
    screen.blit(position_txt, (position_text_rect))

    create_layout()
    game.player_group.draw(screen)

    # Game.UI.draw(screen)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()