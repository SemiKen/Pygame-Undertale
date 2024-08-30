import pygame
from source.shape import Line

class UIManager:
    def __init__(self, screen, game_instance):
        self.screen = screen
        self.game_instance = game_instance

        # Player Information
        self.player = self.game_instance.player
        self.player_status = self.player.info()["player_status"]
        self.player_items = self.player.info()["player_items"]
        self.player_state = self.player.info()["player_state"]
        # "player_mode": self._player_state["current_mode"],

        # Fonts
        self.battle_font = pygame.font.Font("Fonts/undertale-in-battle.ttf", 16)
        self.small_battle_font = pygame.font.Font("Fonts/undertale-in-battle.ttf", 14)
        self.small_font = pygame.font.Font("Fonts/undertale-in-battle.ttf", 12)
        self.selection_font = pygame.font.Font("Fonts/DeterminationMonoWebRegular-Z5oq.ttf", 32)

        


        # Player Info Text and Selections
        self._spell =[]
        self._act = []
        self._item = []
        self._mercy = []
        self.update_player_info()
        # self._menu_index = 0
        # self.player_tween_completed = False
        self.selection_name = ["spell", "act", "bag", "mercy"]
        self.selection_menus = {"items" : [self._spell, self._act, self._item, self._mercy],
                               "length" : 0,
                               "current_selection" : 0}
        # Position Debug Text
        self.position_txt = self.small_font.render("(0, 0)", True, (255, 255, 255))
        self.position_text_rect = self.position_txt.get_rect(topleft=(55, 55))

        # Line Group
        self.line_group = pygame.sprite.Group()
        self.create_lines()

    def update(self, dt):
        self.player_menu_index = self.player_state["menu_selection_index"]
        self.player_selection_index = self.player_state["item_selection_index"]
        self.is_selected_item = self.player_state["is_selected_item"]
        self.is_player_tween = self.player_state["player_tween_completed"]
        self.update_layout()
        

        # Draw lines and player group 
        self.line_group.update(pygame.time.get_ticks())
        for sprite in self.line_group:
            sprite.show(self.screen)
        self.game_instance.player_group.draw(self.screen)
    
    def update_layout(self):
        
        # Draw player selection and information
        self.draw_item_selection_images() # 1
        
        # Draw position for testing debug
        self.screen.blit(self.position_txt, self.position_text_rect)

        # Draw player info text
        self.screen.blit(self.name_txt, self.name_text_rect)
        self.screen.blit(self.level_txt, self.level_text_rect)
        self.screen.blit(self.hp_label, self.hp_label_rect)
        self.screen.blit(self.hp_txt, self.hp_text_rect)

        # Draw actions or items based on the current selection
        if self.selection_menus["items"][self.player_menu_index] == [] or not self.is_selected_item: return
        menu_list = self.selection_menus["items"][self.player_menu_index]
        for i, (item, rect) in enumerate(menu_list[0]):
            if i == self.player_selection_index:
                items = menu_list[1][self.player_selection_index]
                self.screen.blit(items[0], items[1])
            else:
                self.screen.blit(item, rect)
        
    def draw_item_selection_images(self):
        # Draw item selection images based on the player's selection
        for i in range(4):
            state = "focus" if self.player_menu_index == i and self.is_player_tween else "normal"
            item_image = pygame.image.load(f"Images/placeholder/{self.selection_name[i]}_{state}.png")
            self.screen.blit(item_image, (80 + (172 * i), 515))

    def create_text_list(self, text_list, position_func, x, y):
        # Helper to create list of rendered text and their positions
        rendered_list = []
        focus_rendered_list = []
        for i, text in enumerate(text_list):
            rendered_text = self.selection_font.render(f"* {text}", True, (255, 255, 255))
            text_rect = rendered_text.get_rect(bottomleft=position_func(x, y, i))
            rendered_list.append((rendered_text, text_rect))

            focus_rendered_text = self.selection_font.render(f"* {text}", True, (255, 255, 0))
            focus_text_rect = focus_rendered_text.get_rect(bottomleft=position_func(x, y, i))
            focus_rendered_list.append((focus_rendered_text, focus_text_rect))
        return [rendered_list, focus_rendered_list]

   


   # Method เริ่มต้น # --------------------------------

    def update_player_info(self):
        # Render player info text
        self.name_txt = self.battle_font.render(self.player_status[0], True, (255, 255, 255))
        self.name_text_rect = self.name_txt.get_rect(bottomleft=(80, 500))

        self.level_txt = self.battle_font.render(f"LV {self.player_status[1]}", True, (255, 255, 255))
        self.level_text_rect = self.level_txt.get_rect(bottomleft=(180, 500))

        self.hp_label = self.small_battle_font.render("HP", True, (255, 255, 255))
        self.hp_label_rect = self.hp_label.get_rect(bottomleft=(315, 495))

        self.hp_txt = self.battle_font.render(f"{self.player_status[2]} / {self.player_status[3]}", True, (255, 255, 255))
        self.hp_text_rect = self.hp_txt.get_rect(bottomleft=(425, 500))

        def set_column(x, y, i):
            # Calculate offset based on the index `i`
            offset = [225 * (i // 3), 45 * (i % 3)]
            return (x + offset[0], y + offset[1])

        # Initialize actions and items
        self._act = self.create_text_list(["Check", "Talk", "Joke"], set_column, 155, 360)
        self._item = self.create_text_list(self.player_items, set_column, 155, 360)

    def create_lines(self):
        # Define boundary lines for the game area
        boundaries = [
            ((80, 465), (720, 465), "Bottom"),
            ((80, 311), (720, 311), "Top"),
            ((80, 310), (80, 467), "Left"),
            ((720, 310), (720, 467), "Right"),
        ]
        for start_pos, end_pos, name in boundaries:
            self.line_group.add(Line(start_pos, end_pos, name=name))

    # Method อื่นๆ # --------------------------------
    def info(self):
        return {
            "items_menus": [self._spell, self._act[0], self._item[0], self._mercy],
            "menu_list_name" : self.selection_name
        }
    
    def update_mouse_position(self, mouse_x, mouse_y):
        self.position_txt = self.small_battle_font.render(f"({mouse_x}, {mouse_y})", True, (255, 255, 255))
        self.position_text_rect.center = (mouse_x, mouse_y)

    def set_position_menu(self):
        self.menu_index = self.item_selection
        self.selection_menu["items"] = self.UI_group.info()["items_menu"]
        item_of_menu = self.selection_menu["items"][self.menu_index]
        self.selection_menu["length"] = len(item_of_menu)
        self.selection_menu["current_selection"] = self.player.selected_index
        # print(self.selection_menu["length"])
        # print(item_of_menu[n][1]) got rect
        rect = item_of_menu[self.player.selected_index][1]
        self.player.move(rect.x - 4 , 7 + rect.y)

    def reset_menu(self):
        self.menu_index = 0
        self.selection_menu = {"items" : [],
                            "length" : 0,
                            "current_selection" : 0}