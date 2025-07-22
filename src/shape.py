
import pygame
class Line(pygame.sprite.Sprite):
    def __init__(self, start_pos, end_pos, name="", color=(255, 255, 255), width=4):
        super().__init__()
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.width = width
        self.name = name
        
        #  Tween variables
        self.start_pos_initial = start_pos
        self.end_pos_initial = end_pos
        self.tween_duration = 0
        self.tween_time = 0
        self.tweening = False

        self.image = pygame.Surface((1, 1))  # Dummy surface since we're drawing lines
        self.rect = self.image.get_rect()
        
        # Set rect to cover the area of the line
        min_x = min(start_pos[0], end_pos[0])
        max_x = max(start_pos[0] + 2, end_pos[0] + 2)
        min_y = min(start_pos[1], end_pos[1])
        max_y = max(start_pos[1] + 2, end_pos[1] + 2)
        self.rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    
    def show(self, screen):
        # print(self.start_pos, self.end_pos)
        pygame.draw.line(screen, self.color, self.start_pos, self.end_pos, self.width)

    def move(self, target_start_pos, target_end_pos, duration):
        self.start_pos_initial = self.start_pos
        self.end_pos_initial = self.end_pos
        self.target_start_pos = target_start_pos
        self.target_end_pos = target_end_pos
        self.tween_duration = duration
        self.tween_time = 0
        self.tweening = True

    def resize(self, target_scale_x, target_scale_y, duration):
        start_x, start_y = self.start_pos
        end_x, end_y = self.end_pos
        self.start_pos_initial = self.start_pos
        self.end_pos_initial = self.end_pos
        self.target_end_pos = (start_x + int((end_x - start_x) * target_scale_x), start_y + int((end_y - start_y) * target_scale_y))
        self.tween_duration = duration
        self.tween_time = 0
        self.tweening = True

    def cubic_ease_in_out(self, t):
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2
        
    def update(self, dt):
        if self.tweening:
            self.tween_time += dt
            t = self.tween_time / self.tween_duration
            if t >= 1:
                t = 1
                self.tweening = False
            
            ease_value = self.cubic_ease_in_out(t)
            self.start_pos = (self.start_pos_initial[0] + (self.target_start_pos[0] - self.start_pos_initial[0]) * ease_value,
                              self.start_pos_initial[1] + (self.target_start_pos[1] - self.start_pos_initial[1]) * ease_value)
            self.end_pos = (self.end_pos_initial[0] + (self.target_end_pos[0] - self.end_pos_initial[0]) * ease_value,
                            self.end_pos_initial[1] + (self.target_end_pos[1] - self.end_pos_initial[1]) * ease_value)
            
        # Update the rect based on new positions
            min_x = min(self.start_pos[0], self.end_pos[0])
            max_x = max(self.start_pos[0], self.end_pos[0])
            min_y = min(self.start_pos[1], self.end_pos[1])
            max_y = max(self.start_pos[1], self.end_pos[1])
            self.rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)