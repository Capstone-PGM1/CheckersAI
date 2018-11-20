"""
For game window resizing uses code from:
https://github.com/Mekire/pygame-samples/blob/master/resizable/resizable_aspect_ratio.py
"""

from graphics_helpers import *
from client import *
from pygame_textinput import *
from classes import *

class Pieces(object):
	def draw_pieces(self, window, board, possible_moves, selected):
		# TODO: this always shows black on the bottom of the screen.
		for item in board:
			is_possible = (item[0], item[1]) in possible_moves
			is_selected = True if selected == item else False
			color = 'red' if board[item] == 'r' or board[item] == 'R' else 'black'
			is_king = True if board[item] == 'R' or board[item] == 'B' else False
			if board[item] != '.' and board[item] != '_':
				available_moves = possible_moves[item] if is_selected and item in possible_moves else []
				self.draw_piece(window, color, item[0], item[1], is_possible, is_king, is_selected, available_moves)

	def draw_piece(self, window, piece_color, row, col, is_possible, is_king, is_selected, available_moves):
		outline = red_outline if piece_color == 'red' else black_outline
		color = red_color if piece_color == 'red' else black_color
		# These numbers are hard coded, but the pieces render correctly for different sizes for me.
		y_pos = row * 40 + 85
		x_pos = col * 40 + 85
		pg.draw.circle(window, outline, (x_pos, y_pos), 18, 18)
		pg.draw.circle(window, color, (x_pos, y_pos), 15, 15)
		if is_possible:
			pygame.draw.circle(window, light_green, (x_pos, y_pos), 19, 1)
		if is_selected:
			pygame.draw.circle(window, gold_outline, (x_pos, y_pos), 19, 1)
			for move in available_moves:
				next_x = move['endRow'] * 40 + 85
				next_y = move['endColumn'] * 40 + 85
				pygame.draw.circle(window, gold_outline, (next_y, next_x), 19, 1)
		if is_king:
			crown = pygame.image.load("king.png").convert_alpha()
			window.blit(crown, (x_pos - 27, y_pos - 17))


class Page(object):
	def __init__(self):
		# create the background
		wood = pg.image.load("wood.jpg")
		self.background = pg.transform.scale(wood, SCREEN_START_SIZE)

	def settings_quit_btn(self, set_done, set_page):
		if not isinstance(self, WinPage):
			self.button("quit", 510, 425, 85, 20, tan_color, tan_highlight, lambda: set_done(True))
			pg.draw.rect(self.image, brown_color, (510, 425, 85, 20), 2)
		if not isinstance(self, Settings) and not isinstance(self, WinPage):
			self.button("settings", 510, 20, 85, 20, tan_color, tan_highlight, lambda: set_page(Settings()))
			pg.draw.rect(self.image, brown_color, (510, 20, 85, 20), 2)

	def update(self, window: pg.Surface, screen_rect, scale, update_page, update_done, update_client, client):
		self.screen_rect = screen_rect
		self.scale = scale
		self.image = window
		self.image.blit(self.background, (0, 0))

		self.load_background()
		self.load_buttons(update_page, update_client, client)
		self.settings_quit_btn(update_done, update_page)

	def load_background(self):
		pass

	def load_buttons(self, update_page=None, update_client=None, client=None):
		pass

	def handle_event(self, event, set_page, client):
		pass

	def get_text_input(self, events, client):
		pass

	# https://pythonprogramming.net/pygame-button-function/?completed=/placing-text-pygame-buttons/
	def button(self, msg, top_left_x_coordinate, top_left_y_coordinate, width, height, inactive_color, active_color,
			   onClick=None):
		# TODO: some of the button rectangles are smaller than the words.
		cur = pg.mouse.get_pos()
		click = pg.mouse.get_pressed()
		image_x = self.screen_rect.center[0] - (SCREEN_START_SIZE[0] * self.scale) / 2
		image_y = self.screen_rect.center[1] - (SCREEN_START_SIZE[1] * self.scale) / 2
		if (top_left_x_coordinate + width) * self.scale + image_x > cur[
			0] > top_left_x_coordinate * self.scale + image_x and \
							(top_left_y_coordinate + height) * self.scale + image_y > cur[
					1] > top_left_y_coordinate * self.scale + image_y:
			if onClick is not None and msg != "home":
				render_centered_text_with_background(28, msg, black_color, top_left_x_coordinate, top_left_y_coordinate,
													 width, height,
													 self.image, active_color)
			if click[0] == 1 and onClick is not None:
				onClick()
		else:
			if onClick is not None and msg != "home":
				render_centered_text_with_background(28, msg, black_color, top_left_x_coordinate, top_left_y_coordinate,
													 width, height,
													 self.image, inactive_color)


