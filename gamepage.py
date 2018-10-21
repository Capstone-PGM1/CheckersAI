import pygame, sys, time, pygame_textinput
from tiles import *



pygame.init()
pygame.font.init()

currSec = 0
currFrame = 0
FPS = 0
tile_size = 80

# create the background
wood = pygame.image.load("wood.jpg")
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

def load_white_tiles(lower1, upper1, lower2, upper2, n):
	for i in range(n):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.whiteTile, (x, y))
				pygame.draw.rect(window, (0, 0, 0), (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

def load_grey_tiles(lower1, upper1, lower2, upper2, n):
	for i in range(n):
		for x in range(lower1, upper1, tile_size):
			for y in range(lower2, upper2 , tile_size):
				window.blit(Tiles.greyTile, (x, y))
				pygame.draw.rect(window, (0, 0, 0), (x, y, tile_size, tile_size), 1)
			lower1 += 80
			upper1 += 80
			lower2 += 80
			upper2 += 80

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
	load_white_tiles(lower1, upper1, lower2, upper2, 6)

	lower1 = 450
	upper1 = 530
	lower2 = 130
	upper2 = 210
	load_white_tiles(lower1, upper1, lower2, upper2, 4)


	lower1 = 610
	upper1 = 692
	lower2 = 130
	upper2 = 210
	load_white_tiles(lower1, upper1, lower2, upper2, 1)	


	lower1 = 130
	upper1 = 210
	lower2 = 290
	upper2 = 370
	load_white_tiles(lower1, upper1, lower2, upper2, 6)


	lower1 = 130
	upper1 = 210
	lower2 = 450
	upper2 = 530
	load_white_tiles(lower1, upper1, lower2, upper2, 4)


	lower1 = 130
	upper1 = 210
	lower2 = 610
	upper2 = 690
	load_white_tiles(lower1, upper1, lower2, upper2, 2)


#draw grey tiles

	lower1 = 210
	upper1 = 290
	lower2 = 130
	upper2 = 210
	load_grey_tiles(lower1, upper1, lower2, upper2, 7)

	lower1 = 370
	upper1 = 450
	lower2 = 130
	upper2 = 210
	load_grey_tiles(lower1, upper1, lower2, upper2, 5)

	lower1 = 530
	upper1 = 610
	lower2 = 130
	upper2 = 210
	load_grey_tiles(lower1, upper1, lower2, upper2, 3)

	lower1 = 690
	upper1 = 770
	lower2 = 130
	upper2 = 210
	load_grey_tiles(lower1, upper1, lower2, upper2, 1)

	lower1 = 130
	upper1 = 210
	lower2 = 210
	upper2 = 290
	load_grey_tiles(lower1, upper1, lower2, upper2, 7)

	lower1 = 130
	upper1 = 210
	lower2 = 370
	upper2 = 450
	load_grey_tiles(lower1, upper1, lower2, upper2, 5)

	lower1 = 130
	upper1 = 210
	lower2 = 530
	upper2 = 610
	load_grey_tiles(lower1, upper1, lower2, upper2, 3)

	lower1 = 130
	upper1 = 210
	lower2 = 690
	upper2 = 770
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

def renderText(fontSize, message, color, position):
	myfont = pygame.font.SysFont('Comic Sans MS', fontSize)
	textsurface = myfont.render(message, False, color)
	window.blit(textsurface, position)


def loadLogo():
	pygame.draw.circle(window, (50, 47, 47), (900, 300), 180, 180)
	pygame.draw.circle(window, (0, 0, 0), (900, 300), 160, 160)
	pygame.draw.circle(window, (181, 13, 13), (700, 300), 180, 180)
	pygame.draw.circle(window, (255, 0, 0), (700, 300), 160, 160)
	pygame.draw.circle(window, (50, 47, 47), (500, 300), 180, 180)
	pygame.draw.circle(window, (0, 0, 0), (500, 300), 160, 160)
	pygame.draw.circle(window, (181, 13, 13), (300, 300), 180, 180)
	pygame.draw.circle(window, (255, 0, 0), (300, 300), 160, 160)
	renderText(200, "Checkers", (233, 218, 10), (300, 230))

def loadGamePage():
# draw checkers board
	black = 1
	red = 0
	online = 1
	offline = 0
	load_board()
	button("settings", 1090, 20, 100, 40, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(30, "Settings", (0, 0, 0), (1100, 30))
	button("quit", 1090, 850, 100, 40, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(30, "Quit", (0, 0, 0), (1115, 860))
	player_color(black)
	load_chatbox(online)


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


	king_piece(gamePiece, pos3)

def loadPlayerChoicePage():
	loadLogo()
	button("player1", 250, 600, 300, 60, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(60, "1-Player", (0, 0, 0), (320, 610))
	button("player2", 650, 600, 300, 60, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(60, "2-Player", (0, 0, 0), (720, 610))
	button("quit", 1090, 850, 100, 40, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(30, "Quit", (0, 0, 0), (1115, 860))
	button("settings", 1090, 20, 100, 40, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(30, "Settings", (0, 0, 0), (1100, 30))

def loadLoginPage():
	loadLogo()
	button("settings", 1090, 20, 100, 40, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(30, "Settings", (0, 0, 0), (1100, 30))
	button("quit", 1090, 850, 100, 40, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(30, "Quit", (0, 0, 0), (1115, 860))
	pygame.draw.rect(window, (242, 221, 179), [450, 600, 300, 40])
	renderText(30, "Username", (0, 0, 0), (450, 580))
	pygame.draw.rect(window, (242, 221, 179), [450, 680, 300, 40])
	renderText(30, "Password", (0, 0, 0), (450, 660))

def loadOnePlayerPage():
	pygame.draw.rect(window, (242, 221, 179), [200, 50, 800, 200])
	renderText(150, "New Game", (0, 0, 0), (340, 100))
	button("easy", 450, 300, 300, 60, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(60, "Easy", (0, 0, 0), (545, 310))
	button("medium", 450, 410, 300, 60, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(60, "Medium", (0, 0, 0), (520, 420))
	button("hard", 450, 520, 300, 60, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(60, "Hard", (0, 0, 0), (545, 530))

	renderText(60, "Select color", (0, 0, 0), (480, 650))

	pygame.draw.circle(window, (181, 13, 13), (530, 770), 60, 60)
	pygame.draw.circle(window, (255, 0, 0), (530, 770), 50, 50)
	pygame.draw.circle(window, (50, 47, 47), (670, 770), 60, 60)
	pygame.draw.circle(window, (0, 0, 0), (670, 770), 50, 50)

	button("settings", 1090, 20, 100, 40, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(30, "Settings", (0, 0, 0), (1100, 30))
	button("quit", 1090, 850, 100, 40, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(30, "Quit", (0, 0, 0), (1115, 860))

def loadTwoPlayerPage():
	pygame.draw.rect(window, (242, 221, 179), [200, 50, 800, 200])
	renderText(150, "New Game", (0, 0, 0), (340, 100))
	button("LocalGame", 200, 300, 300, 60, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(60, "Local Game", (0, 0, 0), (230, 310))
	button("PlayOnline", 700, 300, 300, 60, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(60, "Play Online", (0, 0, 0), (740, 310))
	button("quit", 1090, 850, 100, 40, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(30, "Quit", (0, 0, 0), (1115, 860))
	button("settings", 1090, 20, 100, 40, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(30, "Settings", (0, 0, 0), (1100, 30))

	pygame.draw.rect(window, (242, 221, 179), [700, 400, 300, 250])

	button("player1", 420, 800, 150, 40, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(40, "Accept", (0, 0, 0), (450, 805))
	button("player2", 630, 800, 150, 40, (242, 221, 179), (242, 235, 222), 'quit')
	renderText(40, "Decline", (0, 0, 0), (655, 805))

def loadWinPage(color):
	move = 80
	if color == 1:
		winnerColor1 = (181, 13, 13)
		winnerColor2 = (255, 0, 0)
	else:
		winnerColor1 = (50, 47, 47)
		winnerColor2 = (0, 0, 0)		

	pygame.draw.circle(window, winnerColor1, (100, 100), 90, 90)
	pygame.draw.circle(window, winnerColor2, (100, 100), 80, 80)
	pygame.draw.circle(window, winnerColor1, (1100, 100), 90, 90)
	pygame.draw.circle(window, winnerColor2, (1100, 100), 80, 80)
	pygame.draw.circle(window, winnerColor1, (100, 800), 90, 90)
	pygame.draw.circle(window, winnerColor2, (100, 800), 80, 80)
	pygame.draw.circle(window, winnerColor1, (1100, 800), 90, 90)
	pygame.draw.circle(window, winnerColor2, (1100, 800), 80, 80)
	renderText(50, "Play", (233, 218, 10), (1060, 760))
	renderText(50, "Again", (233, 218, 10), (1050, 800))

	pygame.draw.circle(window, (216, 171, 23), (300, 800), 60, 60)
	pygame.draw.circle(window, (233, 218, 10), (300, 800), 50, 50)	
	pygame.draw.circle(window, (216, 171, 23), (450, 800), 60, 60)
	pygame.draw.circle(window, (233, 218, 10), (450, 800), 50, 50)	
	pygame.draw.circle(window, (216, 171, 23), (600, 800), 60, 60)
	pygame.draw.circle(window, (233, 218, 10), (600, 800), 50, 50)	
	pygame.draw.circle(window, (216, 171, 23), (750, 800), 60, 60)
	pygame.draw.circle(window, (233, 218, 10), (750, 800), 50, 50)
	pygame.draw.circle(window, (216, 171, 23), (900, 800), 60, 60)
	pygame.draw.circle(window, (233, 218, 10), (900, 800), 50, 50)		

	pygame.draw.circle(window, (216, 171, 23), (300 + move, 650), 60, 60)
	pygame.draw.circle(window, (233, 218, 10), (300 + move, 650), 50, 50)	
	pygame.draw.circle(window, (216, 171, 23), (450 + move, 650), 60, 60)
	pygame.draw.circle(window, (233, 218, 10), (450 + move, 650), 50, 50)	
	pygame.draw.circle(window, (216, 171, 23), (600 + move, 650), 60, 60)
	pygame.draw.circle(window, (233, 218, 10), (600 + move, 650), 50, 50)	
	pygame.draw.circle(window, (216, 171, 23), (750 + move, 650), 60, 60)
	pygame.draw.circle(window, (233, 218, 10), (750 + move, 650), 50, 50)

	pygame.draw.circle(window, (216, 171, 23), (450, 500), 60, 60)
	pygame.draw.circle(window, (233, 218, 10), (450, 500), 50, 50)	
	pygame.draw.circle(window, (216, 171, 23), (600, 500), 60, 60)
	pygame.draw.circle(window, (233, 218, 10), (600, 500), 50, 50)	
	pygame.draw.circle(window, (216, 171, 23), (750, 500), 60, 60)
	pygame.draw.circle(window, (233, 218, 10), (750, 500), 50, 50)

	pygame.draw.circle(window, (216, 171, 23), (450 + move, 350), 60, 60)
	pygame.draw.circle(window, (233, 218, 10), (450 + move, 350), 50, 50)	
	pygame.draw.circle(window, (216, 171, 23), (600 + move, 350), 60, 60)
	pygame.draw.circle(window, (233, 218, 10), (600 + move, 350), 50, 50)	

	pygame.draw.circle(window, (216, 171, 23), (600, 200), 60, 60)
	pygame.draw.circle(window, winnerColor2, (600, 200), 50, 50)	

	renderText(200, "You Win!", (233, 218, 10), (300, 20))

	
create_window()

isRunning = True

while isRunning:
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			isRunning = False
			pygame.quit()
			sys.exit()

	# Render Graphics
	window.blit(Wood, (0, 0))
# draw checkers board
	red = 1
	black = 0
	crown = pygame.image.load("king.png").convert_alpha()

	# loadPlayerChoicePage()
	loadGamePage()
	# loadLoginPage()
	# loadOnePlayerPage()
	# loadWinPage(black)
	# loadTwoPlayerPage()
	# loadSettingsPage()




	pygame.display.flip()				
