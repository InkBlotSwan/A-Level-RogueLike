# File Hub_World.py

# Importing all external files
import pygame

# Importing my own files
import constants
import game_objects
import menufunctions

def hub_world(screen, player, message_list):
	pygame.init()

	# The simple, square hub world.
	game_map = game_objects.hub_map_generate()

	# Placing the player in the centre.
	player.rect.x = 5
	player.rect.y = 8

	# A list used to draw entities en masse.
	all_entity = []
	all_enemy_entity = []
	all_entity.append(player)

	# Variables for player control
	right_pressed = False
	left_pressed = False
	up_pressed = False
	down_pressed = False

	up_right_pressed = False
	up_left_pressed = False
	down_right_pressed = False
	down_left_pressed = False

	facing_iterate = 0

	# Loop variables for initialisation
	clock = pygame.time.Clock()
	index_number = 0
	iterate = 0
	running = True
	while running:
		if player.moving == False:
			player.made_action = False
		# Event processing
		if player.moving == False and player.is_turn == True:
			event_list = pygame.event.get()
			for event in event_list:
				# Closing the window
				if event.type == pygame.QUIT:
					pygame.quit()
					return False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						exit_key = menufunctions.pause_menu(screen, 1, player, message_list, game_map, map_item_list, all_enemy_entity)

						if exit_key:
							running = False

					# All player keydown movement controls

					# Event handling for going right
					if event.key == pygame.K_d:
						# Diagonal movement
						if up_pressed:
							player.direction = "UR"
							up_pressed = False
							up_right_pressed = True
						if down_pressed:
							player.direction = "DR"
							down_pressed = False
							down_right_pressed = False
						# Straight movement
						else:
							player.made_action = True
							right_pressed = True

					# Event handling for going left
					if event.key == pygame.K_a:
						# Diagonal movement
						if up_pressed:
							player.direction = "UL"
							up_pressed = False
							up_left_pressed = True
						if down_pressed:
							player.direction = "DL"
							down_pressed = False
							down_left_pressed = True
						# Straight movement
							left_pressed = True
						else:
							player.made_action = True
							left_pressed = True

					# Event handling for going up
					if event.key == pygame.K_w:
						# Diagonal movement
						if right_pressed:
							player.direction = "UR"
							right_pressed = False
							up_right_pressed = True
						if left_pressed:
							player.direction = "UL"
							left_pressed = False
							up_left_pressed = True
						# Straight movement
						else:
							player.made_action = True
							up_pressed = True

					# Event handling for going down
					if event.key == pygame.K_s:
						# Diagonal movement
						if right_pressed:
							player.direction = "DR"
							right_pressed = False
							down_right_pressed = True
						if left_pressed:
							player.direction = "DL"
							left_pressed = False
							down_left_pressed = True
						# Straight movement
						else:
							player.made_action = True
							down_pressed = True

						# Player attacks
					elif event.key == pygame.K_SPACE and player.moving == False:
						if player.moving == False and player.is_turn:
							pygame.key.set_repeat()
							pygame.key.set_repeat(50,50)
							event_list = pygame.event.get()


					# Open inventory menu
					elif event.key == pygame.K_TAB:
						pygame.key.set_repeat()
						menu = menufunctions.menu_inventory(screen, player, clock, map_item_list, messages, message_list, all_entity, game_map, fps)
						if menu == "QUIT":
							pygame.quit()
							return False
						pygame.key.set_repeat(50,50)

					# Unequip test
					elif event.key == pygame.K_r:
						player.unequip()

				# Player movement keyup controls, also used to "disengage" diagonal movement
				elif event.type == pygame.KEYUP:
					# Letup on the d key
					if event.key == pygame.K_d:
						if up_right_pressed:
							up_right_pressed = False
							up_pressed = True
						elif down_right_pressed:
							down_right_pressed = False
							down_pressed = True
						else:
							right_pressed = False

					# Letup on the a key
					elif event.key == pygame.K_a:

						if up_left_pressed:
							up_left_pressed = False
							up_pressed = True
						elif down_left_pressed:
							down_left_pressed = False
							down_pressed = False
						else:
							left_pressed = False

					# Letup on the w key
					elif event.key == pygame.K_w:
						if up_right_pressed:
							up_right_pressed = False
							right_pressed = True
						elif up_left_pressed:
							up_left_pressed = False
							left_pressed = True
						else:
							up_pressed = False

					# Letup on the s key
					elif event.key == pygame.K_s:
						if down_right_pressed:
							down_right_pressed = False
							right_pressed = True
						elif down_left_pressed:
							down_left_pressed = False
							left_pressed = True
						else:
							down_pressed = False

					# Stop the backlog of pygame keyboard inputs
					state = pygame.key.get_pressed()
					if not state[pygame.K_d]:
						right_pressed = False
						facing_iterate = 0

					if not state[pygame.K_a]:
						left_pressed = False
						facing_iterate = 0

					if not state[pygame.K_w]:
						up_pressed = False
						facing_iterate = 0

					if not state[pygame.K_s]:
						down_pressed = False
						facing_iterate = 0

		# Start Logic code
		# Checks key flags, to allow player to hold button to walk
		if not player.enemy_turn:

			# Straight movement execution
			if up_left_pressed:
				if player.moving == False:
					facing_iterate += 1
					if facing_iterate > constants.TURNING_DELAY:
						player.update(-1,-1,game_map,"UL", all_entity)
					else:
						player.direction = "UL"
			elif up_right_pressed:
				if player.moving == False:
					facing_iterate += 1
					if facing_iterate > constants.TURNING_DELAY:
						player.update(1,-1,game_map,"UR", all_entity)
					else:
						player.direction = "UR"
			elif down_left_pressed:
				if player.moving == False:
					facing_iterate += 1
					if facing_iterate > constants.TURNING_DELAY:
						player.update(-1,1,game_map,"DL", all_entity)
					else:
						player.direction = "DL"
			elif down_right_pressed:
				if player.moving == False:
					facing_iterate += 1
					if facing_iterate > constants.TURNING_DELAY:
						player.update(1,1,game_map,"DR", all_entity)
					else:
						player.direction = "DR"

			if right_pressed:
				if player.moving == False:
					facing_iterate += 1
					if facing_iterate > constants.TURNING_DELAY:
						player.update(1,0,game_map,"R", all_entity)
					else:
						player.direction = "R"
			elif left_pressed:
				if player.moving == False:
					facing_iterate += 1
					if facing_iterate > constants.TURNING_DELAY:
						player.update(-1,0,game_map,"L", all_entity)
					else:
						player.direction = "L"
			elif up_pressed:
				if player.moving == False:
					facing_iterate += 1
					if facing_iterate > constants.TURNING_DELAY:
						player.update(0,-1,game_map,"U", all_entity)
					else:
						player.direction = "U"
			elif down_pressed:
				if player.moving == False:
					facing_iterate += 1
					if facing_iterate > constants.TURNING_DELAY:
						player.update(0,1,game_map,"D", all_entity)
					else:
						player.direction = "D"


		if player.animation_finished == True:
			player.animation_finished = False

		# Allows the turnbased system
		if player.enemy_turn:
			# passing control back to player
			if index_number == (len(all_enemy_entity) - 1):
				all_enemy_entity[index_number].is_last = True
				# checking whether to run a command
			if iterate < 40:
				iterate += 1
				try:
					if all_enemy_entity[index_number].moving == False:
						game_objects.AI().ai(all_enemy_entity[index_number],game_map,all_entity, player, map_item_list, all_enemy_entity)
				except IndexError:
					index_number = 0
					player.enemy_turn = False

			else:
				index_number += 1
				iterate = 0



			if len(all_enemy_entity) <= 0:
				player.is_turn = True	

		# Drawing section.
		screen.fill(constants.BLACK)
		game_objects.map_draw(game_map,screen)

		# Draw all entities
		for i in all_entity:
			if i.moving == True:
				if i.walking:
					i.play_animation_walking(player)
				elif i.attacking:
					if i.animation_type == "stab":
						i.play_animation_attacking_stab(player)
					elif i.animation_type == "one":
						i.play_animation_attacking_one(player)
			i.draw(screen)

		pygame.display.flip()
		clock.tick(constants.FPS)