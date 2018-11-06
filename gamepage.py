import pygame, sys, time
from tiles import *
from classes import *
from client import *

pygame.init()
pygame.font.init()

window = pygame.display.set_mode((1200,900))

clock = pygame.time.Clock()
currSec = 0
currFrame = 0
FPS = 0
tile_size = 80
w = 80
myClient = None

light_green = (83, 249, 88)
black_color = (0, 0, 0)
black_outline = (50, 47, 47)
red_color = (255, 0, 0)
red_outline = (181, 13, 13)
gold_color = (233, 218, 10)
gold_outline = (216, 171, 23)
tan_color = (242, 221, 179)
tan_highlight = (242, 235, 222)

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
	# draw grey tiles
	draw_grid()

	lower = 130
	upper = 210

	for i in range(8):
		for x in range(lower, upper, tile_size):
			for y in range(lower, upper , tile_size):
				window.blit(Tiles.greyTile, (x, y))
				pygame.draw.rect(window, black_color, (x, y, tile_size, tile_size), 1)
			lower += 80
			upper += 80

	lower1, upper1, lower2, upper2, = 290, 370, 130, 210
	load_grey_tiles(lower1, upper1, lower2, upper2, 6)

	lower1, upper1, lower2, upper2, =  450, 530, 130, 210
	load_grey_tiles(lower1, upper1, lower2, upper2, 4)

	lower1, upper1, lower2, upper2, = 610, 692, 130, 210
	load_grey_tiles(lower1, upper1, lower2, upper2, 1)

	lower1, upper1, lower2, upper2, = 130, 210, 290, 370
	load_grey_tiles(lower1, upper1, lower2, upper2, 6)

	lower1, upper1, lower2, upper2, = 130, 210, 450, 530
	load_grey_tiles(lower1, upper1, lower2, upper2, 4)

	lower1, upper1, lower2, upper2, = 130, 210, 610, 690
	load_grey_tiles(lower1, upper1, lower2, upper2, 2)

	#draw white tiles
	lower1, upper1, lower2, upper2, = 210, 290, 130, 210
	load_white_tiles(lower1, upper1, lower2, upper2, 7)

	lower1, upper1, lower2, upper2, =  370, 450, 130, 210
	load_white_tiles(lower1, upper1, lower2, upper2, 5)

	lower1, upper1, lower2, upper2, = 530, 610, 130, 210
	load_white_tiles(lower1, upper1, lower2, upper2, 3)

	lower1, upper1, lower2, upper2, = 690, 770, 130, 210
	load_white_tiles(lower1, upper1, lower2, upper2, 1)

	lower1, upper1, lower2, upper2, = 130, 210, 210, 290
	load_white_tiles(lower1, upper1, lower2, upper2, 7)

	lower1, upper1, lower2, upper2, = 130, 210, 370, 450
	load_white_tiles(lower1, upper1, lower2, upper2, 5)

	lower1, upper1, lower2, upper2, = 130, 210, 530, 610
	load_white_tiles(lower1, upper1, lower2, upper2, 3)

	lower1, upper1, lower2, upper2, = 130, 210, 690, 770
	load_white_tiles(lower1, upper1, lower2, upper2, 1)

