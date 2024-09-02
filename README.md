Nothing Here, No idea to write...
https://www.datawow.io/blogs/readme-md-document-software-open-source

# Project : Undertale With Pygame
เป็นการศึกษาในการทำเกมเบื้องต้นเกี่ยวกับ Pygame โดยโปรเจคนี้จะเป็นการทำ Undertale

## Getting Started : Installing (การติดตั้ง)
1. Download [Python](https://www.python.org/)
2. Download Text-Editor Like [VSCODE](https://code.visualstudio.com/), [Sublime text](https://www.sublimetext.com/) and etc.
3. Install Python PIP and Libary pygame
4. Finally Success for use code

# Running the tests

## Import Code
``` python
import pygame
from game import Game
import os
```

## Initialize Pygame & Constants
``` python
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
```

## Setup display
``` python
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sakuya Battle - Undertale")
icon = pygame.image.load("Images/heart_logo.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
```

## Initialize the game
``` python
game = Game(screen)
```
### Functions
``` python
def update_game(dt):
    try:
        game.update(dt)
    except Exception as e:
        print(f"An error occurred: {e}")
        game.running = False

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            game.UI.update_mouse_position(mouse_x, mouse_y)
```

## Main game loop
``` python
while game.running:
    dt = clock.tick(FPS) / 1000.0
    screen.fill((0, 0, 0))

    if os.path.exists("debug.txt"):
        update_game(dt)
    else:
        game.update(dt)

    handle_events()
```

    pygame.display.update()

## End Process

``` python
pygame.quit()
```
