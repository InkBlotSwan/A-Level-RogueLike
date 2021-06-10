#!/usr/bin/python3.4

# Python modules
import random
import pygame
import math
import pickle
pygame.init()


# My files
import spritefunctions
import constants
import Path

# Classes below
'''
	HERE ARE ALL CLASSES FOR ALL ENTITIES, TILES FOR THE MAP, ENIMIES PLAYER AND ITEMS.
'''

# Class for all tiles on map, (walls/ floors), and what to draw at each location.
class Tile():
	def __init__(self, can_walk):
		self.can_walk = can_walk
		self.has_entity = False

# Class for all rooms on the map, a roguelike maze, with square rooms and tunnels.
class Room():
	def __init__(self, x, y, width, height):
		self.width = width
		self.height = height

		# Calculate the left, right, top and bottom
		self.left = x
		self.top = y

		self.right = self.left + self.width
		self.bottom = self.top + self.height


		# Defines where the room's tunnel will start from.
		self.middle = (self.right - (width // 2), self.bottom - (height // 2))

		# Is this the initial room? this is used to place the player on the map.
		self.is_initial = False


	# Ensure that our room, doesn't collide with any ther room.
	def collide_detect(self, previous_room):
		room_collide = False

		# If the room collide's with the previous room, do not place it.
		if self.right + 1 >= previous_room.left and self.left - 1 <= previous_room.right and self.bottom + 1 >= previous_room.top and self.top - 1 <= previous_room.bottom:
			room_collide = True

		return room_collide


# All living/moving entities, npcs and the player both inherit from this class. Entity child classes below.
class Entity(pygame.sprite.Sprite):
	def __init__(self,x,y,sprite,entity_name,message_list,max_inventory = 5):
		super().__init__()
		self.image = sprite
		self.image.set_colorkey(constants.GREEN_COLOURKEY)

		self.message_list = message_list
		self.is_turn = False
		self.made_action = False
		self.turn = 1
		# Inventory flags + variables
		self.inventory = []
		self.equipped_weapon = []
		self.max_inventory = max_inventory
		self.has_dropped = False
		self.is_last = False

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.entity_name = entity_name
		self.direction = "D"
		self.weapon = Fist(self)

		self.animation_type = "stab"
		self.weapon_image = None
		self.weapon_rect = None
		self.weapon_depth = 1

		# Lists for walking animations, 2 frames + stationary sprite making 3 frames per step.
		self.animate_d = []
		self.animate_u = []
		self.animate_l = []
		self.animate_r = []
		self.walking = False

		# Lists for attacking aniations, changes out depending upon equipped weapon, change via "equip" function, weapon method.
		self.attack_d = []
		self.attack_u = []
		self.attack_l = []
		self.attack_r = []
		self.attacking = False

		# Lists for weapon animations, diplsyaed over the attack animations, like the attack animations they change out.
		self.weapon_d = []
		self.weapon_u = []
		self.weapon_l = []
		self.weapon_r = []

		# Lists for holstered weapins, to be imposed upon the walking animations
		self.holster_d = []
		self.holster_u = []
		self.holster_l = []
		self.holster_r = []

		# All below are variables used by the play_animate functions.
		self.animation_finished = False
		self.moving = False
		self.iterate = 0

		self.x_new_location = None
		self.y_new_location = None
		self.x_old_location = None
		self.y_old_location = None

		self.x_animate_distance = 0
		self.y_animate_distance = 0

	def draw(self,screen):
		if self.moving == False:
			if self.direction == "D":
				self.image = self.animate_d[0]
			elif self.direction == "U":
				self.image = self.animate_u[0]
			elif self.direction == "L" or self.direction == "UL" or self.direction == "DL":
				self.image = self.animate_l[0]
			elif self.direction == "R" or self.direction == "UR" or self.direction == "DR":
				self.image = self.animate_r[0]
		
		if self.moving == False:
			screen.blit(self.image,(self.rect.x * constants.TILE_WIDTH, self.rect.y *constants.TILE_HEIGHT))
		else:
			if self.weapon.name != "fists" and self.attacking and self.weapon_depth == 1:
				screen.blit(self.weapon_image,(self.weapon_rect.x, self.weapon_rect.y))
			screen.blit(self.image,(self.rect.x, self.rect.y))
			if self.weapon.name != "fists" and self.attacking and self.weapon_depth == 2:
				screen.blit(self.weapon_image,(self.weapon_rect.x, self.weapon_rect.y))


	def update(self, x_change, y_change, game_map, direction, all_entity, player = None):
		if self.iterate > 0:
			return False
		self.direction = direction
		if self.moving == False:
			# Checks if the move is eligable
			if game_map[self.rect.x + x_change][self.rect.y + y_change].can_walk == True:
				can_walk = check_can_walk(all_entity, x_change, y_change, self)
				if can_walk:
					# Code which actually moves the entity.
					if self.entity_name != "Player":
						player.is_turn = False

					self.moving = True
					self.walking = True

					self.x_old_location = self.rect.x
					self.y_old_location = self.rect.y

					self.x_new_location = self.rect.x + x_change
					self.y_new_location = self.rect.y + y_change

					game_map[self.x_old_location][self.y_old_location].has_entity = False
					game_map[self.x_new_location][self.y_new_location].has_entity = True


		elif self.moving == True:
			self.play_animation_walking(player)

	# Walking animation
	def play_animation_walking(self, player):
		# Check which direction players facing
		self.check_direction(1)
		self.animation_finished = False
		self.made_action = False
		self.iterate += 1
		self.rect.x = ((self.x_old_location) * constants.TILE_WIDTH) + self.x_animate_distance
		self.rect.y = ((self.y_old_location) * constants.TILE_HEIGHT) + self.y_animate_distance

		# Play first frame
		if self.iterate < 15:
			if self.direction == "D":
				self.image = self.animate_d[1]
			elif self.direction == "U":
				self.image = self.animate_u[1]
			elif self.direction == "L" or self.direction == "DL" or self.direction == "UL":
				self.image = self.animate_l[1]
			elif self.direction == "R" or self.direction == "DR" or self.direction == "UR":
				self.image = self.animate_r[1]

		# Play second frame
		if self.iterate > 20:
			if self.direction == "D":
				self.image = self.animate_d[0]
			elif self.direction == "U":
				self.image = self.animate_u[0]
			elif self.direction == "L" or self.direction == "DL" or self.direction == "UL":
				self.image = self.animate_l[0]
			elif self.direction == "R" or self.direction == "DR" or self.direction == "UR":
				self.image = self.animate_r[0]

		# Play third frame
		
		if self.iterate > 25:
			if self.direction == "D":
				self.image = self.animate_d[2]
			elif self.direction == "U":
				self.image = self.animate_u[2]
			elif self.direction == "L" or self.direction == "DL" or self.direction == "UL":
				self.image = self.animate_l[2]
			elif self.direction == "R" or self.direction == "DR" or self.direction == "UR":
				self.image = self.animate_r[2]
		# Ending animation
		if self.iterate >= 40:
			self.has_dropped = False

			self.moving = False
			self.walking = False
			self.made_action = True
			self.animation_finished = True

			self.iterate = 0
			self.x_animate_distance = 0
			self.y_animate_distance = 0

			self.rect.x = self.x_new_location
			self.rect.y = self.y_new_location

			if self.is_last == True:
				player.is_turn = True

			if self.entity_name == "Player":
				player.enemy_turn = True

	def play_animation_attacking_stab(self, player):
		if self.iterate < 12:
			self.check_direction(1.5)
		self.animation_finished = False
		self.made_action = False
		self.iterate += 1

		self.rect.x = ((self.x_old_location) * constants.TILE_WIDTH) + self.x_animate_distance
		self.rect.y = ((self.y_old_location) * constants.TILE_HEIGHT) + self.y_animate_distance

		# Play the first frame
		if self.iterate < 6:
			if self.direction == "D":
				self.image = self.attack_d[0]
			elif self.direction == "U":
				self.image = self.attack_u[0]
			elif self.direction == "L":
				self.image = self.attack_l[0]
			elif self.direction == "R":
				self.image = self.attack_r[0]

			# Play the second frame
		if self.iterate > 6:
			if self.direction == "D":
				self.image = self.attack_d[1]
			elif self.direction == "U":
				self.image = self.attack_u[1]
			elif self.direction == "L":
				self.image = self.attack_l[1]
			elif self.direction == "R":
				self.image = self.attack_r[1]

		# Ending the animation
		if self.iterate >= 40:

			self.moving = False
			self.attacking = False
			self.made_action = True
			self.animation_finished = True

			self.iterate = 0
			self.x_animate_distance = 0
			self.y_animate_distance = 0

			self.rect.x = self.x_old_location
			self.rect.y = self.y_old_location

			if self.is_last == True:
				player.is_turn = True

			if self.entity_name == "Player":
				player.enemy_turn = True

	def play_animation_attacking_one(self, player):

		self.animation_finished = False
		self.made_action = False
		self.iterate += 1

		if self.direction == "D":
			self.weapon_image = self.weapon_d[0]
		elif self.direction == "U":
			self.weapon_image = self.weapon_u[0]
		elif self.direction == "L":
			self.weapon_image = self.weapon_l[0]
		elif self.direction == "R":
			self.weapon_image = self.weapon_r[0]

		if self.weapon_rect == None:
			self.weapon_rect = self.weapon_image.get_rect()

		self.rect.x = ((self.x_old_location) * constants.TILE_WIDTH)
		self.rect.y = ((self.y_old_location) * constants.TILE_HEIGHT)

		self.weapon_rect.x = ((self.x_old_location) * constants.TILE_WIDTH)
		self.weapon_rect.y = ((self.y_old_location) * constants.TILE_HEIGHT)

		if self.direction == "D":
			self.weapon_depth = 2
		elif self.direction == "U":
			self.weapon_rect.x += 7
			self.weapon_rect.y -= 7
		elif self.direction == "L":
			self.weapon_rect.x -= 15
			self.weapon_rect.y -= 6
			self.weapon_depth = 1
		elif self.direction == "R":
			self.weapon_rect.x += 16
			self.weapon_rect.y -= 6
			self.weapon_depth = 1

		# Playing first character frame
		if self.iterate < 10:
			if self.direction == "D":
				self.image = self.attack_d[0]
				self.weapon_image = self.weapon_d[0]
			elif self.direction == "U":
				self.image = self.attack_u[0]
				self.weapon_image = self.weapon_u[0]
			elif self.direction == "L":
				self.image = self.attack_l[0]
				self.weapon_image = self.weapon_l[0]
			elif self.direction == "R":
				self.image = self.attack_r[0]
				self.weapon_image = self.weapon_r[0]

		# Playing the second frame
		if self.iterate > 10:
			if self.direction == "D":
				self.image = self.attack_d[0]
				self.weapon_image = self.weapon_d[1]
			elif self.direction == "U":
				self.image = self.attack_u[0]
				self.weapon_image = self.weapon_u[1]
			elif self.direction == "L":
				self.image = self.attack_l[0]
				self.weapon_image = self.weapon_l[1]
			elif self.direction == "R":
				self.image = self.attack_r[0]
				self.weapon_image = self.weapon_r[1]

		# Playing the third frame
		if self.iterate > 15:
			if self.direction == "D":
				self.image = self.attack_d[0]
				self.weapon_image = self.weapon_d[0]
			elif self.direction == "U":
				self.image = self.attack_u[0]
				self.weapon_image = self.weapon_u[0]
			elif self.direction == "L":
				self.image = self.attack_l[0]
				self.weapon_image = self.weapon_l[0]
			elif self.direction == "R":
				self.image = self.attack_r[0]
				self.weapon_image = self.weapon_r[0]

		# Ending the animation
		if self.iterate >= 40:
			if self.is_last == True:
				player.is_turn = True
			self.moving = False
			self.attacking = False
			self.made_action = True
			self.animation_finished = True

			self.iterate = 0
			self.x_animate_distance = 0
			self.y_animate_distance = 0

			self.rect.x = self.x_old_location
			self.rect.y = self.y_old_location

			if self.is_last == True:
				player.is_turn = True

			if self.entity_name == "Player":
				player.enemy_turn = True

	# To be used when determining direction a walking animation will use	
	def check_direction(self, speed):
		# Checking for straight or diagonal movement
		if len(self.direction) < 2:
			if self.direction == "D":
				self.y_animate_distance += speed

			elif self.direction == "U":
				self.y_animate_distance += -speed

			elif self.direction == "L":
				self.x_animate_distance += -speed

			elif self.direction == "R":
				self.x_animate_distance += speed

		# Diagonal movement
		else:
			if self.direction == "DL":
				self.x_animate_distance += -speed
				self.y_animate_distance += speed

			elif self.direction == "DR":
				self.x_animate_distance += speed
				self.y_animate_distance += speed

			elif self.direction == "UL":
				self.x_animate_distance += -speed
				self.y_animate_distance += -speed

			elif self.direction == "UR":
				self.x_animate_distance += speed
				self.y_animate_distance += -speed

	def attack(self, list_of_entities):
		if self.entity_name == "player":
			if self.is_turn:
				self.is_turn = False
				self.x_old_location = self.rect.x
				self.y_old_location = self.rect.y
				self.weapon.shoot(list_of_entities)
				self.animation_finished = False
				self.made_action = True
				self.moving = True
				self.attacking = True
		else:
			self.is_turn = False
			self.x_old_location = self.rect.x
			self.y_old_location = self.rect.y
			self.weapon.shoot(list_of_entities)
			self.animation_finished = False
			self.made_action = True
			self.moving = True
			self.attacking = True

	def take_damage(self, damage, attacker):
		self.health -= damage
		self.message_list.append(attacker.name + " hit " + self.name + " for " + str(damage) + " points")

	def heal(self, health_replenished):
		if self.health == self.max_health:
			self.message_list.append(self.name + " is allready at full health")
			return False
		elif self.health + health_replenished > self.max_health:
			self.health = self.max_health
			self.message_list.append(self.name + " was fully healed")
		else:
			self.message_list.append(self.name + " was healed for " + str(health_replenished) + " points")

	def die(self, all_entity, map_item_list, all_enemy_entity):
		if self.is_last == True:
			all_entity[0].is_turn = True
		all_entity.remove(self)
		all_enemy_entity.remove(self)
		self.message_list.append(self.name + " is dead.")
		if len(self.inventory) > 0:
			try:
				self.inventory[random.randint(0,len(self.inventory) - 1)].drop(all_entity, map_item_list)
			except IndexError:
				pass

	def equip(self, weapon, weapon_item):
		if self.weapon.name == "fists":
			self.weapon = weapon
			self.equipped_weapon.append(weapon_item)
			self.inventory.remove(weapon_item)

			self.weapon.sprite_assign()

	def unequip(self):
		if self.weapon.name != "fists":
			self.weapon = Fist(self)
			self.inventory.append(self.equipped_weapon[0])
			self.equipped_weapon = []

			self.weapon.sprite_assign()

# The player a child of entity
class Player(Entity):
	def __init__(self, max_health, player_name, message_list, x, y):
		super().__init__(x,y, spritefunctions.SpriteSheet("data/images/player_spritesheet.png").pull_sprite(80,0,40,40,None), "Player", message_list)
		self.max_health = max_health
		self.health = self.max_health
		self.name = player_name

		self.made_action = False
		self.animation_finished = False
		self.is_turn = True
		self.enemy_turn = False
		self.turn = None

		# Walking animation downwards list
		spritefunctions.SpriteSheet.player_sprite_assign(self,self,"data/images/player_spritesheet.png")
		spritefunctions.SpriteSheet.player_sprite_assign_stab(self,self,"data/images/player_stab_spritesheet.png")

		self.image = self.animate_d[0]

# A generic enemy class also a child of entity
class Enemy(Entity):
	def __init__(self, max_health, enemy_name, message_list, x, y):
		super().__init__(x, y, constants.enemy, "Enemy", message_list)
		self.max_health = max_health
		self.health = self.max_health
		self.name = enemy_name

		is_last = False

		# Walking animation downwards list
		spritefunctions.SpriteSheet.player_sprite_assign(self,self,"data/images/enemy_spritesheet.png")
		spritefunctions.SpriteSheet.player_sprite_assign_stab(self,self,"data/images/enemy_stab_spritesheet.png")


# Weapon class, individual weapon classes below, objects are passed to entities, which trigger them through attack functions.
class Weapon():
	def __init__(self, owner, weapon_name):
		self.name = weapon_name
		self.owner = owner
		self.hit = False

	def check_if_hit(self, list_of_entities, weapon_range, offset, far_range):
		targets = []
		if self.owner.direction == "D":
			for i in list_of_entities:
				for iterate in range(weapon_range):
					if i is not self.owner:
						if (self.owner.rect.x == i.rect.x - offset and i.rect.y == self.owner.rect.y + (iterate + 1)) or (self.owner.rect.x == i.rect.x and i.rect.y == self.owner.rect.y + (iterate + 1)) or (self.owner.rect.x == i.rect.x + offset and i.rect.y == self.owner.rect.y + (iterate + 1)):
							targets.append(i)
							

		elif self.owner.direction == "U":
			for i in list_of_entities:
				for iterate in range(weapon_range):
					if i is not self.owner:
						if (self.owner.rect.x == i.rect.x - offset and i.rect.y == self.owner.rect.y - (iterate - 1)) or (self.owner.rect.x == i.rect.x and i.rect.y == self.owner.rect.y - (iterate + 1)) or (self.owner.rect.x == i.rect.x + offset and i.rect.y == self.owner.rect.y - (iterate + 1)):
							targets.append(i)
							

		elif self.owner.direction == "R":
			for i in list_of_entities:
				for iterate in range(weapon_range):
					if i is not self.owner:
						if (self.owner.rect.y == i.rect.y - offset and i.rect.x == self.owner.rect.x + (iterate + 1)) or (self.owner.rect.y == i.rect.y and i.rect.x == self.owner.rect.x + (iterate + 1)) or (self.owner.rect.y == i.rect.y + offset and i.rect.x == self.owner.rect.x + (iterate + 1)):
							targets.append(i)
							
		elif self.owner.direction == "L":
			for i in list_of_entities:
				for iterate in range(weapon_range):
					if i is not self.owner:
						if (self.owner.rect.y == i.rect.y - offset and i.rect.x == self.owner.rect.x - (iterate + 1)) or (self.owner.rect.y == i.rect.y and i.rect.x == self.owner.rect.x - (iterate + 1)) or (self.owner.rect.y == i.rect.y + offset and i.rect.x == self.owner.rect.x - (iterate + 1)):
							targets.append(i)
		targets = list(set(targets))				
		return targets

	def shoot(self, list_of_entities):
		targets = self.check_if_hit(list_of_entities, self.range, self.offset, self.far_range)
		for target in targets:
			damage = dam_generate(self.damage)
			target.take_damage(damage, self.owner)

# Fists, default weapon.
class Fist(Weapon):
	def __init__(self, owner):
		super().__init__(owner, "fists")

		# Damage and range variables/ unique for each weapon
		self.offset = 0
		self.range = 1
		self.far_range = 1
		self.damage = 1
		self.armour_pass = False

	def sprite_assign(self):
		# Assign the weapon sprites
		spritefunctions.SpriteSheet("data/images/player_spritesheet.png").clear_weapon_sprites(self.owner)

		# Assign the animation sprites
		spritefunctions.SpriteSheet("data/images/player_spritesheet.png").player_sprite_assign_stab(self.owner)

		self.owner.animation_type = "stab"


class Revolver(Weapon):
	def __init__(self, owner):
		super().__init__(owner, "revolver")

		# Damage and range variables/ unique for each weapon
		self.offset = 0
		self.range = 3
		self.far_range = 4
		self.damage = 3
		self.armour_pass = False

		#Used for unequipping and dropping the weapon
		self.item_form = []

	def sprite_assign(self):
		# Assign the weapon sprites
		spritefunctions.SpriteSheet("data/images/player_spritesheet.png").revolver_sprite_assign(self.owner)

		# Assign the animation sprites
		spritefunctions.SpriteSheet("data/images/player_spritesheet.png").player_sprite_assign_one(self.owner, "data/images/player_one_spritesheet.png")

		self.owner.animation_type = "one"


# All items that can be picked up from the map, or looted of of enimies are derived of this class.

class Item(pygame.sprite.Sprite):
	def __init__(self, x, y, sprite, capacity = 1):
		super().__init__()
		self.image = sprite
		self.image.set_colorkey(constants.GREEN_COLOURKEY)
		self.rect = self.image.get_rect()

		self.rect.x = x
		self.rect.y = y

		# Highlighting for consoles
		self.is_highlighted = False

		self.entity_name = "Item"
		self.capacity = capacity
		self.owner = None

	def draw(self, screen):
		screen.blit(self.image,(self.rect.x * constants.TILE_WIDTH, self.rect.y * constants.TILE_HEIGHT))

	def pick_up(self, entity, map_item_list):
		self.owner = entity
		if (len(self.owner.inventory) - 1) + self.capacity < self.owner.max_inventory:
			self.owner.inventory.append(self)
			map_item_list.remove(self)
			self.owner.message_list.append(self.owner.name + " picked up " + self.name)
		else:
			self.owner.message_list.append(self.owner.name + " cant carry any more")

	def drop(self,list_of_entities, map_item_list):
		check = map_drop_check(self.owner,map_item_list)
		if check:
			map_item_list.append(self)
			self.owner.inventory.remove(self)
			self.owner.message_list.append(self.owner.name + " dropped " + self.name)
			self.rect.x = self.owner.rect.x
			self.rect.y = self.owner.rect.y
			self.owner.has_dropped = True
			self.owner = None
		else:
			self.owner.message_list.append("Can't drop over an item.")

class Stick(Item):
	def __init__(self, x, y):
		super().__init__(x,y,constants.stick,1)
		self.name = "stick"

	def use(self):
		self.owner.message_list.append(self.owner.name + " waved the stick about...")

class MedKit(Item):
	def __init__(self, x, y):
		super().__init__(x,y,constants.med_kit,1)
		self.name = "medkit"
		self.heal_strength = 7
	def use(self):
		used = self.owner.heal(self.heal_strength)
		if used:
			self.owner.inventory.remove(self)

# Weapon item forms, used for inventory
class RevolverItem(Item):
	def __init__(self, x, y):
		super().__init__(x,y,constants.revolver,1)
		self.name = "revolver"

	def use(self):
		self.owner.equip(Revolver(self.owner), self)

# Console super class, all other forms of console below will draw from this, consoles for printing events and information to the screen.
class Console():
	# Draws the standard green txt
	def draw_text(self, surface, text, text_coordinates):
		text_surface = constants.font.render(text, True, constants.GREEN, constants.BLACK)
		text_rect = text_surface.get_rect()

		text_rect.topleft = text_coordinates

		surface.blit(text_surface, text_rect)
	# Identical but in red
	def draw_text_red(self, surface, text, text_coordinates):
		text_surface = constants.font.render(text, True, constants.RED, constants.BLACK)
		text_rect = text_surface.get_rect()

		text_rect.topleft = text_coordinates

		surface.blit(text_surface, text_rect)

	# For use when the mouse highlights an option that can be clicked
	def draw_text_highlight(self, surface, text, text_coordinates):
		text_surface = constants.font.render(text, True, constants.YELLOW_HIGHLIGHT, constants.BLACK)
		text_rect = text_surface.get_rect()

		text_rect.topleft = text_coordinates

		surface.blit(text_surface, text_rect)

	# Calculates the height of a character
	def text_height(self):
		letter = constants.font.render("a", True, constants.GREEN)
		letter_height = letter.get_rect().height
		return letter_height

	# Calclates the width of a character, useful for centering text.
	def text_width(self):
		letter = constants.font.render("a", True, constants.GREEN)
		letter_width = letter.get_rect().width
		return letter_width

class Debug_Console(Console):
	def __init__(self, screen):
		self.surface = screen

	def output(self, clock):
		self.draw_text(self.surface, "fps: " + str(int(clock.get_fps())), (0,0))

class Message_Console(Console):
	def __init__(self, screen):
		self.surface = screen

	def output(self, message_list):
		# ensure messages dont print right on top of eachover, would be bad... also illegible.
		try:
			output = message_list[-constants.AMOUNT_OF_MESSAGES_IN_LOG:]
		except IndexError:
			output = message_list

		# Coordinates of printing
		y = (constants.MAP_HEIGHT * constants.TILE_HEIGHT) - (constants.AMOUNT_OF_MESSAGES_IN_LOG * self.text_height())

		message_count = 0

		for message in output:
			self.draw_text(self.surface, message, (0, y + (message_count * self.text_height())))
			message_count += 1


# FUNCTIONS BELOW

'''
	HERE ARE ALL FUNCTIONS FOR THE PROGRAM, THINGS SUCH AS INDEPENDANT SCRIPTS, LIKE MAP GENERATION.
'''

# Generate random damage values
def dam_generate(base_dam):
	dam_to_deal = base_dam

	# Start looping three times, adding variance
	for i in range(3):
		chance = random.randrange(0,100)
		if chance < 50:
			dam_to_deal -= 1
		else:
			break

	# Deciding if its a regular, critical or bad hit
	chance = random.randrange(0,100)
	if chance < 10:
		dam_to_deal // 2
	elif chance > 90:
		dam_to_deal * 2
	else:
		pass

	# Return the final damage to deal
	return dam_to_deal

# Saving and loading functions, these functions extract and write parameters in a pythonic list to an external save file.
def load_func():
	list_to_load = pickle.load(open("savefile.p", "rb"))

	return list_to_load

def save_gameloop(player, message_list, game_map, map_item_list, all_enemy_entity):
	# Flag to ensure the correct function is called at the main menu
	loop_to_run = 1

	# Extracting the player information.
	player_variables = [player.max_health, player.name]

	# Extracting the players inventory information
	inventory_list_to_save = []
	inventory_list = player.inventory
	for i in inventory_list:
		inventory_list_to_save.append([i.name, i.rect.x, i.rect.y])

	list_to_save = [loop_to_run, player_variables, inventory_list_to_save]

	pickle.dump(list_to_save, open("savefile.p", "wb"))



# Generates the world Hub World map.
def hub_map_generate():
	new_map = [[Tile(True) for y in range(0,constants.MAP_WIDTH)] for x in range(0,constants.MAP_HEIGHT)]

	for x in range(constants.MAP_WIDTH):
		new_map[x][0].can_walk = False
		new_map[x][constants.MAP_HEIGHT - 1].can_walk = False
	for y in range(constants.MAP_HEIGHT):
		new_map[0][y].can_walk = False
		new_map[constants.MAP_WIDTH - 1][y].can_walk = False

	return new_map



# Generates the random world map.
def map_generate():


	# Generate a map of walls, to be tunneled out.
	new_map = [[Tile(False) for y in range(0,constants.MAP_WIDTH)] for x in range(0,constants.MAP_HEIGHT)]
	
	
	# The list of rooms in the map
	list_of_rooms = []

	initial_room = True

	for i in range(10):

		room_to_place = map_generate_room()
		can_place = True

		# Check the room wont collide with another room.
		for previous_room in list_of_rooms:
			if room_to_place.collide_detect(previous_room):
				can_place = False
				break
			else:
				can_place = True


		# Placing the room on the map
		if can_place:
			# Check if this is the initial room.
			if initial_room:
				room_to_place.is_initial = True

				# Place the room into the map
				for x in range(room_to_place.left, room_to_place.right):
					for y in range(room_to_place.top, room_to_place.bottom):
						new_map[x][y].can_walk = True

				list_of_rooms.append(room_to_place)

			else:
				room_to_place.is_initial = False

				# Place the room into the map
				for x in range(room_to_place.left, room_to_place.right):
					for y in range(room_to_place.top, room_to_place.bottom):
						new_map[x][y].can_walk = True


				# Ending x axis
				ending_node_x = list_of_rooms[-1].middle[0]
				# Ending y axis
				ending_node_y = list_of_rooms[-1].middle[1]

				list_of_rooms.append(room_to_place)
				# Starting x axis
				current_node_x = list_of_rooms[-1].middle[0]
				# Starting Y axis
				current_node_y = list_of_rooms[-1].middle[1]
				print(current_node_x, current_node_y)
				print(ending_node_x, ending_node_y)

				# The difference between the two rooms
				x_range = current_node_x - ending_node_x
				y_range = current_node_y - ending_node_y
				print(y_range)

			
			# Tunnelling to the previous room
			if initial_room:
				initial_room = False

			else:
				# Digging along the x axis (working edition)
				tunnel_finished = False
				while tunnel_finished == False:
					new_map[current_node_x][current_node_y].can_walk = True

					# Checking whether the tunnel should go left or right
					if x_range > 0:
						for i in range(x_range):
							current_node_x -= 1
							new_map[current_node_x][current_node_y].can_walk = True
					else:
						x_range *= -1
						for i in range(x_range):
							current_node_x += 1
							new_map[current_node_x][current_node_y].can_walk = True

					# Setting the tunneling process to finish
					tunnel_finished = True


				# Digging along the Y axis
				tunnel_finished = False
				while tunnel_finished == False:
					new_map[current_node_x][current_node_y].can_walk = True

					# Checking whether the tunnel should go left or right
					if y_range > 0:
						for i in range(y_range):
							current_node_y -= 1
							new_map[current_node_x][current_node_y].can_walk = True
					else:
						y_range *= -1
						for i in range(y_range):
							current_node_y += 1
							new_map[current_node_x][current_node_y].can_walk = True

					# Setting the tunneling process to finish
					tunnel_finished = True


				"""
					# Check which way to iterate
					if current_node_x <= room_to_place.middle[0]:
						current_node_x += 1

						if current_node_x < room_to_place.middle[0]:
							tunnel_finished = True

					else:
						current_node_x += -1
						
						if current_node_x > room_to_place.middle[0]:
							tunnel_finished = True

				# Digging along the y axis
				tunnel_finished = False
				while tunnel_finished == False:
					new_map[current_node_x][current_node_y].can_walk = True

					# Check which way to iterate
					if current_node_y <= room_to_place.middle[1]:
						current_node_y += 1

						if current_node_y > room_to_place.middle[1]:
							tunnel_finished = True

					else:
						current_node_y += -1

						if current_node_y > room_to_place.middle[1]:
							tunnel_finished = True
						"""

	return (new_map, list_of_rooms)

# Generates a single room.
def map_generate_room():

	width = random.randint(2,5)
	height = random.randint(2,5)

	x = random.randint(5, (constants.MAP_WIDTH - width) - 2)
	y = random.randint(5, (constants.MAP_HEIGHT - height) - 2)

	room = Room(x, y, width, height)
	return room


# Draws the world map to the screen.
def map_draw(map_to_draw, screen):
	for x in range(0,constants.MAP_WIDTH):
		for y in range(0,constants.MAP_HEIGHT):
			if map_to_draw[x][y].can_walk == True:
				# Draw floor
				screen.blit(constants.floor,(x * constants.TILE_WIDTH,y * constants.TILE_HEIGHT))
			else:
				screen.blit(constants.wall,(x * constants.TILE_WIDTH,y * constants.TILE_HEIGHT))

# Checks if the entitiy is over an item, and whether to pick that Item up or not.
def map_item_check(list_of_entities, map_item_list):
	for item in map_item_list:
		for entity in list_of_entities:
			if entity.has_dropped == False:
				if item.rect.x == entity.rect.x and item.rect.y == entity.rect.y:
					item.pick_up(entity,map_item_list)
					return False

def map_drop_check(entity, map_item_list):
	if entity.has_dropped == True:
		return False
	else:
		return True


def check_if_hit(self, list_of_entities, weapon_range, offset):
	targets = []
	if self.owner.direction == "D":
		for i in list_of_entities:
			for iterate in range(weapon_range):
				if i is not self.owner and self.owner.rect.x == i.rect.x - offset and self.owner.rect.x == i.rect.x and self.owner.rect.x == i.rect.x + offset and i.rect.y == self.owner.rect.y + iterate:
					targets.append(i)
	elif self.owner.direction == "U":
			for iterate in range(weapon_range):
				if i is not self.owner and self.owner.rect.x == i.rect.x - offset and self.owner.rect.x == i.rect.x and self.owner.rect.x == i.rect.x + offset and i.rect.y == self.owner.rect.y - iterate:
					targets.append(i)
	elif self.owner.direction == "R":
		for i in list_of_entities:
			if i is not self.owner and self.owner.rect.x + weapon_range == i.rect.x and i.rect.y == self.owner.rect.y:
				targets.append(i)
	elif self.owner.direction == "L":
		for i in list_of_entities:
			if i is not self.owner and self.owner.rect.x - weapon_range == i.rect.x and i.rect.y == self.owner.rect.y:
				targets.append(i)
	return targets

def check_can_walk(all_entity, x_change, y_change, player):
	for entity in all_entity:
		if player.rect.x + x_change == entity.rect.x and player.rect.y + y_change == entity.rect.y:
			return False
	return True


# Pathfinding algorith, breadth first search.
def find_path():
	frontier = queue.Queue()


"""
	ALL FUNCTIONALIY FOR NPC'S OR OTHERWISE NON PLAYER ACTIVITY.
"""
# All ai functions controlls all non player actions.
class AI():
	def __init__(self):
		pass

	def ai(self,npc,game_map,all_entity, player, map_item_list, all_enemy_entity):
		if npc.health <= 0:
			npc.die(all_entity, map_item_list, all_enemy_entity)
		else:
			# Moving towards the target
			if self.ai_distance_to_target(npc, player, game_map) > npc.weapon.range:

				self.ai_walk_towards_target(npc,player,game_map, all_entity)
			else:
				# Check npc can hit
				self.face_player(npc, player)
				npc.attack(all_entity)

	# Moves the npc in one random direction
	def ai_random(self,npc,game_map, player):
		rand_direc = random.randint(1,4)
		if rand_direc == 1:
			self.left(npc,game_map, player)
		elif rand_direc == 2:
			self.right(npc,game_map, player)
		elif rand_direc == 3:
			self.up(npc,game_map, player)
		elif rand_direc == 4:
			self.down(npc,game_map, player)

	# Defines what the NPC's target is, ie: the player to attack, or follow, another NPC or an item, or an item to then use to attack the player
	def ai_walk_towards_target(self, npc, target, game_map, all_entity):
		path_to_target = Path.path_bfs((npc.rect.x, npc.rect.y), game_map, (target.rect.x, target.rect.y), all_entity, npc)

		current = [path_to_target[0][0], path_to_target[0][1]]
		destination = [path_to_target[1][0], path_to_target[1][1]]

		# Calculate the difference ie: next location - current location
		difference_x = destination[0] - current[0]
		difference_y = destination[1] - current[1]

		if difference_y == -1 and difference_x == -1:
			npc.direction = "UL"
			self.up_left(npc, game_map, all_entity, target)
		elif difference_y == -1 and difference_x == 1:
			npc.direction = "UR"
			self.up_right(npc, game_map, all_entity, target)
		elif difference_y == 1 and difference_x == -1:
			npc.direction = "DL"
			self.down_left(npc, game_map, all_entity, target)
		elif difference_y == 1 and difference_x == 1:
			npc.direction = "DR"
			self.down_right(npc, game_map, all_entity, target)

		elif difference_y == -1:
			npc.direction = "U"
			self.up(npc, game_map, all_entity, target)
		elif difference_y == 1:
			npc.direction = "D"
			self.down(npc, game_map, all_entity, target)
		elif difference_x == 1:
			npc.direction = "R"
			self.right(npc, game_map, all_entity, target)
		elif difference_x == -1:
			npc.direction = "L"
			self.left(npc, game_map, all_entity, target)


	def ai_distance_to_target(self, npc, target, game_map):
		difference_x = target.rect.x - npc.rect.x
		difference_y = target.rect.y - npc.rect.y

		distance = math.sqrt(difference_x ** 2 + difference_y ** 2)

		return int(distance)

	def face_player(self, npc, target):
		difference_x = target.rect.x - npc.rect.x
		difference_y = target.rect.y - npc.rect.y
		if difference_y == -1 and difference_x == -1:
			npc.direction = "UL"
		elif difference_y == -1 and difference_x == 1:
			npc.direction = "UR"
		elif difference_y == 1 and difference_x == -1:
			npc.direction = "DL"
		elif difference_y == 1 and difference_x == 1:
			npc.direction = "DR"

		elif difference_y == -1:
			npc.direction = "U"
		elif difference_y == 1:
			npc.direction = "D"
		elif difference_x == 1:
			npc.direction = "R"
		elif difference_x == -1:
			npc.direction = "L"

	# All movement functions, can be referenced from elsewhere within the AI class
	def left(self, npc, game_map, all_entity, player):
		npc.update(-1,0,game_map,"L", all_entity, player)
	def right(self, npc, game_map, all_entity, player):
		npc.update(1,0,game_map,"R", all_entity, player)
	def up(self, npc,game_map, all_entity, player):
		npc.update(0,-1,game_map,"U", all_entity, player)
	def down(self, npc,game_map, all_entity, player):
		npc.update(0,1,game_map,"D", all_entity, player)

	def up_left(self, npc, game_map, all_entity, player):
		npc.update(-1,-1,game_map,"UL", all_entity, player)
	def up_right(self, npc, game_map, all_entity, player):
		npc.update(1,-1,game_map,"UR", all_entity, player)
	def down_left(self, npc, game_map, all_entity, player):
		npc.update(-1,1,game_map,"DL", all_entity, player)
	def down_right(self, npc, game_map, all_entity, player):
		npc.update(1,1,game_map,"DR", all_entity, player)