# game border
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

	def draw_pieces(self, board, possible_moves, selected):
		# TODO: this always shows black on the bottom of the screen.
		for item in board:
			is_possible = (item[0], item[1]) in possible_moves
			is_selected = True if selected == item else False
			color = 'red' if board[item] == 'r' or board[item] == 'R' else 'black'
			is_king = True if board[item] == 'R' or board[item] == 'B' else False
			if board[item] != '.' and board[item] != '_':
				availableMoves = possible_moves[item] if is_selected else []
				self.draw_piece(color, item[0], item[1], is_possible, is_king, is_selected, availableMoves)

	def draw_piece(self, piece_color, row, col, is_possible, is_king, is_selected, availableMoves):
		outline = red_outline if piece_color == 'red' else black_outline
		color = red_color if piece_color == 'red' else black_color
		yPos = row * 80 + 170
		xPos = col * 80 + 170
		pygame.draw.circle(window, outline, (xPos, yPos), 37, 37)
		pygame.draw.circle(window, color, (xPos, yPos), 30, 30)

		if is_possible:
			pygame.draw.circle(window, light_green, (xPos, yPos), 38, 2)
		if is_selected:
			pygame.draw.circle(window, gold_outline, (xPos, yPos), 38, 2)
			for move in availableMoves:
				nextX = move['endRow'] * 80 + 170
				nextY = move['endColumn'] * 80 + 170
				pygame.draw.circle(window, gold_outline, (nextY, nextX), 38, 2)
		if is_king:
			crown = pygame.image.load("king.png").convert_alpha()
			window.blit(crown, (xPos - 27, yPos - 17))

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

def button(msg, x, y, w, h, ic, ac, action = None):
	global myClient
	cur = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x + w > cur[0] > x and y + h > cur[1] > y:
		pygame.draw.rect(window, ac, (x, y, w, h))
		if click[0] == 1 and action != None:
			if action == "quit":
				pygame.quit()
				sys.exit()

			if action == "soundOn":
				pass

			if action == "soundOff":
				pass

			if action == "challenge" and myClient:
				myClient.sendChallenge(msg)

			if action == 'listOnline':
				if not myClient:
					myClient = startClient()
					myClient.pump()

			if action == "player1":
				loadOnePlayerPage()

			if action == "player2":
				loadTwoPlayerPage()

			if action == "settings":
				loadSettingsPage()

			if action == "PlayOnline":
				print("clicked play online")

			if action == "LocalGame":
				gameLoop(False)

			if action == "p1":
				print("In action p1")

			if action == "p2":
				print("In action p2")

			# game loop for one player
			if action == "main1":
				gameLoop(True)

			if action == "acceptChallenge":
				myClient.respondToChallenge(True)

			if action == "rejectChallenge":
				myClient.respondToChallenge(False)

			#game loop for two player
			if action == "main2":
				# add parameters to gameLoop for AI
				gameLoop(False)

			if action == "home":
				game_intro()
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
	button("settings", 1090, 20, 100, 40, tan_color, tan_highlight, 'settings')
	renderText(30, "Settings", black_color, (1100, 30))
	button("quit", 1090, 850, 100, 40, tan_color, tan_highlight, 'quit')
	renderText(30, "Quit", black_color, (1115, 860))
	# player_color(black)
	load_chatbox(online)

def loadPlayerChoicePage():
	loadLogo()
	button("player1", 250, 600, 300, 60, tan_color, tan_highlight, 'player1')
	renderText(60, "1-Player", black_color, (320, 610))
	button("player2", 650, 600, 300, 60, tan_color, tan_highlight, 'player2')
	renderText(60, "2-Player", black_color, (720, 610))
	button("quit", 1090, 850, 100, 40, tan_color, tan_highlight, 'quit')
	renderText(30, "Quit", black_color, (1115, 860))
	button("settings", 1090, 20, 100, 40, tan_color, tan_highlight, 'settings')
	renderText(30, "Settings", black_color, (1100, 30))

def loadLoginPage():
	loadLogo()
	button("settings", 1090, 20, 100, 40, tan_color, tan_highlight, 'settings')
	renderText(30, "Settings", black_color, (1100, 30))
	button("quit", 1090, 850, 100, 40, tan_color, tan_highlight, 'quit')
	renderText(30, "Quit", black_color, (1115, 860))
	pygame.draw.rect(window, tan_color, [450, 600, 300, 40])
	renderText(30, "Username", black_color, (450, 580))
	pygame.draw.rect(window, tan_color, [450, 680, 300, 40])
	renderText(30, "Password", black_color, (450, 660))

