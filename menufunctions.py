# File menufunctions.py

import pygame
pygame.init()

import game_objects
import constants

# Utilities for pause menus, inventory, and dialogue.
def menu_inventory(screen, player, clock, map_items_list, messages, message_list, all_entity, game_map, fps):
	menu_open = True
	pygame.mouse.set_visible(True)

	# Variables for the window.
	# Text variables

	# Size of the inventory window.
	width = (game_objects.Console.text_width(None) * 10)
	height = (game_objects.Console.text_height(None) * 10)

	# Location of the inventory window.
	x_coordinate = 0
	y_coordinate = (constants.MAP_HEIGHT * constants.TILE_HEIGHT // 2) - (height // 2)

	window = pygame.Surface((width, height))

	# Contents of inventory.
	inventory = []
	# Loop for the menu
	while menu_open:
		mouse_click = False
		for event in pygame.event.get():
			# Closing the window
			if event.type == pygame.QUIT:
				pygame.quit()
				return "quit"
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					return "QUIT"
				# Exit the menu
				if event.key == pygame.K_TAB:
					pygame.mouse.set_visible(False)
					menu_open = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_click = True
		# Locic code below here
		# Getting mouse coordinates.
		mouse_pos = pygame.mouse.get_pos()
		mouse_pos_x = mouse_pos[0]
		mouse_pos_y = mouse_pos[1] - y_coordinate

		# Is the mouse over an item?
		for i in player.inventory:
			i.is_highlighted = False
		if mouse_pos_x <= width:
			if mouse_pos_y <= game_objects.Console.text_height(None) * 1:
				pass
			elif mouse_pos_y <= game_objects.Console.text_height(None) * 2:
				try:
					player.inventory[0].is_highlighted = True
				except IndexError:
					pass
				if mouse_click:
					try:
						menu_open = menu_use_or_drop(screen, player.inventory[0], clock, y_coordinate, width, map_items_list, messages, message_list, fps, all_entity, game_map, window)
					except IndexError:
						pass
			elif mouse_pos_y <= game_objects.Console.text_height(None) * 3:
				try:
					player.inventory[1].is_highlighted = True
				except IndexError:
					pass
				if mouse_click:
					try:
						menu_open = menu_use_or_drop(screen, player.inventory[1], clock, y_coordinate, width, map_items_list, messages, message_list, fps, all_entity, game_map, window)
					except IndexError:
						pass
			elif mouse_pos_y <= game_objects.Console.text_height(None) * 4:
				try:
					player.inventory[2].is_highlighted = True
				except IndexError:
					pass
				if mouse_click:
					try:
						menu_open = menu_use_or_drop(screen, player.inventory[2], clock, y_coordinate, width, map_items_list, messages, message_list, fps, all_entity, game_map, window)
					except IndexError:
						pass
			elif mouse_pos_y <= game_objects.Console.text_height(None) * 5:
				try:
					player.inventory[3].is_highlighted = True
				except IndexError:
					pass
				if mouse_click:
					try:
						menu_open = menu_use_or_drop(screen, player.inventory[3], clock, y_coordinate, width, map_items_list, messages, message_list, fps, all_entity, game_map, window)
					except IndexError:
						pass
			elif mouse_pos_y <= game_objects.Console.text_height(None) * 6:
				try:
					player.inventory[4].is_highlighted = True
				except IndexError:
					pass
				if mouse_click:
					try:
						menu_open = menu_use_or_drop(screen, player.inventory[4], clock, y_coordinate, width, map_items_list, messages, message_list, fps, all_entity, game_map, window)
					except IndexError:
						pass
			elif mouse_pos_y <= game_objects.Console.text_height(None) * 7:
				try:
					player.inventory[5].is_highlighted = True
				except IndexError:
					pass
				if mouse_click:
					try:
						menu_open = menu_use_or_drop(screen, player.inventory[5], clock, y_coordinate, width, map_items_list, messages, message_list, fps, all_entity, game_map, window)
					except IndexError:
						pass
			elif mouse_pos_y <= game_objects.Console.text_height(None) * 8:
				try:
					player.inventory[6].is_highlighted = True
				except IndexError:
					pass
				if mouse_click:
					try:
						menu_open = menu_use_or_drop(screen, player.inventory[6], clock, y_coordinate, width, map_items_list, messages, message_list, fps, all_entity, game_map, window)
					except IndexError:
						pass
			elif mouse_pos_y <= game_objects.Console.text_height(None) * 9:
				try:
					player.inventory[7].is_highlighted = True
				except IndexError:
					pass
				if mouse_click:
					try:
						menu_open = menu_use_or_drop(screen, player.inventory[7], clock, y_coordinate, width, map_items_list, messages, message_list, fps, all_entity, game_map, window)
					except IndexError:
						pass
			elif mouse_pos_y <= game_objects.Console.text_height(None) * 10:
				try:
					player.inventory[8].is_highlighted = True
				except IndexError:
					pass
				if mouse_click:
					try:
						menu_open = menu_use_or_drop(screen, player.inventory[8], clock, y_coordinate, width, map_items_list, messages, message_list, fps, all_entity, game_map, window)
					except IndexError:
						pass
			elif mouse_pos_y <= game_objects.Console.text_height(None) * 11:
				try:
					player.inventory[9].is_highlighted = True
				except IndexError:
					pass
				if mouse_click:
					try:
						menu_open = menu_use_or_drop(screen, player.inventory[9], clock, y_coordinate, width, map_items_list, messages, message_list, fps, all_entity, game_map, window)
					except IndexError:
						pass

		mouse_click = False
		# End logic code

		# Drawing code below here
		screen.fill(constants.BLACK)
		game_objects.map_draw(game_map,screen)

		# Draw the item dropped
		for i in map_items_list:
			i.draw(screen)

		# Draw entities over items
		for i in all_entity:
			i.draw(screen)
		messages.output(message_list)

		# Drawing the menu
		window.fill(constants.BLACK)
		window.set_alpha(150)
		game_objects.Console.draw_text(None,window,"Inventory:",(0,0))
		iterate = 1
		for i in player.inventory:
			if i.is_highlighted == False:
				game_objects.Console.draw_text(None,window,i.name,(0, (player.inventory.index(i) + 1) + game_objects.Console.text_height(None) * iterate))
			else:
				game_objects.Console.draw_text_highlight(None,window,i.name,(0, (player.inventory.index(i) + 1) + game_objects.Console.text_height(None) * iterate))
			iterate += 1
		screen.blit(window,(x_coordinate,y_coordinate))

		fps.output(clock)

		# End of Drawing code
		pygame.display.flip()
		clock.tick(constants.FPS)

def menu_use_or_drop(screen, item, clock, y_coordinate, x_coordinate, map_items_list, messages, message_list, fps, all_entity, game_map, menu):
	running = True

	width = (game_objects.Console.text_width(None) * 15)
	height = (game_objects.Console.text_height(None) * 4)

	# Location of the inventory window.

	window = pygame.Surface((width, height))

	terms = []
	use_highlight = False
	terms.append(use_highlight)
	drop_highlight = False
	terms.append(drop_highlight)

	while running:
		mouse_click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return "quit"
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					return "QUIT"
				# Exit the menu
				if event.key == pygame.K_TAB:
					running = False
			# Check for mouse click
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_click = True

		# Start Logic code
		mouse_pos = pygame.mouse.get_pos()
		mouse_pos_x = mouse_pos[0] - x_coordinate
		mouse_pos_y = mouse_pos[1] - y_coordinate

		terms[0] = False
		terms[1] = False
		# Deciding what to higlight and taking input
		if mouse_pos_x <= width:
			if mouse_pos_y <= game_objects.Console.text_height(None) * 2:
				pass
			elif mouse_pos_y <= game_objects.Console.text_height(None) * 3:
				terms[0] = True
				if mouse_click:
					item.use()
					pygame.mouse.set_visible(False)
					return False
			elif mouse_pos_y <= game_objects.Console.text_height(None) * 4:
				terms[1] = True
				if mouse_click:
					item.drop(all_entity, map_items_list)
					pygame.mouse.set_visible(False)
					return False

		mouse_click = False
		# End Logic code

		# Start Drawing code
		# Drawing the menu
		screen.fill(constants.BLACK)
		game_objects.map_draw(game_map,screen)
		for i in map_items_list:
			i.draw(screen)

		# Draw entities over items
		for i in all_entity:
			i.draw(screen)
		messages.output(message_list)

		screen.blit(menu,(0,y_coordinate))
		fps.output(clock)
		window.fill(constants.BLACK)
		window.set_alpha(150)
		game_objects.Console.draw_text(None,window,"What to do with",(0,0))
		game_objects.Console.draw_text(None,window,item.name + "?",(0,game_objects.Console.text_height(None) * 1))

		# Highlighting options
		if terms[0] == False:
			game_objects.Console.draw_text(None,window,"Use:",(0,game_objects.Console.text_height(None) * 2))
		else:
			game_objects.Console.draw_text_highlight(None,window,"Use:",(0,game_objects.Console.text_height(None) * 2))
		if terms[1] == False:
			game_objects.Console.draw_text(None,window,"Drop:",(0,game_objects.Console.text_height(None) * 3))
		else:
			game_objects.Console.draw_text_highlight(None,window,"Drop:",(0,game_objects.Console.text_height(None) * 3))
		screen.blit(window,(x_coordinate,y_coordinate))

		# End drawing code
		pygame.display.flip()
		clock.tick(constants.FPS)

def pause_menu(screen, hub_or_loop, player, message_list, game_map, map_item_list, all_enemy_entity):
	pygame.mouse.set_visible(True)

	# Variables required for the pause menu
	# Dimesnions of the box, containing the three options
	window_width = constants.MAP_WIDTH * constants.TILE_WIDTH // 2
	# Makes the window tall enough for three options
	window_height = game_objects.Console.text_height(None) * 3

	# Coordinates display the window in the centre of the screen
	window_x = constants.MAP_WIDTH * constants.TILE_WIDTH // 2 - (window_width // 2)
	window_y = constants.MAP_HEIGHT * constants.TILE_HEIGHT // 2 - (window_height // 2)

	window = pygame.Surface((window_width, window_height))
	option = ["Save Game", "Resume Game", "Quit Game"]
	option_highlight = [False, False, False]

	# used to detect when the mouse is clicked.
	mouse_click = False

	# Variables for the loop
	running = True
	clock = pygame.time.Clock()
	while running:
		for i in range(3):
			option_highlight[i] = False

		# Variables to keep track of the mouse location.
		mouse_pos = pygame.mouse.get_pos()
		mouse_pos_x = mouse_pos[0]
		mouse_pos_y = mouse_pos[1]

		event_list = pygame.event.get()
		for event in event_list:
			if event.type == pygame.QUIT:
				pass
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_click = True

		# Updating code
		# If statements checking the mouse is within the window.
		if mouse_pos_x >= window_x and mouse_pos_x <= (window_x + window_width):
			if mouse_pos_y >= window_y and mouse_pos_y <= (window_y + window_height):
				if mouse_pos_y < window_y + game_objects.Console.text_height(None) * 1:
					option_highlight[0] = True
					if mouse_click:
						# Saving the game
						pygame.mouse.set_visible(False)

						# Checking which save function to use, 0 = Hubworl 1 = Game Loop.
						if hub_or_loop == 0:
							game_objects.save_hubworld()
						elif hub_or_loop == 1:
							game_objects.save_gameloop(player, message_list, game_map, map_item_list, all_enemy_entity)

						running = False

				elif mouse_pos_y < window_y + game_objects.Console.text_height(None) * 2:
					option_highlight[1] = True
					if mouse_click:
						# Resuming the game
						running = False

				elif mouse_pos_y < window_y + game_objects.Console.text_height(None) * 3:
					option_highlight[2] = True
					if mouse_click:
						# Quitting to menu
						return True


		# Drawing code
		# Drawing the window
		window.fill(constants.BLACK)
		
		# Displaying the first option
		if option_highlight[0] == True:
			game_objects.Console.draw_text_highlight(None,window,option[0],((window_width // 2) - game_objects.Console.text_width(None) * (len(option[0]) // 2), game_objects.Console.text_height(None) * 0))
		else:
			game_objects.Console.draw_text(None,window,option[0],((window_width // 2) - game_objects.Console.text_width(None) * (len(option[0]) // 2), game_objects.Console.text_height(None) * 0))
		# Displaying the second option
		if option_highlight[1] == True:
			game_objects.Console.draw_text_highlight(None,window,option[1],((window_width // 2) - game_objects.Console.text_width(None) * (len(option[1]) // 2), game_objects.Console.text_height(None) * 1))
		else:
			game_objects.Console.draw_text(None,window,option[1],((window_width // 2) - game_objects.Console.text_width(None) * (len(option[1]) // 2), game_objects.Console.text_height(None) * 1))
		# Displaying the third option
		if option_highlight[2] == True:
			game_objects.Console.draw_text_highlight(None,window,option[2],((window_width // 2) - game_objects.Console.text_width(None) * (len(option[2]) // 2), game_objects.Console.text_height(None) * 2))
		else:
			game_objects.Console.draw_text(None,window,option[2],((window_width // 2) - game_objects.Console.text_width(None) * (len(option[2]) // 2), game_objects.Console.text_height(None) * 2))
		
		# Drawing to the screen
		screen.blit(window, (window_x, window_y))
		pygame.display.flip()

		clock.tick(constants.FPS)