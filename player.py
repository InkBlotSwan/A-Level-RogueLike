# File player.py

import pygame
import constants
import spritefunctions

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.velocity_x = 0
		self.velocity_y = 0

		self.frames_left = []
		self.frames_right = []
		self.frames_up = []
		self.frames_down = []

		self.direction = "D"

		# Retrieving images for animation
		spritesheet = spritefunctions.SpriteSheet("sprites/test.png")
		self.image = pygame.image.load("sprites/test.png")
		self.image.set_colorkey(constants.WHITE)
		self.rect = self.image.get_rect()

		self.rect.x = 100
		self.rect.y = 100