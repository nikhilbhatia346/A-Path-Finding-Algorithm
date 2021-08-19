import pygame
import math
from queue import PriorityQueue

WIDTH = 800 # the window gonna be square, capital letters for the constants
WIN = pygame.display.set_mode((WIDTH, WIDTH)) # this is how big the display or window gonna be width*width
pygame.display.set_caption("A* Path Finding Algorithm") # title of the window

# color codes for making the diff path, making the diff squares, changing the colors of the things
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot: # the cubes in the grid or the nodes
	def __init__(self, row, col, width, total_rows):
		self.row = row 
		self.col = col
		self.x = row * width  # the coordinates at which we want to make the cube
		self.y = col * width
		self.color = WHITE  # in the start all the cubes will be white
		self.neighbors = []
		self.width = width 
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self, ):  # means have we looked at the cube or not
		return self.color == RED  # if we have visited the cube then we will mark it as red

	def is_open(self):
		return self.color == GREEN  

	def is_barrier(self):
		return self.color == BLACK  # if the cube is the barrier then we can't visit the cube

	def is_start(self):
		return self.color == ORANGE # The starting node or the cube will be in orange color

	def is_end(self):
		return self.color == TURQUOISE # The end node or the cube will be purple color

	def reset(self):
		self.color = WHITE # when we reset the cube back to its original state then it should be in white color

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED  # make the color of the cube red

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self): 
		self.color = PURPLE # the path from the start node to end node will be purple

	def draw(self,win): # draw the cube and the surface gonna be the win(window)
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))  #x,y are the coordinates at which we want to draw the rect of width*width

	def update_neighbors(self,grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # we are going to check that we are on the row that is 1 less than the total_rows to avoid out of bounds and if that cube is not a barrier then we can add [row+1][col] to the neighbors, this will be the bottom neighbor  
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # the top neighbor
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # the right neighbor
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # the left neighbor
			self.neighbors.append(grid[self.row][self.col - 1])


	def __lt__(self, other): # lt means less than, we are comparing the two spots the current one and the some other one and saying that the other spot is greater than this spot
		return False

def h(p1, p2): # h(heuristic) function to calc the dis between the two points p1 and p2
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2) # the manhattan dis is used to calc the distance

def reconstruct_path(came_from, current, draw): # current node is going to be end node and then move backwards
	while current in came_from: # start node is not in the came_from so it will stop there
		current = came_from[current] 
		current.make_path() # make the path
		draw() # draw the path

def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start)) # 0 is the f-score of th starting node, when we add something then we will increment count and it is like the tie-breaker when we have same nodes with same f-score then we will consider the node which came first using the count, start is the start node itself 
	came_from = {} # the previous node where we came from
	g_score = {spot:float('inf') for row in grid for spot in row}
	g_score[start] = 0 # dis of the start node from the start node is going to be 0
	f_score = {spot:float('inf') for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos()) # get the estimate dis between the start and the end node

	open_set_hash = {start} # this is used to keep track of all the items that are present in the priorityqueue and that are not

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # if the user closes the game then quit the pygame
				pygame.quit()

		current = open_set.get()[2] # the second value is the node, get the smallest element out of it everytime
		open_set_hash.remove(current) # remove the current popped node from the open_set_hash

		if current == end: # found the shortest path
			end.make_end() # this will not make the end node purple 
			reconstruct_path(came_from, end, draw)
			return True

		for neighbor in current.neighbors: # explore all the neighbors
			temp_g_score = g_score[current] + 1 # get the gscore of the current(dis from the start node) and add 1 to it bcz the all the edges have a dis of 1 and we are moving to neighbors from the current node 

			if temp_g_score < g_score[neighbor]: # if we found the shorter path than before
				came_from[neighbor] = current # update the came_from
				g_score[neighbor] = temp_g_score # update the g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor)) # put it into the priorityqueue for further process
					open_set_hash.add(neighbor) 
					neighbor.make_open() # means the neighbor is open and we can move onto that neighbor 

		draw()
		if current != start:
			current.make_closed() # make the node red and close it bcz we have considered it before

	return False


def make_grid(rows, width): # row = col, and width is the width of the entire grid
	grid = []
	gap = width // rows  # the width(gap) of the cubes in the grid 
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows) # create an object of spot and add it to the grid
			grid[i].append(spot)

	return grid

def draw_grid(win, rows, width): # used to draw the line in the grid
	gap = width // rows  
	for i in range(rows): # for the horizontal lines
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) # the last two arguments are the starting pos and the ending pos of the line
		for j in range(rows): # for the vertical lines
			pygame.draw.line(win, GREY, (j * gap, 0), (j* gap, width))

def draw(win, grid, rows, width): # used to restore everything back to its original state
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win) # call the draw function

	draw_grid(win,rows,width) # next we are going to draw grid lines on top of the spot
	pygame.display.update() # update it on the display

def get_clicked_pos(pos, rows, width): # get the pos of where we clicked, pos argument is the position of the mouse 
 	gap = width // rows
 	y, x = pos 
 	row = y // gap
 	col = x // gap

 	return row, col # the pos on what the user clicked on


def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width) # make the grid

	start = None # the starting and the ending pos in the start is None
	end = None 

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get(): # loop through all the events that happened, events can be like mouse pressed or a key is pressed on the keyboard
			if event.type == pygame.QUIT: # if we press the x button at the top right corner of the window then stop running the game
				run = False

			if pygame.mouse.get_pressed()[0]: # if the left button of the mouse is clicked then do something
				pos = pygame.mouse.get_pos() # gives the pos on the pygame mouse on the screen
				row, col = get_clicked_pos(pos, ROWS, width) # get the row,col we clicked on
				spot = grid[row][col]
				if not start and spot != end: # if the start node has not been placed yet then place it
					start = spot # the spot at which we clicked
					start.make_start() # create the start node

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # if the right button is clicked
				pos = pygame.mouse.get_pos() 
				row, col = get_clicked_pos(pos, ROWS, width) 
				spot = grid[row][col]
				spot.reset() # reset it to the original state
				if spot == start: # if right click on the start then remove the start
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end: # if the key pressed was spacebar and the algorithm has not started yet
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end) # lambda is an anonymous function, we are just calling the draw func and passing it as an argument

				# to reset the screen
				if event.key == pygame.K_c: # press lowercase 'c' then clear the screen
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit() # quit the pygame window

main(WIN, WIDTH)