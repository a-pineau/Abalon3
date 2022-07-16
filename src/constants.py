"""Sets the constant variables.

In descending order:
- Window size and font property
- Colours used
- Images (please note that all images used are free to use, links provided below)
- Initial configurations
"""

import os
import pygame
from math import sqrt
from pygame.locals import *

pygame.init()
useless_screen = pygame.display.set_mode()

FONT = pygame.font.SysFont("Calibri", 42)

# Directories
FILE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(FILE_DIR, "../images")
SNAP_FOLDER = "snapshots"

# Colours
BACKGROUND = (30, 30, 30)
DEAD_ZONE = (141, 141, 141)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
RED2 = (207, 46, 46)
BLUE_MARBLE = (158, 190, 228, 255)
YELLOW = (255, 255, 0)
YELLOW_MARBLE = (249, 217, 84, 255)
GREEN = (0, 255, 0)
GREEN2 = (39, 151, 0)
GREEN3 = (102, 203, 112)
ARROW_COLOR = (255, 0, 247)

# Images
# https://www.iconshock.com/flat-icons/3d-graphics-icons/sphere-icon/
MARBLE_RED = pygame.image.load(
    os.path.join(IMAGES_DIR, "sphere_red.png")
    ).convert_alpha()
MARBLE_GREEN = pygame.image.load(
    os.path.join(IMAGES_DIR, "sphere_green.png")
    ).convert_alpha()
MARBLE_BLUE = pygame.image.load(
    os.path.join(IMAGES_DIR, "sphere_blue.png")
    ).convert_alpha()
DEAD_BLUE = pygame.image.load(
    os.path.join(IMAGES_DIR, "sphere_blue.png")
    ).convert_alpha()
DEAD_BLUE.set_alpha(128)
MARBLE_YELLOW = pygame.image.load(
    os.path.join(IMAGES_DIR, "sphere_yellow.png")
    ).convert_alpha()
DEAD_YELLOW = pygame.image.load(
    os.path.join(IMAGES_DIR, "sphere_yellow.png")
    ).convert_alpha()
DEAD_YELLOW.set_alpha(128)
MARBLE_PURPLE = pygame.image.load(
    os.path.join(IMAGES_DIR, "sphere_purple.png")
    ).convert_alpha()
MARBLE_CYAN = pygame.image.load(
    os.path.join(IMAGES_DIR, "sphere_cyan.png")
    ).convert_alpha()
MARBLE_BROWN = pygame.image.load(
    os.path.join(IMAGES_DIR, "sphere_brown.png")
    ).convert_alpha()
MARBLE_FREE = pygame.image.load(
    os.path.join(IMAGES_DIR, "sphere_empty.png")
    ).convert_alpha()

MARBLE_RED.get_rect().inflate_ip(2, 2)
MARBLE_SIZE = MARBLE_RED.get_rect().size[0] # All marbles have the same size
MAX_DISTANCE_MARBLE = MARBLE_SIZE * sqrt(1.25) # Max distance between two neighbouring marbles (diagonal)

# https://icons8.com/icon/54885/skull
SKULL = pygame.image.load(
    os.path.join(IMAGES_DIR, "skull.png")
).convert_alpha()
SKULL = pygame.transform.rotozoom(SKULL, 0, 0.7)  # Adjusting size

# Window's size
WIDTH = 900
FIRST_X = WIDTH*0.5 - MARBLE_SIZE*2.5 # Centering board inside game window
FIRST_Y = 60 # Defines window's height
HEIGHT = FIRST_Y*2 + MARBLE_SIZE*9

# Keys are arbitrary chosen
MARBLE_IMGS = {
    -2: DEAD_BLUE,
    -3: DEAD_YELLOW,
    1: MARBLE_FREE, 
    2: MARBLE_BLUE, 
    3: MARBLE_YELLOW,
    4: MARBLE_GREEN,
    5: MARBLE_RED,
}

# Messages
CONFIRM_MOVE = "Hit the spacebar to confirm your move"
WRONG_MOVE = "Wrong move!"

# Initial configurations
STANDARD = [
    [2, 2, 3, 2, 2],
    [2, 2, 2, 2, 2, 2],
    [1, 1, 2, 2, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 3, 3, 3, 1, 1],
    [3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3],
]
GERMAN_DAISY = (
    [1, 1, 1, 1, 1],
    [2, 2, 1, 1, 3, 3],
    [2, 2, 2, 1, 3, 3, 3],
    [1, 2, 2, 1, 1, 3, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 1, 1, 2, 2, 1],
    [3, 3, 3, 1, 2, 2, 2],
    [3, 3, 1, 1, 2, 2],
    [1, 1, 1, 1, 1],
)
BELGIAN_DAISY = (
    [2, 2, 1, 3, 3],
    [2, 2, 2, 3, 3, 3],
    [1, 2, 2, 1, 3, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 1, 2, 2, 1],
    [3, 3, 3, 2, 2, 2],
    [3, 3, 1, 2, 2],
)
DUTCH_DAISY = (
    [2, 2, 1, 3, 3],
    [2, 3, 2, 3, 2, 3],
    [1, 2, 2, 1, 3, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 1, 2, 2, 1],
    [3, 2, 3, 2, 3, 2],
    [3, 3, 1, 2, 2],
)
SWISS_DAISY = (
    [1, 1, 1, 1, 1],
    [2, 2, 1, 1, 3, 3],
    [2, 3, 2, 1, 3, 2, 3],
    [1, 2, 2, 1, 1, 3, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 1, 1, 2, 2, 1],
    [3, 2, 3, 1, 2, 3, 2],
    [3, 3, 1, 1, 2, 2],
    [1, 1, 1, 1, 1],
)
DOMINATION = (
    [1, 1, 1, 1, 1],
    [2, 1, 1, 1, 1, 3],
    [2, 2, 1, 1, 1, 3, 3],
    [2, 2, 2, 2, 1, 3, 3, 3],
    [1, 1, 1, 3, 1, 3, 1, 1, 1],
    [3, 3, 3, 1, 2, 2, 2, 2],
    [3, 3, 1, 1, 1, 2, 2],
    [3, 1, 1, 1, 1, 2],
    [1, 1, 1, 1, 1],
)
PYRAMID = (
    [2, 1, 1, 1, 1],
    [2, 2, 1, 1, 1, 1],
    [2, 2, 2, 1, 1, 1, 1],
    [2, 2, 2, 2, 1, 1, 1, 1],
    [2, 2, 2, 2, 1, 3, 3, 3, 3],
    [1, 1, 1, 1, 3, 3, 3, 3],
    [1, 1, 1, 1, 3, 3, 3],
    [1, 1, 1, 1, 3, 3],
    [1, 1, 1, 1, 3],
)
THE_WALL = (
    [1, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 1],
    [2, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 3, 3, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 3, 1, 1],
)

