# File py

import pygame
pygame.init()
import constants

class SpriteSheet(object):
	def __init__(self,sprite_file):
		self.spritesheet = pygame.image.load(sprite_file).convert()

	# Pulls a single sprite
	def pull_sprite(self,x,y,width,height,scale):
		image = pygame.Surface([width,height]).convert()
		image.blit(self.spritesheet,(0,0),(x,y,width,height))
		image.set_colorkey(constants.GREEN_COLOURKEY)
		
		if scale != None:
			image = pygame.transform.scale(image, (scale))

		return image

	'''
		ANIMATION SETS FOR CHARACTERS, THIS DOES NOT INCLUDE WEAPONS, THESE WILL BE IMPOSED OVER THE TOP
	'''

	# Assign walking animations
	def player_sprite_assign(self,player, location):

		# Resetting the walking animations lists, allows for different weapons, ie, rifle classes
		player.animate_d = []
		player.animate_u = []
		player.animate_l = []
		player.animate_r = []

		image = SpriteSheet(location).pull_sprite(40,0,40,40,None)
		player.animate_d.append(image)
		image = SpriteSheet(location).pull_sprite(0,0,40,40,None)
		player.animate_d.append(image)
		image = SpriteSheet(location).pull_sprite(80,0,40,40,None)
		player.animate_d.append(image)

		# Walking animation left list
		image = SpriteSheet(location).pull_sprite(160,0,40,40,None)
		player.animate_l.append(image)
		image = SpriteSheet(location).pull_sprite(120,0,40,40,None)
		player.animate_l.append(image)
		image = SpriteSheet(location).pull_sprite(200,0,40,40,None)
		player.animate_l.append(image)

		# Walking animation right list
		image = SpriteSheet(location).pull_sprite(280,0,40,40,None)
		player.animate_r.append(image)
		image = SpriteSheet(location).pull_sprite(240,0,40,40,None)
		player.animate_r.append(image)
		image = SpriteSheet(location).pull_sprite(320,0,40,40,None)
		player.animate_r.append(image)

		# Walking animation upwards list
		image = SpriteSheet(location).pull_sprite(400,0,40,40,None)
		player.animate_u.append(image)
		image = SpriteSheet(location).pull_sprite(360,0,40,40,None)
		player.animate_u.append(image)
		image = SpriteSheet(location).pull_sprite(440,0,40,40,None)
		player.animate_u.append(image)

	# Stab animations used for "puglism" and "sharp" category weapons (sadly not a pokemon reference)
	def player_sprite_assign_stab(self,player, location):

		# Clearing the previous attack animation
		player.attack_d = []
		player.attack_u = []
		player.attack_l = []
		player.attack_r = []

		# Stab animations down
		image = SpriteSheet(location).pull_sprite(0,0,40,40,None)
		player.attack_d.append(image)
		image = SpriteSheet(location).pull_sprite(40,0,40,40,None)
		player.attack_d.append(image)

		# Stab animations left
		image = SpriteSheet(location).pull_sprite(80,0,40,40,None)
		player.attack_l.append(image)
		image = SpriteSheet(location).pull_sprite(0,40,40,40,None)
		player.attack_l.append(image)

		# Stab animations right
		image = SpriteSheet(location).pull_sprite(40,40,40,40,None)
		player.attack_r.append(image)
		image = SpriteSheet(location).pull_sprite(80,40,40,40,None)
		player.attack_r.append(image)

		# Stab animations up
		image = SpriteSheet(location).pull_sprite(0,80,40,40,None)
		player.attack_u.append(image)
		image = SpriteSheet(location).pull_sprite(40,80,40,40,None)
		player.attack_u.append(image)

	# One handed animations, used for pistols, ala revolver
	def player_sprite_assign_one(self,player,location):

		# Clearing the previous attack animation
		player.attack_d = []
		player.attack_u = []
		player.attack_l = []
		player.attack_r = []

		# One animations down
		image = SpriteSheet(location).pull_sprite(0,0,40,40,None)
		player.attack_d.append(image)

		# One animations left
		image = SpriteSheet(location).pull_sprite(40,0,40,40,None)
		player.attack_l.append(image)

		# One animations right
		image = SpriteSheet(location).pull_sprite(80,0,40,40,None)
		player.attack_r.append(image)

		# One animations up
		image = SpriteSheet(location).pull_sprite(120,0,40,40,None)
		player.attack_u.append(image)

	'''
		ANIMATION SETS FOR WEAPONS, WILL BE IMPOSED ABOVE CHARACTER MODELS, ALLOWS A CUT DOWN OF DRAWING FOR INDVIDUAL ANIMATONS.
	'''
	def clear_weapon_sprites(self, player):
		player.weapon_d = []
		player.weapon_u = []
		player.weapon_l = []
		player.weapon_r = []

	def revolver_sprite_assign(self, player):

		# Clearing the previous weapon animation
		player.weapon_d = []
		player.weapon_u = []
		player.weapon_l = []
		player.weapon_r = []

		# Revolver animations down
		image = SpriteSheet("data/images/revolver_shoot_spritesheet.png").pull_sprite(0,0,40,40,None)
		player.weapon_d.append(image)
		image = SpriteSheet("data/images/revolver_shoot_spritesheet.png").pull_sprite(40,0,40,40,None)
		player.weapon_d.append(image)

		# Revolver animations left
		image = SpriteSheet("data/images/revolver_shoot_spritesheet.png").pull_sprite(80,0,40,40,None)
		player.weapon_l.append(image)
		image = SpriteSheet("data/images/revolver_shoot_spritesheet.png").pull_sprite(0,40,40,40,None)
		player.weapon_l.append(image)

		# Revolver animations right
		image = SpriteSheet("data/images/revolver_shoot_spritesheet.png").pull_sprite(40,40,40,40,None)
		player.weapon_r.append(image)
		image = SpriteSheet("data/images/revolver_shoot_spritesheet.png").pull_sprite(80,40,40,40,None)
		player.weapon_r.append(image)

		# Revolver animations up
		image = SpriteSheet("data/images/revolver_shoot_spritesheet.png").pull_sprite(0,80,40,40,None)
		player.weapon_u.append(image)
		image = SpriteSheet("data/images/revolver_shoot_spritesheet.png").pull_sprite(40,80,40,40,None)
		player.weapon_u.append(image)