class Intro(Page):
	def load_background(self):
		draw_black_circle(450, 150, intro_circle_radius, intro_outline_radius, self.image)
		draw_red_circle(350, 150, intro_circle_radius, intro_outline_radius, self.image)
		draw_black_circle(250, 150, intro_circle_radius, intro_outline_radius, self.image)
		draw_red_circle(150, 150, intro_circle_radius, intro_outline_radius, self.image)
		render_centered_text(100, "Checkers", gold_color, 265, 110, intro_circle_radius, intro_outline_radius,
							 self.image)

	def load_buttons(self, update_page=None, update_client=None, client=None):
		self.button("One Player", 125, 300, 150, 34, tan_color, tan_highlight, lambda: update_page(OnePlayerOptions()))
		self.button("Two Player", 325, 300, 150, 34, tan_color, tan_highlight, lambda: update_page(TwoPlayerOptions()))



class Settings(Page):
	def load_background(self):
		# TODO: Update these numbers if necessary
		render_centered_text_with_background(70, "Settings", black_color, 100, 25, 400, 80, self.image, tan_color)
		self.image.blit(render_text(25, "Preferred color", black_color)[0], (245, 320))

	def load_buttons(self, update_page=None, update_client=None, client=None):
		draw_red_circle(265, 385, settings_circle_radius, settings_outline_radius, self.image)
		draw_black_circle(335, 385, settings_circle_radius, settings_outline_radius, self.image)
		self.button("Home", 10, 10, 60, 35, tan_color, tan_highlight, lambda: update_page(Intro()))		
		self.button("List Online", 350, 150, 150, 30, tan_color, tan_highlight, lambda: update_client())
		self.button("2 player page", 350, 185, 150, 30, tan_color, tan_highlight,
						lambda: update_page(TwoPlayerOptions()))
		if (client):
			self.button("Don't play online", 350, 150, 150, 30, tan_color, tan_highlight, lambda: update_client(None))
		else:
			self.button("List Online", 350, 150, 150, 30, tan_color, tan_highlight, lambda: update_client(startClient()))
		pg.draw.rect(self.image, tan_color, (100, 150, 150, 30))
		pg.draw.rect(self.image, brown_color, (100, 150, 150, 30), 2)
		self.image.blit(render_text(20, "Update Username", black_color)[0], (120, 160))
 
    
class red_selection(Page):
	def load_background(self):
		# TODO: update these numbers -- looks good on the Mac.
		render_centered_text_with_background(70, "New Game", black_color, 100, 25, 400, 80, self.image, tan_color)
		self.image.blit(render_text(25, "Select color", black_color)[0], (255, 320))
		select_red_circle(265, 385, settings_circle_radius, settings_outline_radius, self.image)

	def load_buttons(self, update_page=None, update_client=None, client=None):
		self.button("Red", 245, 365, 40, 40, tan_color, tan_highlight, lambda: update_page(red_selection()))
		self.button("Black", 315, 365, 40, 40, tan_color, tan_highlight, lambda: update_page(black_selection()))

		draw_red_circle(265, 385, settings_circle_radius, settings_outline_radius, self.image)
		draw_black_circle(335, 385, settings_circle_radius, settings_outline_radius, self.image)
		self.button("Easy", 225, 150, 150, 30, tan_color, tan_highlight, lambda: update_page(GamePage(True, 1)))
		self.button("Medium", 225, 205, 150, 30, tan_color, tan_highlight, lambda: update_page(GamePage(True, 3)))
		self.button("Hard", 225, 260, 150, 30, tan_color, tan_highlight, lambda: update_page(GamePage(True, 5)))
		self.button("Home", 10, 10, 60, 35, tan_color, tan_highlight, lambda: update_page(Intro()))	


