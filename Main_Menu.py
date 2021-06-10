# Main_Menu.py

# Importing other modules
import pygame
pygame.init()

# Importing my modules
import Game_Loop
import Hub_World
import game_objects
import constants
import menufunctions

# Prepping important variables before the solution is run
# Defining the window
size = [constants.MAP_WIDTH * constants.TILE_WIDTH, constants.MAP_HEIGHT * constants.TILE_HEIGHT]

# Screen variable, which solution is drawn to
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Coursework")
# Mouse is required for using the menu
pygame.mouse.set_visible(True)
# Slight delay before registering keys, keeps the solution from being unweildly (too sensitive)
pygame.key.set_repeat(50,150)

# Variables required for the main menu
# Dimesnions of the box, containing the three options
window_width = constants.MAP_WIDTH * constants.TILE_WIDTH // 2
# Makes the window tall enough for three options
window_height = game_objects.Console.text_height(None) * 3

# Coordinates display the window in the centre of the screen
window_x = constants.MAP_WIDTH * constants.TILE_WIDTH // 2 - (window_width // 2)
window_y = constants.MAP_HEIGHT * constants.TILE_HEIGHT // 2 - (window_height // 2)

window = pygame.Surface((window_width, window_height))
option = ["New  Game", "Load Game", "Quit Solution"]
option_highlight = [False, False, False]
# The main Game Loop
clock = pygame.time.Clock()
running = True
while running:
	for i in range(3):
		option_highlight[i] = False
	# Variables for tracking the mouse
	# used to detect when the mouse is clicked.
	mouse_click = False
	# Used for tracking the mouse lcation.
	mouse_pos = pygame.mouse.get_pos()
	mouse_pos_x = mouse_pos[0]
	mouse_pos_y = mouse_pos[1]

	# Event log for the menu, takes user input
	event_list = pygame.event.get()
	for event in event_list:
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_click = True

	# All updating code
	# If statements checking the mouse is within the window.
	if mouse_pos_x >= window_x and mouse_pos_x <= (window_x + window_width):
		if mouse_pos_y >= window_y and mouse_pos_y <= (window_y + window_height):
			if mouse_pos_y < window_y + game_objects.Console.text_height(None) * 1:
				option_highlight[0] = True
				if mouse_click:
					# Starting a new game
					pygame.mouse.set_visible(False)
					message_list = []
					player = game_objects.Player(6, "Emma", message_list, 0,0)
					Game_Loop.main(screen, player, message_list)
			elif mouse_pos_y < window_y + game_objects.Console.text_height(None) * 2:
				option_highlight[1] = True
				if mouse_click:
					# Loading an old game
					pygame.mouse.set_visible(False)
					list_to_load = game_objects.load_func()

					# Checking which function needs to be called
					if list_to_load[0] == 0:
						Hub_World.hub_world(screen, list_to_load[1], list_to_load[2])
					elif list_to_load[0] == 1:
						# Initialising the player
						message_list = []
						player = game_objects.Player(list_to_load[1][0], list_to_load[1][1], message_list, 0,0)

						# Initialising the inventory
						inventory = list_to_load[2]
						for i in inventory:
							if i[0] == "stick":
								player.inventory.append(game_objects.Stick(i[1], i[2]))
							elif i[0] == "medkit":
								player.inventory.append(game_objects.MedKit(i[1], i[2]))
							elif i[0] == "revolver":
								player.inventory.append(game_objects.Revolver(i[1], i[2]))

						Game_Loop.main(screen, player, message_list)

			elif mouse_pos_y < window_y + game_objects.Console.text_height(None) * 3:
				option_highlight[2] = True
				if mouse_click:
					running = False

	# All Drawing code
	# Reseting the screen for the current frame
	screen.fill(constants.BLACK)

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

pygame.quit()