def loadOnePlayerPage():
	gcont = True

	while gcont:
		for event in pygame.event.get():
				#print(event)
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
		window.blit(Wood, (0, 0))
		pygame.draw.rect(window, tan_color, [200, 50, 800, 200])
		renderText(150, "New Game", black_color, (340, 100))
		button("easy", 450, 300, 300, 60, tan_color, tan_highlight, 'main1')
		renderText(60, "Easy", black_color, (545, 310))
		button("medium", 450, 410, 300, 60, tan_color, tan_highlight, 'main1')
		renderText(60, "Medium", black_color, (520, 420))
		button("hard", 450, 520, 300, 60, tan_color, tan_highlight, 'main1')
		renderText(60, "Hard", black_color, (545, 530))

		renderText(60, "Select color", black_color, (480, 650))

		pygame.draw.circle(window, red_outline, (530, 770), 60, 60)
		pygame.draw.circle(window, red_color, (530, 770), 50, 50)
		pygame.draw.circle(window, black_outline, (670, 770), 60, 60)
		pygame.draw.circle(window, black_color, (670, 770), 50, 50)

		button("settings", 1090, 20, 100, 40, tan_color, tan_highlight, 'settings')
		renderText(30, "Settings", black_color, (1100, 30))
		button("quit", 1090, 850, 100, 40, tan_color, tan_highlight, 'quit')
		renderText(30, "Quit", black_color, (1115, 860))
		pygame.display.update()
		clock.tick(15)

def loadTwoPlayerPage():
	gcont = True

	while gcont:
		for event in pygame.event.get():
				#print(event)
				if event.type == pygame.QUIT:
					# if myClient:
					# 	myClient.closeConnection()
					pygame.quit()
					quit()
				if myClient:
					myClient.pump()

		window.blit(Wood, (0, 0))
		pygame.draw.rect(window, tan_color, [200, 50, 800, 200])
		renderText(150, "New Game", black_color, (340, 100))
		button("LocalGame", 200, 300, 300, 60, tan_color, tan_highlight, 'main2')
		renderText(60, "Local Game", black_color, (230, 310))
		button("PlayOnline", 700, 300, 300, 60, tan_color, tan_highlight, 'PlayOnline')
		renderText(60, "Play Online", black_color, (740, 310))
		button("quit", 1090, 850, 100, 40, tan_color, tan_highlight, 'quit')
		renderText(30, "Quit", black_color, (1115, 860))
		button("settings", 1090, 20, 100, 40, tan_color, tan_highlight, 'settings')
		renderText(30, "Settings", black_color, (1100, 30))

		pygame.draw.rect(window, tan_color, [700, 400, 300, 250])
		if myClient and hasattr(myClient, "otherPlayers"):
			xNum = 700
			yNum = 400
			for player in myClient.otherPlayers:
				# I need to be able to make a button for each player too.
				button(player, xNum, yNum, 300, 60, tan_color, tan_highlight, "challenge")
				renderText(60, player, black_color, (xNum, yNum))
				yNum += 50
		else:
			button("Find online players.", 700, 400, 300, 60, tan_color, tan_highlight, "listOnline")
			renderText(60, "Find online players.", black_color, (700, 400))

		if myClient and myClient.hasCurrentGame:
			loadGamePage()
			gameLoop(False)

		if myClient and myClient.rejectedChallenge:
			button(
			"Your challenge to " + str(myClient.rejectedChallenge) + " was rejected.",
			xNum, yNum + 150, 300, 60, tan_color, tan_highlight, 'main2')
			renderText(60, "challenge rejected", black_color, (xNum, 660))
			myClient.acknowledge_rejected_challenge()

		if myClient and myClient.pendingChallenge:
			if myClient.pendingChallenge.challengeTo == myClient.id:
				button("player1", 420, 800, 150, 40, tan_color, tan_highlight, 'acceptChallenge')
				renderText(40, "Accept", black_color, (450, 805))
				button("player2", 630, 800, 150, 40, tan_color, tan_highlight, 'rejectChallenge')
				renderText(40, "Decline", black_color, (655, 805))
			else:
				button("Sent challenge to " + str(myClient.pendingChallenge.challengeTo), xNum, yNum + 100, 300, 60, tan_color, tan_highlight, 'main2')
				renderText(30, "Waiting for player to respond...", black_color, (xNum, 660))
		pygame.display.update()
		clock.tick(15)