class black_selection(Page):
	def load_background(self):
		# TODO: update these numbers -- looks good on the Mac.
		render_centered_text_with_background(70, "New Game", black_color, 100, 25, 400, 80, self.image, tan_color)
		self.image.blit(render_text(25, "Select color", black_color)[0], (255, 320))
		select_black_circle(335, 385, settings_circle_radius, settings_outline_radius, self.image)

	def load_buttons(self, update_page=None, update_client=None, client=None):
		self.button("Red", 245, 365, 40, 40, tan_color, tan_highlight, lambda: update_page(red_selection()))
		self.button("Black", 315, 365, 40, 40, tan_color, tan_highlight, lambda: update_page(black_selection()))

		draw_red_circle(265, 385, settings_circle_radius, settings_outline_radius, self.image)
		draw_black_circle(335, 385, settings_circle_radius, settings_outline_radius, self.image)
		self.button("Easy", 225, 150, 150, 30, tan_color, tan_highlight, lambda: update_page(GamePage(True, 1)))
		self.button("Medium", 225, 205, 150, 30, tan_color, tan_highlight, lambda: update_page(GamePage(True, 3)))
		self.button("Hard", 225, 260, 150, 30, tan_color, tan_highlight, lambda: update_page(GamePage(True, 5)))
		self.button("Home", 10, 10, 60, 35, tan_color, tan_highlight, lambda: update_page(Intro()))	



class OnePlayerOptions(Page):
	def load_background(self):
		# TODO: update these numbers -- looks good on the Mac.
		render_centered_text_with_background(70, "New Game", black_color, 100, 25, 400, 80, self.image, tan_color)
		self.image.blit(render_text(25, "Select color", black_color)[0], (255, 320))



	def load_buttons(self, update_page=None, update_client=None, client=None):
		self.button("Red", 245, 365, 40, 40, tan_color, tan_highlight, lambda: update_page(red_selection()))
		self.button("Black", 315, 365, 40, 40, tan_color, tan_highlight, lambda: update_page(black_selection()))
		draw_red_circle(265, 385, settings_circle_radius, settings_outline_radius, self.image)
		draw_black_circle(335, 385, settings_circle_radius, settings_outline_radius, self.image)
		self.button("Easy", 225, 150, 150, 30, tan_color, tan_highlight, lambda: update_page(GamePage(True, 1)))
		self.button("Medium", 225, 205, 150, 30, tan_color, tan_highlight, lambda: update_page(GamePage(True, 3)))
		self.button("Hard", 225, 260, 150, 30, tan_color, tan_highlight, lambda: update_page(GamePage(True, 5)))
		self.button("Home", 10, 10, 60, 35, tan_color, tan_highlight, lambda: update_page(Intro()))	



class TwoPlayerOptions(Page):
    def __init__(self, message = ""):
        Page.__init__(self)
        self.scroll = 0
        self.message = message
        self.timeout = 45

    def handle_event(self, event, set_page, client):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.scroll -= 1
            elif event.button == 5:
                self.scroll += 1

    def load_background(self):
        render_centered_text_with_background(70, "New Game", black_color, 100, 25, 400, 80, self.image, tan_color)

    def load_buttons(self, update_page=None, update_client=None, client=None):
        self.button("Local Game", 100, 150, 180, 30, tan_color, tan_highlight, lambda: update_page(GamePage(False)))
        self.button("Home", 10, 10, 60, 35, tan_color, tan_highlight, lambda: update_page(Intro()))	
        if not client:
            self.button("Play Online", 100, 200, 180, 30, tan_color, tan_highlight, lambda: update_client(startClient()))
        else:
            if client.has_current_game:
                update_page(GamePage(False, networked_game = True))
            self.button("Don't play online", 100, 200, 180, 30, tan_color, tan_highlight, lambda: update_client(None))
            self.show_available_players(client)
        self.show_message(client)

    def show_available_players(self, client):
        render_centered_text_with_background(30, "Available players", black_color, 350, 150, 180, 30, self.image,
                                             tan_color)
        xNum = 350
        yNum = 200
        if hasattr(client, "other_players"):
            pygame.draw.rect(self.image, tan_color, [xNum, yNum, 180, 150])
            if len(client.other_players) == 0:
                render_centered_text_with_background(30, "None", black_color, xNum, yNum, 180, 150,
                                                     self.image, tan_color)

            else:
                self.scroll = drawText(self.image,
                                       client.other_players,
                                       black_color,
                                       [xNum, yNum, 180, 150],
                                       self.scroll,
                                       self.button,
                                       30,
                                       5,
                                       lambda player: client.send_challenge(player))

    def show_message(self, client):
        self.timeout -= 1

        if client:
            if self.message != client.game_message:
                self.message = client.game_message
                self.timeout = 45

            if client.pending_challenge and client.pending_challenge.challenge_to == client.id:
                self.button("Accept", 210, 400, 75, 20, tan_color, tan_highlight,
                            lambda: client.respond_to_challenge(True))
                self.button("Decline", 315, 400, 75, 20, tan_color, tan_highlight,
                            lambda: client.respond_to_challenge(False))
            if self.timeout == 0:
                client.game_message = ""
                client.pending_challenge = None

        if self.timeout == 0:
            self.message = ""
            self.timeout = 45
        if self.timeout:
            render_centered_text(30, self.message, black_color, 100, 370, 400, 20, self.image)


    def __del__(self):
        if hasattr(self, 'timeout'):
            self.timeout = 0


