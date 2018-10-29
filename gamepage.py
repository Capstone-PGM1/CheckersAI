from typing import List, Any, Union, Tuple

import pygame, sys, time, pygame_textinput
from tiles import *

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
currSec = 0
currFrame = 0
FPS = 0
tile_size = 80
w = 80

light_green = (83, 249, 88)
black_color = (0, 0, 0)
black_outline = (50, 47, 47)
red_color = (255, 0, 0)
red_outline = (181, 13, 13)
gold_color = (233, 218, 10)
gold_outline = (216, 171, 23)
tan_color = (242, 221, 179)
tan_highlight = (242, 235, 222)

# checker positions
pos1 = (250, 170)
pos2 = (410, 170)
pos3 = (570, 170)
pos4 = (730, 170)
pos5 = (170, 250)
pos6 = (330, 250)
pos7 = (490, 250)
pos8 = (650, 250)
pos9 = (250, 330)
pos10 = (410, 330)
pos11 = (570, 330)
pos12 = (730, 330)

pos13 = (170, 570)
pos14 = (330, 570)
pos15 = (490, 570)
pos16 = (650, 570)
pos17 = (250, 650)
pos18 = (410, 650)
pos19 = (570, 650)
pos20 = (730, 650)
pos21 = (170, 730)
pos22 = (330, 730)
pos23 = (490, 730)
pos24 = (650, 730)

# Gameboard squares

board1 = [210, 130]
board2 = [370, 130]
board3 = [530, 130]
board4 = [690, 130]
board5 = [130, 210]
board6 = [290, 210]
board7 = [450, 210]
board8 = [610, 210]
board9 = [210, 290]
board10 = [370, 290]
board11 = [530, 290]
board12 = [690, 290]
board13 = [130, 370]
board14 = [290, 370]
board15 = [450, 370]
board16 = [610, 370]
board17 = [210, 450]
board18 = [370, 450]
board19 = [530, 450]
board20 = [690, 450]
board21 = [130, 530]
board22 = [290, 530]
board23 = [450, 530]
board24 = [610, 530]
board25 = [210, 610]
board26 = [370, 610]
board27 = [530, 610]
board28 = [690, 610]
board29 = [130, 690]
board30 = [290, 690]
board31 = [450, 690]
board32 = [610, 690]

blackChecks= [board1, board2, board3, board4, board5, board6, board7, board8, board9, board10,
			  board11, board12, board13, board14, board15, board16, board17, board18, board19,
			  board20, board21, board22, board23, board24, board25, board26, board27, board28,
			  board29, board30, board31, board32]

# create the background
wood = pygame.image.load("wood.jpg")
wood = pygame.transform.scale(wood, (1200, 900))
Wood = pygame.Surface(wood.get_size(), pygame.HWSURFACE)
Wood.blit(wood, (0, 0))
del wood

grid = [[1]*16 for n in range(16)]
mouseX, mouseY = pygame.mouse.get_pos()

def draw_grid():
	# r, c = 1, 1
	# grid_map = []
	x, y = -30, -30
	for row in grid:
		for col in row:
			pygame.draw.rect(window, black_color, (x, y, w, w), 1)
			x = x + w
			# grid_map.append((r, c))
			# c += 1
		y = y + w
		x = -30
		# r += 1
		# c = 1
	# return grid_map
	window.blit(Wood, (0, 0))


# create game window - will make maximize button later
def create_window():
	global window, window_height, window_width, window_title
	window_width, window_height = 1200, 900
	window_title = "Checkers"
	pygame.display.set_caption(window_title)
	# hardeware/doublebug mode to make things smoother
	window = pygame.display.set_mode((window_width, window_height), pygame.HWSURFACE|pygame.DOUBLEBUF)

