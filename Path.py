#!/usr/bin/python3.4

import queue


# User is the entity currently trying to check for where it can move.

# Start is a tuple, pointing to the current location of the user (coordinates).

# Goal is the target, could possibly be selected from a list of objects/entities in the room? 
# room by room basis.

# game_map is the game map, allows for checking of walls.

# Frontier, an ever expanding "ring" this is where neighbours are drawn from, and allows the "expansion"
# or otherwise "exploring" of all directions, searching for possible paths.

# Each node should have 8 possible nodes, ie: one for each direction of movement, both straight and diagonal, 
# these possibilities are calculated in calc_neighbours, apart from when there are walls or entities occoupying what 
# would otherwise be a clear space.

# Next, this is the name of the next variable, given in the for loop for simplicities sake I haven't used "i".



# The path function, builds the path from the start to the goal (uses breadth first search)
def path_bfs(start, game_map, goal, all_entity, own_entity):
	# The expanding "ring"
	frontier = queue.Queue()
	frontier.put(start)

	came_from = {}
	came_from[start] = None
	current = start

	while not frontier.empty():
		# Early exit flag
		if current == goal:
			break

		current = frontier.get()

		for next in calc_neighbours(current, game_map, all_entity, own_entity, goal):
			if next not in came_from:
				frontier.put(next)
				came_from[next] = current

	# After navigating the frontier, go through the nodes backwards to build the path
	current = goal
	path = [current]
	while current != start:
		current = came_from[current]
		path.append(current)
	path.reverse()

	print(path)
	return path



def calc_neighbours(current, game_map, all_entity, own_entity, goal):
	neighbours = []

	for i in range(9):
		# The parts of the coordiante to calculate neighbours
		current_x = current[0]
		current_y = current[1]

		# Straight, up, down, left and right movement
		if i == 1:
			current_x += -1
		elif i == 2:
			current_x += 1
		elif i == 3:
			current_y += -1
		elif i == 4:
			current_y += 1

		# Diagonal movement
		elif i == 5:
			current_x += -1
			current_y += -1
		elif i == 6:
			current_x += 1
			current_y += -1
		elif i == 7:
			current_x += 1
			current_y += 1
		elif i == 8:
			current_x += -1
			current_y += 1
		else:
			break

		# Possible neighbour node
		neighbour = (current_x, current_y)
		applicable = False
		# Check if that node is applicable, first check can I walk on that part of map?
		if game_map[current_x][current_y].can_walk == True:
			applicable = True

		for entity in all_entity:
			if entity.rect.x == current_x and entity.rect.y == current_y:
				applicable = False
				if entity is own_entity:
					applicable = True
				if neighbour == goal:
					applicable = True

		if applicable:	
			# Neighbour is applicable
			neighbours.append(neighbour)

	# Return all the applicable neighbours
	return neighbours