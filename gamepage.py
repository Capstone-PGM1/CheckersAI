import pygame, sys, time
from tiles import *

pygame.init()

currSec = 0
currFrame = 0
FPS = 0
tile_size = 80

# create the background
wood = pygame.image.load("wood.jpg")
# wood = pygame.image.load("wood.jpg").convert()
wood = pygame.transform.scale(wood, (1200, 900))
Wood = pygame.Surface(wood.get_size(), pygame.HWSURFACE)
Wood.blit(wood, (0, 0))
del wood


# create game window - will make maximize button later
def create_window():
	global window, window_height, window_width, window_title
	window_width, window_height = 1200, 900
	window_title = "Checkers"
	pygame.display.set_caption(window_title)
	# hardeware/doublebug mode to make things smoother
	window = pygame.display.set_mode((window_width, window_height), pygame.HWSURFACE|pygame.DOUBLEBUF)


def load_board():
	# draw white tiles

	lower = 130
	upper = 210
	for i in range(8):
		for x in range(lower, upper, tile_size):
			for y in range(lower, upper , tile_size):
				window.blit(Tiles.whiteTile, (x, y))
				pygame.draw.rect(window, (0, 0, 0), (x, y, tile_size, tile_size), 1)
			lower += 80
			upper += 80

	lower1 = 290
	upper1 = 370
	lower2 = 130
	upper2 = 210
	for i in range(6):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.whiteTile, (x, y))
				pygame.draw.rect(window, (0, 0, 0), (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

	lower1 = 450
	upper1 = 530
	lower2 = 130
	upper2 = 210
	for i in range(4):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.whiteTile, (x, y))
				pygame.draw.rect(window, (0, 0, 0), (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

	lower1 = 610
	upper1 = 692
	lower2 = 130
	upper2 = 210
	for i in range(1):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.whiteTile, (x, y))
				pygame.draw.rect(window, (0, 0, 0), (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

	lower1 = 130
	upper1 = 210
	lower2 = 290
	upper2 = 370
	for i in range(6):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.whiteTile, (x, y))
				pygame.draw.rect(window, (0, 0, 0), (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

	lower1 = 130
	upper1 = 210
	lower2 = 450
	upper2 = 530
	for i in range(4):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.whiteTile, (x, y))
				pygame.draw.rect(window, (0, 0, 0), (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

	lower1 = 130
	upper1 = 210
	lower2 = 610
	upper2 = 690
	for i in range(2):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.whiteTile, (x, y))
				pygame.draw.rect(window, (0, 0, 0), (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

#draw grey tiles

	lower1 = 210
	upper1 = 290
	lower2 = 130
	upper2 = 210
	for i in range(7):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.greyTile, (x, y))
				pygame.draw.rect(window, (0, 0, 0), (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

	lower1 = 370
	upper1 = 450
	lower2 = 130
	upper2 = 210
	for i in range(5):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.greyTile, (x, y))
				pygame.draw.rect(window, (0, 0, 0), (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

	lower1 = 530
	upper1 = 610
	lower2 = 130
	upper2 = 210
	for i in range(3):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.greyTile, (x, y))
				pygame.draw.rect(window, (0, 0, 0), (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

	lower1 = 690
	upper1 = 770
	lower2 = 130
	upper2 = 210
	for i in range(1):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.greyTile, (x, y))
				pygame.draw.rect(window, (0, 0, 0), (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

	lower1 = 130
	upper1 = 210
	lower2 = 210
	upper2 = 290
	for i in range(7):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.greyTile, (x, y))
				pygame.draw.rect(window, (0, 0, 0), (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

	lower1 = 130
	upper1 = 210
	lower2 = 370
	upper2 = 450
	for i in range(5):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.greyTile, (x, y))
				pygame.draw.rect(window, (0, 0, 0), (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

	lower1 = 130
	upper1 = 210
	lower2 = 530
	upper2 = 610
	for i in range(3):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.greyTile, (x, y))
				pygame.draw.rect(window, (0, 0, 0), (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

	lower1 = 130
	upper1 = 210
	lower2 = 690
	upper2 = 770
	for i in range(1):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.greyTile, (x, y))
				pygame.draw.rect(window, (0, 0, 0), (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

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



def player_color(color):
	# if player color is black
	if (color == 1):
		# initial red checkers
		lower = 250
		upper = 170
		for i in range(4):
			pygame.draw.circle(window, (181, 13, 13), (lower, upper), 37, 37)
			pygame.draw.circle(window, (255, 0, 0), (lower, upper), 30, 30)
			lower += 160

		lower = 170
		upper = 250
		for i in range(4):
			pygame.draw.circle(window, (181, 13, 13), (lower, upper), 37, 37)
			pygame.draw.circle(window, (255, 0, 0), (lower, upper), 30, 30)
			lower += 160

		lower = 250
		upper = 330
		for i in range(4):
			pygame.draw.circle(window, (181, 13, 13), (lower, upper), 37, 37)
			pygame.draw.circle(window, (255, 0, 0), (lower, upper), 30, 30)
			lower += 160


		# initial black checkers
		lower = 170
		upper = 570
		for i in range(4):
			pygame.draw.circle(window, (50, 47, 47), (lower, upper), 37, 37)
			pygame.draw.circle(window, (0, 0, 0), (lower, upper), 30, 30)
			lower += 160

		lower = 250
		upper = 650
		for i in range(4):
			pygame.draw.circle(window, (50, 47, 47), (lower, upper), 37, 37)
			pygame.draw.circle(window, (0, 0, 0), (lower, upper), 30, 30)
			lower += 160

		lower = 170
		upper = 730
		for i in range(4):
			pygame.draw.circle(window, (50, 47, 47), (lower, upper), 37, 37)
			pygame.draw.circle(window, (0, 0, 0), (lower, upper), 30, 30)
			lower += 160
	# if player color is red
	else:


		# initial red checkers
		lower = 250
		upper = 170
		for i in range(4):
			pygame.draw.circle(window, (50, 47, 47), (lower, upper), 37, 37)
			pygame.draw.circle(window, (0, 0, 0), (lower, upper), 30, 30)
			lower += 160

		lower = 170
		upper = 250
		for i in range(4):
			pygame.draw.circle(window, (50, 47, 47), (lower, upper), 37, 37)
			pygame.draw.circle(window, (0, 0, 0), (lower, upper), 30, 30)
			lower += 160

		lower = 250
		upper = 330
		for i in range(4):
			pygame.draw.circle(window, (50, 47, 47), (lower, upper), 37, 37)
			pygame.draw.circle(window, (0, 0, 0), (lower, upper), 30, 30)
			lower += 160


		# initial black checkers
		lower = 170
		upper = 570
		for i in range(4):
			pygame.draw.circle(window, (181, 13, 13), (lower, upper), 37, 37)
			pygame.draw.circle(window, (255, 0, 0), (lower, upper), 30, 30)
			lower += 160

		lower = 250
		upper = 650
		for i in range(4):
			pygame.draw.circle(window, (181, 13, 13), (lower, upper), 37, 37)
			pygame.draw.circle(window, (255, 0, 0), (lower, upper), 30, 30)
			lower += 160

		lower = 170
		upper = 730
		for i in range(4):
			pygame.draw.circle(window, (181, 13, 13), (lower, upper), 37, 37)
			pygame.draw.circle(window, (255, 0, 0), (lower, upper), 30, 30)
			lower += 160

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




create_window()

isRunning = True

while isRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
			pygame.quit()
			sys.exit()

	# Render Graphics
	window.blit(Wood, (0, 0))
# draw checkers board
	black = 1
	red = 0
	online = 1
	offline = 0
	crown = pygame.image.load("king.png").convert_alpha()
	gamePiece = 1 
	pos1 = (170 , 730)
	gamePiece = 2 
	pos2 = (330 , 730)
	gamePiece = 3 
	pos3 = (490 , 730)
	gamePiece = 4 
	pos4 = (650 , 730)
	gamePiece = 13 
	pos13 = (250 , 170)
	gamePiece = 14 
	pos14 = (410 , 170)
	gamePiece = 15 
	pos15 = (570 , 170)
	gamePiece = 16 
	pos16 = (730 , 170)


	load_board()
	button("quit", 1090, 850, 100, 40, (242, 221, 179), (242, 235, 222), 'quit')
	player_color(red)
	load_chatbox(online)
	king_piece(gamePiece, pos1)


	pygame.display.flip()				