def loadWinPage(color):
	gcont = True

	while gcont:
		for event in pygame.event.get():
				#print(event)
				if event.type == pygame.QUIT:
					# if myClient:
					# 	myClient.closeConnection()
					pygame.quit()
					quit()
		move = 80
		if color == 1:
			winnerColor1 = red_outline
			winnerColor2 = red_color
		else:
			winnerColor1 = black_outline
			winnerColor2 = black_color
		button("home", 950, 700, 300, 300, tan_color, tan_highlight, 'home')
		window.blit(Wood, (0, 0))
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

		pygame.display.update()
		clock.tick(15)

def loadSettingsPage():
	gcont = True

	while gcont:
		for event in pygame.event.get():
				# if myClient:
				# 	myClient.closeConnection()
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
		window.blit(Wood, (0, 0))
		pygame.draw.rect(window, tan_color, [200, 50, 800, 200])
		renderText(150, "Settings", black_color, (340, 100))
		renderText(50, "Prefered color", black_color, (470, 650))

		button("quit", 1090, 850, 100, 40, tan_color, tan_highlight, 'quit')
		renderText(30, "Quit", black_color, (1115, 860))

		pygame.draw.circle(window, red_outline, (530, 770), 60, 60)
		pygame.draw.circle(window, red_color, (530, 770), 50, 50)
		pygame.draw.circle(window, black_outline, (670, 770), 60, 60)
		pygame.draw.circle(window, black_color, (670, 770), 50, 50)

		button("soundOn", 200, 300, 100, 60, tan_color, tan_highlight, 'soundOn')
		renderText(25, "Sound On", black_color, (205, 310))
		button("soundOff", 350, 300, 100, 60, tan_color, tan_highlight, 'soundOff')
		renderText(25, "Sound Off", black_color, (355, 310))
		button("listOnline", 700, 300, 300, 60, tan_color, tan_highlight, 'listOnline')
		renderText(40, "List me online", black_color, (740, 310))

		button("2 player page", 700, 375, 300, 60, tan_color, tan_highlight, 'player2')
		renderText(40, "2 player page", black_color, (740, 410))

		# button("medium", 450, 410, 300, 60, (0, 0, 0), 'main1')
		pygame.draw.rect(window, (tan_color), (450, 475, 300, 60))
		renderText(50, "Update Username", black_color, (460, 440))

		pygame.draw.rect(window, (tan_color), (450, 585, 300, 60))
		renderText(50, "Update Password", black_color, (460, 550))

		pygame.display.update()
		clock.tick(15)

def game_intro():

	intro = True

	# Render Graphics
	while intro:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_c:
						intro = False
					elif event.key == pygame.K_q:

						pygame.quit()
						quit()
		window.blit(Wood, (0, 0))


		loadLogo()
		loadPlayerChoicePage()


		pygame.display.update()

		clock.tick(15)

def check_win(game):
	if game.is_game_over():
		if game.is_draw():
			print("The game is a draw.")
		else:
			winningPlayer = 'red' if game.is_win() == 0 else 'black'
			if (winningPlayer == 'red'):
				window.blit(Wood, (0, 0))
				loadWinPage(1)
			else:
				window.blit(Wood, (0, 0))
				loadWinPage(0)
		return True
	return False

