#!/usr/bin/python3.4

import pygame
pygame.init()

import spritefunctions

# Colour variables
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# used in menus to highlight selected items
YELLOW_HIGHLIGHT = (255,255,153)

# used for png transparency
GREEN_COLOURKEY = (0,255,80)

# Size of the screen in pixels
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Size of the map in tiles
MAP_WIDTH = 20
MAP_HEIGHT = 20

# width/height of a floor tile in pixels
TILE_WIDTH = 40
TILE_HEIGHT = 40

# Speed that the game runs at, in frames per second, used for animation pacing, logic, as well as player responsiveness (game is VERY tied to the framerate)
FPS = 60

# Other game variables
# Used to dictate the amount of frames a key must be held down for, before triggering the player to walk in that direction, and not turn on the spot
TURNING_DELAY = 10
# Font used by the ingame console
font = pygame.font.Font("data/pixle.ttf", 20)
# Amount of ingame messages to be printed to console (in game console window, not cmd.)
AMOUNT_OF_MESSAGES_IN_LOG = 3

# Temporary sprite holders
enemy = pygame.image.load("data/images/test2.png")

# Items
stick = pygame.image.load("data/images/stick.png")
med_kit = pygame.image.load("data/images/medical.png")

# Weapon item forms
revolver = pygame.image.load("data/images/revolver_working/shoot/revolver_l_shoot_1.png")

floor = pygame.image.load("data/images/rock_floor.png")
wall = pygame.image.load("data/images/rock_wall.png")