def load_white_tiles(lower1, upper1, lower2, upper2, n):
	for i in range(n):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.whiteTile, (x, y))
				pygame.draw.rect(window, black_color, (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

def load_grey_tiles(lower1, upper1, lower2, upper2, n):
	for i in range(n):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.greyTile, (x, y))
				pygame.draw.rect(window, black_color, (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

def load_board():
	# draw white tiles
	draw_grid()

	lower = 130
	upper = 210

	for i in range(8):
		for x in range(lower, upper, tile_size):
			for y in range(lower, upper , tile_size):
				window.blit(Tiles.whiteTile, (x, y))
				pygame.draw.rect(window, black_color, (x, y, tile_size, tile_size), 1)
			lower += 80
			upper += 80

	lower1, upper1, lower2, upper2, = 290, 370, 130, 210
	load_white_tiles(lower1, upper1, lower2, upper2, 6)

	lower1, upper1, lower2, upper2, =  450, 530, 130, 210
	load_white_tiles(lower1, upper1, lower2, upper2, 4)

	lower1, upper1, lower2, upper2, = 610, 692, 130, 210
	load_white_tiles(lower1, upper1, lower2, upper2, 1)

	lower1, upper1, lower2, upper2, = 130, 210, 290, 370
	load_white_tiles(lower1, upper1, lower2, upper2, 6)

	lower1, upper1, lower2, upper2, = 130, 210, 450, 530
	load_white_tiles(lower1, upper1, lower2, upper2, 4)

	lower1, upper1, lower2, upper2, = 130, 210, 610, 690
	load_white_tiles(lower1, upper1, lower2, upper2, 2)

	#draw grey tiles
	lower1, upper1, lower2, upper2, = 210, 290, 130, 210
	load_grey_tiles(lower1, upper1, lower2, upper2, 7)

	lower1, upper1, lower2, upper2, =  370, 450, 130, 210
	load_grey_tiles(lower1, upper1, lower2, upper2, 5)

	lower1, upper1, lower2, upper2, = 530, 610, 130, 210
	load_grey_tiles(lower1, upper1, lower2, upper2, 3)

	lower1, upper1, lower2, upper2, = 690, 770, 130, 210
	load_grey_tiles(lower1, upper1, lower2, upper2, 1)

	lower1, upper1, lower2, upper2, = 130, 210, 210, 290
	load_grey_tiles(lower1, upper1, lower2, upper2, 7)

	lower1, upper1, lower2, upper2, = 130, 210, 370, 450
	load_grey_tiles(lower1, upper1, lower2, upper2, 5)

	lower1, upper1, lower2, upper2, = 130, 210, 530, 610
	load_grey_tiles(lower1, upper1, lower2, upper2, 3)

	lower1, upper1, lower2, upper2, = 130, 210, 690, 770
	load_grey_tiles(lower1, upper1, lower2, upper2, 1)

# game boarder
	for x in range(110, 130, 20):
		for y in range(130, 770 , 20):
			window.blit(Tiles.blackTile, (x, y))

	for x in range(770, 790, 20):
		for y in range(130, 770 , 20):
			window.blit(Tiles.blackTile, (x, y))

	for x in range(110, 790, 20):
		for y in range(110, 130 , 20):
			window.blit(Tiles.blackTile, (x, y))

	for x in range(110, 790, 20):
		for y in range(770, 790 , 20):
			window.blit(Tiles.blackTile, (x, y))

class Pieces(object):
	def __init__(self):
		self.r1 = pygame.draw.circle(window, red_outline, (250, 170), 37, 37)
		self.p1 = pygame.draw.circle(window, red_color, (250, 170), 30, 30)

	# def handle_mouse(self):
	# 	for e in pygame.event.get():
		# if e.type == pygame.QUIT:
		# 	isRunning = False
		# 	pygame.quit()
		# 	sys.exit()
		# elif e.type == pygame.MOUSEBUTTONDOWN:
		# 	col = (pos[0] - 50)// 80
		# 	row = (pos[1] - 50) // 80
		# 	# Debug prints
		# 	print("Click ", pos, "Grid coordinates: ", row, col)
		# 	# grid[row][col] = 1
	#
	# def move_piece(self, x, y):
	# 	self.r1 = self.r1.move(x*self.dist, y*self.dist); pygame.draw.circle(window, red_outline, (250, 170), 37, 37)
	# 	pygame.display.update()


	def player_color(color):
		# if player color is black
		if (color == 1):
			# initial red checkers
			lower = 250
			upper = 170
			for i in range(4):
				pygame.draw.circle(window, red_outline, (lower, upper), 37, 37)
				pygame.draw.circle(window, red_color, (lower, upper), 30, 30)
				lower += 160

			lower = 170
			upper = 250
			for i in range(4):
				pygame.draw.circle(window, red_outline, (lower, upper), 37, 37)
				pygame.draw.circle(window, red_color, (lower, upper), 30, 30)
				lower += 160

			lower = 250
			upper = 330
			for i in range(4):
				pygame.draw.circle(window, red_outline, (lower, upper), 37, 37)
				pygame.draw.circle(window, red_color, (lower, upper), 30, 30)
				lower += 160


			# initial black checkers
			lower = 170
			upper = 570
			for i in range(4):
				pygame.draw.circle(window, black_outline, (lower, upper), 37, 37)
				pygame.draw.circle(window, black_color, (lower, upper), 30, 30)
				lower += 160

			lower = 250
			upper = 650
			for i in range(4):
				pygame.draw.circle(window, black_outline, (lower, upper), 37, 37)
				pygame.draw.circle(window, black_color, (lower, upper), 30, 30)
				lower += 160

			lower = 170
			upper = 730
			for i in range(4):
				pygame.draw.circle(window, black_outline, (lower, upper), 37, 37)
				pygame.draw.circle(window, black_color, (lower, upper), 30, 30)
				lower += 160
		# if player color is red
		else:


			# initial red checkers
			lower = 250
			upper = 170
			for i in range(4):
				pygame.draw.circle(window, black_outline, (lower, upper), 37, 37)
				pygame.draw.circle(window, black_color, (lower, upper), 30, 30)
				lower += 160

			lower = 170
			upper = 250
			for i in range(4):
				pygame.draw.circle(window, black_outline, (lower, upper), 37, 37)
				pygame.draw.circle(window, black_color, (lower, upper), 30, 30)
				lower += 160

			lower = 250
			upper = 330
			for i in range(4):
				pygame.draw.circle(window, black_outline, (lower, upper), 37, 37)
				pygame.draw.circle(window, black_color, (lower, upper), 30, 30)
				lower += 160


			# initial black checkers
			lower = 170
			upper = 570
			for i in range(4):
				pygame.draw.circle(window, red_outline, (lower, upper), 37, 37)
				pygame.draw.circle(window, red_color, (lower, upper), 30, 30)
				lower += 160

			lower = 250
			upper = 650
			for i in range(4):
				pygame.draw.circle(window, red_outline, (lower, upper), 37, 37)
				pygame.draw.circle(window, red_color, (lower, upper), 30, 30)
				lower += 160

			lower = 170
			upper = 730
			for i in range(4):
				pygame.draw.circle(window, red_outline, (lower, upper), 37, 37)
				pygame.draw.circle(window, red_color, (lower, upper), 30, 30)
				lower += 160

def highlight_checkers(pieces):

	for i in range(len (pieces)):
		p = pieces[i]
		t = p[1]
		lower = t[0]
		upper = t[1]
		pygame.draw.circle(window, light_green, (lower, upper), 38, 2)

def highlight_available_moves(availableMoves):
	for i in range(len(availableMoves)):
		lower = availableMoves[i][0]
		upper = availableMoves[i][1]
		pygame.draw.rect(window, light_green, (lower, upper, tile_size, tile_size), 2)

def load_chatbox(gamestate):
	if gamestate == 1:

		for x in range(875, 1095, tile_size):
			for y in range(280, 630 , tile_size):
				window.blit(Tiles.tanTile, (x, y))

		pygame.draw.rect(window, (108, 64, 7), [875, 580, 240, 100], 3)
	else:
		return

def king_piece(gamePiece, position):
	xPos, yPos = position
	window.blit(crown, (xPos - 27, yPos - 17))

# https://pythonprogramming.net/pygame-button-function/
def button(msg, x, y, w, h, ic, ac, action):
	cur = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x + w > cur[0] > x and y + h > cur[1] > y:
		pygame.draw.rect(window, ac, (x, y, w, h))
		if click[0] == 1 and action != None:
			if action == "quit":
				pygame.quit()
				sys.exit()
	else:
		pygame.draw.rect(window, ic, (x, y, w, h))
	# text_to_button(text, black, x, y, w, h)

def renderText(fontSize, message, color, position):
	myfont = pygame.font.SysFont('Comic Sans MS', fontSize)
	textsurface = myfont.render(message, False, color)
	window.blit(textsurface, position)


def loadLogo():
	pygame.draw.circle(window, black_outline, (900, 300), 180, 180)
	pygame.draw.circle(window, black_color, (900, 300), 160, 160)
	pygame.draw.circle(window, red_outline, (700, 300), 180, 180)
	pygame.draw.circle(window, red_color, (700, 300), 160, 160)
	pygame.draw.circle(window, black_outline, (500, 300), 180, 180)
	pygame.draw.circle(window, black_color, (500, 300), 160, 160)
	pygame.draw.circle(window, red_outline, (300, 300), 180, 180)
	pygame.draw.circle(window, red_color, (300, 300), 160, 160)
	renderText(200, "Checkers", gold_color, (300, 230))

def loadGamePage():
# draw checkers board
	black = 1
	red = 0
	online = 1
	offline = 0
	load_board()
	button("settings", 1090, 20, 100, 40, tan_color, tan_highlight, 'quit')
	renderText(30, "Settings", black_color, (1100, 30))
	button("quit", 1090, 850, 100, 40, tan_color, tan_highlight, 'quit')
	renderText(30, "Quit", black_color, (1115, 860))
	# player_color(black)
	load_chatbox(online)

	gamePiece1 = [1, pos1]
	gamePiece2 = [2, pos2]
	gamePiece3 = [3, pos3]
	gamePiece4 = [4, pos4]
	gamePiece5 = [5, pos5]
	gamePiece6 = [6, pos6]
	gamePiece7 = [7, pos7]
	gamePiece8 = [8, pos8]
	gamePiece9 = [9, pos9]
	gamePiece10 = [10, pos10]
	gamePiece11 = [11, pos11]
	gamePiece12 = [12, pos12]

	gamePiece13 = [13, pos13]
	gamePiece14 = [14, pos14]
	gamePiece15 = [15, pos15]
	gamePiece16 = [16, pos16]
	gamePiece17 = [17, pos17]
	gamePiece18 = [18, pos18]
	gamePiece19 = [19, pos19]
	gamePiece20 = [20, pos20]
	gamePiece21 = [21, pos21]
	gamePiece22 = [22, pos22]
	gamePiece23 = [23, pos23]
	gamePiece24 = [24, pos24]

	validCheckers = [gamePiece13, gamePiece14, gamePiece15, gamePiece16]
	highlight_checkers(validCheckers)


	# king_piece(gamePiece, pos3)

def loadPlayerChoicePage():
	loadLogo()
	button("player1", 250, 600, 300, 60, tan_color, tan_highlight, 'quit')
	renderText(60, "1-Player", black_color, (320, 610))
	button("player2", 650, 600, 300, 60, tan_color, tan_highlight, 'quit')
	renderText(60, "2-Player", black_color, (720, 610))
	button("quit", 1090, 850, 100, 40, tan_color, tan_highlight, 'quit')
	renderText(30, "Quit", black_color, (1115, 860))
	button("settings", 1090, 20, 100, 40, tan_color, tan_highlight, 'quit')
	renderText(30, "Settings", black_color, (1100, 30))

def loadLoginPage():
	loadLogo()
	button("settings", 1090, 20, 100, 40, tan_color, tan_highlight, 'quit')
	renderText(30, "Settings", black_color, (1100, 30))
	button("quit", 1090, 850, 100, 40, tan_color, tan_highlight, 'quit')
	renderText(30, "Quit", black_color, (1115, 860))
	pygame.draw.rect(window, tan_color, [450, 600, 300, 40])
	renderText(30, "Username", black_color, (450, 580))
	pygame.draw.rect(window, tan_color, [450, 680, 300, 40])
	renderText(30, "Password", black_color, (450, 660))

def loadOnePlayerPage():
	pygame.draw.rect(window, tan_color, [200, 50, 800, 200])
	renderText(150, "New Game", black_color, (340, 100))
	button("easy", 450, 300, 300, 60, tan_color, tan_highlight, 'quit')
	renderText(60, "Easy", black_color, (545, 310))
	button("medium", 450, 410, 300, 60, tan_color, tan_highlight, 'quit')
	renderText(60, "Medium", black_color, (520, 420))
	button("hard", 450, 520, 300, 60, tan_color, tan_highlight, 'quit')
	renderText(60, "Hard", black_color, (545, 530))

	renderText(60, "Select color", black_color, (480, 650))

	pygame.draw.circle(window, red_outline, (530, 770), 60, 60)
	pygame.draw.circle(window, red_color, (530, 770), 50, 50)
	pygame.draw.circle(window, black_outline, (670, 770), 60, 60)
	pygame.draw.circle(window, black_color, (670, 770), 50, 50)

	button("settings", 1090, 20, 100, 40, tan_color, tan_highlight, 'quit')
	renderText(30, "Settings", black_color, (1100, 30))
	button("quit", 1090, 850, 100, 40, tan_color, tan_highlight, 'quit')
	renderText(30, "Quit", black_color, (1115, 860))

def loadTwoPlayerPage():
	pygame.draw.rect(window, tan_color, [200, 50, 800, 200])
	renderText(150, "New Game", black_color, (340, 100))
	button("LocalGame", 200, 300, 300, 60, tan_color, tan_highlight, 'quit')
	renderText(60, "Local Game", black_color, (230, 310))
	button("PlayOnline", 700, 300, 300, 60, tan_color, tan_highlight, 'quit')
	renderText(60, "Play Online", black_color, (740, 310))
	button("quit", 1090, 850, 100, 40, tan_color, tan_highlight, 'quit')
	renderText(30, "Quit", black_color, (1115, 860))
	button("settings", 1090, 20, 100, 40, tan_color, tan_highlight, 'quit')
	renderText(30, "Settings", black_color, (1100, 30))

	pygame.draw.rect(window, tan_color, [700, 400, 300, 250])

	button("player1", 420, 800, 150, 40, tan_color, tan_highlight, 'quit')
	renderText(40, "Accept", black_color, (450, 805))
	button("player2", 630, 800, 150, 40, tan_color, tan_highlight, 'quit')
	renderText(40, "Decline", black_color, (655, 805))

def loadWinPage(color):
	move = 80
	if color == 1:
		winnerColor1 = red_outline
		winnerColor2 = red_color
	else:
		winnerColor1 = black_outline
		winnerColor2 = black_color

	pygame.draw.circle(window, winnerColor1, (100, 100), 90, 90)
	pygame.draw.circle(window, winnerColor2, (100, 100), 80, 80)
	pygame.draw.circle(window, winnerColor1, (1100, 100), 90, 90)
	pygame.draw.circle(window, winnerColor2, (1100, 100), 80, 80)
	pygame.draw.circle(window, winnerColor1, (100, 800), 90, 90)
	pygame.draw.circle(window, winnerColor2, (100, 800), 80, 80)
	pygame.draw.circle(window, winnerColor1, (1100, 800), 90, 90)
	pygame.draw.circle(window, winnerColor2, (1100, 800), 80, 80)
	renderText(50, "Play", gold_color, (1060, 760))
	renderText(50, "Again", gold_color, (1050, 800))

	pygame.draw.circle(window, gold_outline, (300, 800), 60, 60)
	pygame.draw.circle(window, gold_color, (300, 800), 50, 50)
	pygame.draw.circle(window, gold_outline, (450, 800), 60, 60)
	pygame.draw.circle(window, gold_color, (450, 800), 50, 50)
	pygame.draw.circle(window, gold_outline, (600, 800), 60, 60)
	pygame.draw.circle(window, gold_color, (600, 800), 50, 50)
	pygame.draw.circle(window, gold_outline, (750, 800), 60, 60)
	pygame.draw.circle(window, gold_color, (750, 800), 50, 50)
	pygame.draw.circle(window, gold_outline, (900, 800), 60, 60)
	pygame.draw.circle(window, gold_color, (900, 800), 50, 50)

	pygame.draw.circle(window, gold_outline, (300 + move, 650), 60, 60)
	pygame.draw.circle(window, gold_color, (300 + move, 650), 50, 50)
	pygame.draw.circle(window, gold_outline, (450 + move, 650), 60, 60)
	pygame.draw.circle(window, gold_color, (450 + move, 650), 50, 50)
	pygame.draw.circle(window, gold_outline, (600 + move, 650), 60, 60)
	pygame.draw.circle(window, gold_color, (600 + move, 650), 50, 50)
	pygame.draw.circle(window, gold_outline, (750 + move, 650), 60, 60)
	pygame.draw.circle(window, gold_color, (750 + move, 650), 50, 50)

	pygame.draw.circle(window, gold_outline, (450, 500), 60, 60)
	pygame.draw.circle(window, gold_color, (450, 500), 50, 50)
	pygame.draw.circle(window, gold_outline, (600, 500), 60, 60)
	pygame.draw.circle(window, gold_color, (600, 500), 50, 50)
	pygame.draw.circle(window, gold_outline, (750, 500), 60, 60)
	pygame.draw.circle(window, gold_color, (750, 500), 50, 50)

	pygame.draw.circle(window, gold_outline, (450 + move, 350), 60, 60)
	pygame.draw.circle(window, gold_color, (450 + move, 350), 50, 50)
	pygame.draw.circle(window, gold_outline, (600 + move, 350), 60, 60)
	pygame.draw.circle(window, gold_color, (600 + move, 350), 50, 50)

	pygame.draw.circle(window, gold_outline, (600, 200), 60, 60)
	pygame.draw.circle(window, winnerColor2, (600, 200), 50, 50)

	renderText(200, "You Win!", gold_color, (300, 20))


def loadSettingsPage():
	pygame.draw.rect(window, tan_color, [200, 50, 800, 200])
	renderText(150, "Settings", black_color, (340, 100))

	renderText(60, "Prefered color", black_color, (470, 650))

	pygame.draw.circle(window, red_outline, (530, 770), 60, 60)
	pygame.draw.circle(window, red_color, (530, 770), 50, 50)
	pygame.draw.circle(window, black_outline, (670, 770), 60, 60)
	pygame.draw.circle(window, black_color, (670, 770), 50, 50)


create_window()

isRunning = True
mx, my = pygame.mouse.get_pos()
while isRunning:
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			isRunning = False
			pygame.quit()
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			col = (pos[0] - 50)// 80
			row = (pos[1] - 50) // 80
			# Debug prints
			print("Click ", pos, "Grid coordinates: ", row, col)
			# grid[row][col] = 1

	pos = pygame.mouse.get_pos()
	x = pos[0]
	y = pos[1]

	# Render Graphics
	window.blit(Wood, (0, 0))
# draw checkers board
	red = 1
	black = 0
	crown = pygame.image.load("king.png").convert_alpha()

	# loadPlayerChoicePage()
	loadGamePage()
	piece = Pieces()
	piece.player_color()

	# loadLoginPage()
	# loadOnePlayerPage()
	# loadWinPage(red)
	# loadTwoPlayerPage()
	# loadSettingsPage()
	# pieces =[[250, 330]]
	# highlight_checkers(pieces)
	# availableMoves = [[130, 210]]
	# highlight_available_moves(availableMoves)
	# mouse_pressed()
	# highlight_available_moves(blackChecks)



	pygame.display.flip()



	# clock.tick(60)