def gameLoop(use_AI):
	gameExit = False
	gameOver = False
	FPS = 15

	while not gameExit:
		global myClient
		isRunning = True
		# mx, my = pygame.mouse.get_pos()
		initialClick = None
		piece = Pieces()
		game = GameState()
		game.get_all_legal_moves()
		loadGamePage()
		pygame.display.flip()
		while isRunning:
			# this is the AI's turn.
			if use_AI and game.activePlayer == 1:
				initialClick = None
				game.update_game_state_with_move(game.get_ai_move())
				game.switch_player()
				game.get_all_legal_moves()
				if check_win(game):
					isRunning = False
					break
			# networked version
			elif myClient and myClient.hasCurrentGame:
				# If it's the current player's turn
				myClient.pump()
				if myClient.possibleMoves:
					possible_moves = myClient.possibleMoves
					events = pygame.event.get()
					for event in events:
						if event.type == pygame.QUIT:
							# TODO: delete game then.
							isRunning = False
							pygame.quit()
							sys.exit()
						elif event.type == pygame.MOUSEBUTTONDOWN:
							col = ((pos[0] - 50) // 80) - 1
							row = ((pos[1] - 50) // 80) - 1
							print(row, col)

							if initialClick and initialClick in possible_moves:
								made_move = False
								print(possible_moves)
								for possibleMove in possible_moves[initialClick]:

									print("possibleMoveValue: {}. type: {}".format(possibleMove, type(possibleMove)))
									# print("possible row: {}, col: {}".format(possibleMove['e', possibleMove[1]))
									# print("received row: {}, col: {}".format(row, col))

									if row == possibleMove['endRow'] and col == possibleMove['endColumn']:
										print(
											"trying to move from " + str(initialClick) + " to (" + str(row) + ", " + str(col) + ")")
										myClient.sendResponse({
											"startRow": initialClick[0],
											"startColumn": initialClick[1],
											"endRow": row,
											"endCol": col})
										initialClick = None
									# else:
									# 	print("move doesn't work")
									# 	# initialClick = None
								if not made_move:
									print("cannot move from {} to ({}, {})".format(str(initialClick), row, col))
									initialClick = None
							# Debug prints
							if (row, col) in possible_moves:
								initialClick = (row, col)

						pos = pygame.mouse.get_pos()

				for event in pygame.event.get():

					if event.type == pygame.QUIT:
						gameExit = True
				# Render Graphics
				window.blit(Wood, (0, 0))

				loadGamePage()
				# Update board
				possible_moves = myClient.possibleMoves if myClient.possibleMoves else {}
				piece.draw_pieces(myClient.board, possible_moves, initialClick)

				pygame.display.flip()
				clock.tick(FPS)
			# get the move from the board.
			else:
				possible_moves = game.send_possible_moves_for_network()
				events = pygame.event.get()
				for event in events:
					if event.type == pygame.QUIT:
						isRunning = False
						pygame.quit()
						sys.exit()
					elif event.type == pygame.MOUSEBUTTONDOWN:
						col = ((pos[0] - 50)// 80) - 1
						row = ((pos[1] - 50) // 80) - 1
						print(row, col)

						if initialClick:
							made_move = False
							for possibleMove in game.board[initialClick[0]][initialClick[1]].possibleMoves:
								if row == possibleMove.endRow and col == possibleMove.endColumn:
									print("moved from " + str(initialClick) + " to (" + str(row) + ", " + str(col) + ")")
									made_move = True
									game.update_game_state_with_move(possibleMove)
									game.switch_player()
									game.get_all_legal_moves()

									if check_win(game):
										isRunning = False
										break
							if not made_move:
								print("cannot move from " + str(initialClick) + " to (" + str(row) + ", "+ str(col) + ")")
								initialClick = None

						if (row, col) in possible_moves:
							initialClick = (row, col)

					pos = pygame.mouse.get_pos()

					for event in pygame.event.get():

						if event.type == pygame.QUIT:
							gameExit = True

				loadGamePage()
				# # Update board
				piece.draw_pieces(game.get_board_for_network(), game.send_possible_moves_for_network(), initialClick)

				pygame.display.flip()
				clock.tick(FPS)
	pygame.quit()
	quit()

if __name__ == '__main__':

	game_intro()

	gameLoop()