class GamePage(Page):
    def __init__(self, ai_game=False, ai_depth = 1, networked_game = False):
        Page.__init__(self)
        self.initial_click = None
        self.piece = Pieces()
        self.gameState = GameState()
        self.board = self.gameState.get_board_for_network()
        self.possible_moves = []
        self.AIgame = ai_game
        self.scroll = 0
        self.count = 0
        # Weird variables -- basically it prevents the game from reading the same key being pressed too many times.
        self.textinput = TextInput(repeat_keys_initial_ms=40000, repeat_keys_interval_ms=40000)
        self.networked_game = networked_game
        self.AIdepth = ai_depth

    def handle_event(self, event, set_page, client):
        if (self.gameState.activePlayer == 0 or not self.AIgame) and event.type == pg.MOUSEBUTTONDOWN:
            self.handleGameClick(set_page, client)
            if client and client.has_current_game and event.button == 4:
                self.scroll -= 1
            elif client and client.has_current_game and event.button == 5:
                self.scroll += 1
        elif self.AIgame and self.gameState.activePlayer == 1 and not self.gameState.is_game_over(self.gameState.get_all_legal_moves())[0]:
            self.gameState.update_game_state_with_move_helper(self.gameState.get_ai_move(self.AIdepth))
            self.gameState.switch_player()

    def get_text_input(self, events, client):
        if client and client.has_current_game:
            if self.textinput.update(events):
                print('pressed enter: {}'.format(self.count))
                self.count += 1
                text = self.textinput.get_text()
                if text:
                    client.sendMessage(self.textinput.get_text())
                    self.textinput.clear_text()

    def load_buttons(self, update_page=None, update_client=None, client=None):
        if self.networked_game and not client.has_current_game:
            update_page(TwoPlayerOptions())
            return
        if self.AIgame and self.gameState.is_game_over(self.gameState.get_all_legal_moves())[0]:
            is_win = self.check_win(self.gameState.get_all_legal_moves())
            if is_win != -1:
                update_page(WinPage(is_win))
        elif client and client.has_current_game:
            self.scroll = load_chatbox(self.image, client.messages, self.scroll, self.textinput.get_text())
            self.board = client.board
            self.possible_moves = client.possible_moves if client.possible_moves else []
        else:
            self.board = self.gameState.get_board_for_network()
            self.possible_moves = self.gameState.send_possible_moves_for_network()
        self.piece.draw_pieces(self.image, self.board, self.possible_moves, self.initial_click)


    def load_background(self):
        lower = 65
        upper = 105

        for i in range(8):
            for x in range(lower, upper, tile_size):
                for y in range(lower, upper, tile_size):
                    self.image.blit(Tiles.greyTile, (x, y))
                    pg.draw.rect(self.image, black_color, (x, y, tile_size, tile_size), 1)
                lower += 40
                upper += 40

        lower1, upper1, lower2, upper2, = 145, 185, 65, 105
        load_grey_tiles(self.image, lower1, upper1, lower2, upper2, 6)

        lower1, upper1, lower2, upper2, = 225, 265, 65, 105
        load_grey_tiles(self.image, lower1, upper1, lower2, upper2, 4)

        lower1, upper1, lower2, upper2, = 305, 346, 65, 105
        load_grey_tiles(self.image, lower1, upper1, lower2, upper2, 1)

        lower1, upper1, lower2, upper2, = 65, 105, 145, 185
        load_grey_tiles(self.image, lower1, upper1, lower2, upper2, 6)

        lower1, upper1, lower2, upper2, = 65, 105, 225, 265
        load_grey_tiles(self.image, lower1, upper1, lower2, upper2, 4)

        lower1, upper1, lower2, upper2, = 65, 105, 305, 345
        load_grey_tiles(self.image, lower1, upper1, lower2, upper2, 2)

        # draw white tiles
        lower1, upper1, lower2, upper2, = 105, 145, 65, 105
        load_white_tiles(self.image, lower1, upper1, lower2, upper2, 7)

        lower1, upper1, lower2, upper2, = 185, 225, 65, 105
        load_white_tiles(self.image, lower1, upper1, lower2, upper2, 5)

        lower1, upper1, lower2, upper2, = 265, 305, 65, 105
        load_white_tiles(self.image, lower1, upper1, lower2, upper2, 3)

        lower1, upper1, lower2, upper2, = 345, 385, 65, 105
        load_white_tiles(self.image, lower1, upper1, lower2, upper2, 1)

        lower1, upper1, lower2, upper2, = 65, 105, 105, 145
        load_white_tiles(self.image, lower1, upper1, lower2, upper2, 7)

        lower1, upper1, lower2, upper2, = 65, 105, 185, 225
        load_white_tiles(self.image, lower1, upper1, lower2, upper2, 5)

        lower1, upper1, lower2, upper2, = 65, 105, 265, 305
        load_white_tiles(self.image, lower1, upper1, lower2, upper2, 3)

        lower1, upper1, lower2, upper2, = 65, 105, 345, 385
        load_white_tiles(self.image, lower1, upper1, lower2, upper2, 1)

        # game border
        for x in range(55, 65, 10):
            for y in range(65, 385, 10):
                self.image.blit(Tiles.blackTile, (x, y))

        for x in range(385, 395, 10):
            for y in range(65, 385, 10):
                self.image.blit(Tiles.blackTile, (x, y))

        for x in range(55, 395, 10):
            for y in range(55, 65, 10):
                self.image.blit(Tiles.blackTile, (x, y))

        for x in range(55, 395, 10):
            for y in range(385, 395, 10):
                self.image.blit(Tiles.blackTile, (x, y))

    def check_win(self, possible_moves):
        is_win, winner = self.gameState.is_game_over(possible_moves)
        if is_win:
            return winner
        return -1

    def handleGameClick(self, update_page, client):
        pos = pygame.mouse.get_pos()
        image_x = self.screen_rect.center[0] - (SCREEN_START_SIZE[0] * self.scale) / 2
        image_y = self.screen_rect.center[1] - (SCREEN_START_SIZE[1] * self.scale) / 2
        col = int((((pos[0] - image_x) / self.scale - 25) // 40) - 1)
        row = int((((pos[1] - image_y) / self.scale - 25) // 40) - 1)
        made_move = False
        game = client if client and client.has_current_game else self.gameState

        if self.initial_click and self.initial_click in self.possible_moves:
            for possibleMove in self.possible_moves[self.initial_click]:
                if row == possibleMove['endRow'] and col == possibleMove['endColumn']:
                    print("moved from " + str(self.initial_click) + " to (" + str(row) + ", " + str(col) + ")")
                    made_move = True
                    game.update_game_state_with_move(self.initial_click[0], self.initial_click[1], row, col)
            if not made_move:
                print("cannot move from " + str(self.initial_click) + " to (" + str(row) + ", " + str(col) + ")")
                self.initial_click = None

        if (row, col) in self.possible_moves:
            self.initial_click = (row, col)
        if made_move:
            is_win = self.check_win(self.gameState.get_all_legal_moves())
            if is_win != -1:
                update_page(WinPage(is_win))



# TODO: add a 'replay' button?
class WinPage(Page):
	def __init__(self, winner):
		Page.__init__(self)
		self.winner = winner

	def load_background(self):
		if self.winner == 2:
			winnerColor1 = gold_outline
			winnerColor2 = gold_color
		elif self.winner == 0:
			winnerColor1 = red_outline
			winnerColor2 = red_color
		else:
			winnerColor1 = black_outline
			winnerColor2 = black_color
		draw_circle(50, 50, winnerColor2, winnerColor1, 40, 45, self.image)
		draw_circle(550, 50, winnerColor2, winnerColor1, 40, 45, self.image)
		draw_circle(50, 400, winnerColor2, winnerColor1, 40, 45, self.image)
		draw_circle(550, 400, winnerColor2, winnerColor1, 40, 45, self.image)
		self.image.blit(render_text(25, "Play", gold_color)[0], (535, 385))
		self.image.blit(render_text(25, "Again", gold_color)[0], (530, 405))

		draw_circle(150, 400, gold_color, gold_outline, 25, 30, self.image)
		draw_circle(225, 400, gold_color, gold_outline, 25, 30, self.image)
		draw_circle(300, 400, gold_color, gold_outline, 25, 30, self.image)
		draw_circle(375, 400, gold_color, gold_outline, 25, 30, self.image)
		draw_circle(450, 400, gold_color, gold_outline, 25, 30, self.image)

		draw_circle(190, 325, gold_color, gold_outline, 25, 30, self.image)
		draw_circle(265, 325, gold_color, gold_outline, 25, 30, self.image)
		draw_circle(340, 325, gold_color, gold_outline, 25, 30, self.image)
		draw_circle(415, 325, gold_color, gold_outline, 25, 30, self.image)

		draw_circle(225, 250, gold_color, gold_outline, 25, 30, self.image)
		draw_circle(300, 250, gold_color, gold_outline, 25, 30, self.image)
		draw_circle(375, 250, gold_color, gold_outline, 25, 30, self.image)

		draw_circle(265, 175, gold_color, gold_outline, 25, 30, self.image)
		draw_circle(340, 175, gold_color, gold_outline, 25, 30, self.image)

		pygame.draw.circle(self.image, gold_outline, (300, 100), 30, 30)
		pygame.draw.circle(self.image, winnerColor2, (300, 100), 25, 25)

		if self.winner == 2:
			text = "It's a Draw!"
		else:
			if self.winner == 0:
				text = "Red Wins!"
			else:
				text = "Black Wins!"
		self.image.blit(render_text(80, text, gold_color)[0], (165, 5))

	def load_buttons(self, update_page=None, update_client=None, client=None):
		self.button("home", 475, 350, 150, 150, tan_color, tan_highlight, lambda: update_page(Intro()))


class ScreenControl(object):
    def __init__(self):
        pg.init()
        pg.display.set_caption(CAPTION)
        self.screen = pg.display.set_mode(SCREEN_START_SIZE, pg.RESIZABLE)
        self.screen_rect = self.screen.get_rect()
        self.image = pg.Surface(SCREEN_START_SIZE).convert()
        self.image_rect = self.image.get_rect()
        self.scale = 1
        self.clock = pg.time.Clock()
        self.fps = 10.0
        self.done = False
        self.keys = pg.key.get_pressed()
        self.client = None
        self.page = Intro()
        self.scroll = 0

    def screen_event(self):
        events = pg.event.get()
        for event in events:
            self.keys = pg.key.get_pressed()
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type == pg.VIDEORESIZE:
                self.screen = pg.display.set_mode(event.size, pg.RESIZABLE)
                self.screen_rect = self.screen.get_rect()
            else:
                self.page.handle_event(event, self.set_page, self.client)
        self.page.get_text_input(events, self.client)
        if self.client:
            self.client.pump()

    def screen_update(self):
        self.page.update(self.image, self.screen_rect, self.scale, self.set_page, self.set_done, self.set_client,
                         self.client)
        if self.screen_rect.size != SCREEN_START_SIZE:
            fit_to_rect = self.image_rect.fit(self.screen_rect)
            fit_to_rect.center = self.screen_rect.center
            scaled = pg.transform.smoothscale(self.image, fit_to_rect.size)
            self.scale = fit_to_rect.width / SCREEN_START_SIZE[0]
            self.screen.blit(scaled, fit_to_rect)
        else:
            self.screen.blit(self.image, (0, 0))

    def main(self):
        while not self.done:
            if self.client and self.client.error:
                print("in main")
                self.client = None
                if isinstance(self.page, GamePage) and self.client.has_current_game:
                    self.page = TwoPlayerOptions("There was a problem connecting to the server.")
                elif isinstance(self.page, TwoPlayerOptions):
                    self.page = TwoPlayerOptions("There was a problem connecting to the server.")
            self.screen_event()
            self.screen_update()
            pg.display.update()
            self.clock.tick(self.fps)

    def set_page(self, page):
        self.page = page

    def set_client(self, client):
        print('clicked')
        self.client = client

    def set_done(self, done):
        self.done = done



if __name__ == "__main__":
	run_it = ScreenControl()
	run_it.main()
	pg.quit()
	sys.exit()
