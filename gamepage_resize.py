"""
For game window resizing uses code from:
https://github.com/Mekire/pygame-samples/blob/master/resizable/resizable_aspect_ratio.py
"""

from graphics_helpers import *
from client import *


class Pieces(object):
    def draw_pieces(self, window, game, selected):
        board = game.get_board_for_network()
        possible_moves = game.send_possible_moves_for_network()
        # TODO: this always shows black on the bottom of the screen.
        for item in board:
            is_possible = (item[0], item[1]) in possible_moves
            is_selected = True if selected == item else False
            color = 'red' if board[item] == 'r' or board[item] == 'R' else 'black'
            is_king = True if board[item] == 'R' or board[item] == 'B' else False
            if board[item] != '.' and board[item] != '_':
                available_moves = possible_moves[item] if is_selected else []
                self.draw_piece(window, color, item[0], item[1], is_possible, is_king, is_selected, available_moves)

    def draw_piece(self, window, piece_color, row, col, is_possible, is_king, is_selected, available_moves):
        outline = red_outline if piece_color == 'red' else black_outline
        color = red_color if piece_color == 'red' else black_color
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

    def get_background(self):
        return self.background


class Intro(Page):
    def load_intro(self, window: pg.Surface):
        draw_black_circle(450, 150, intro_circle_radius, intro_outline_radius, window)
        draw_red_circle(350, 150, intro_circle_radius, intro_outline_radius, window)
        draw_black_circle(250, 150, intro_circle_radius, intro_outline_radius, window)
        draw_red_circle(150, 150, intro_circle_radius, intro_outline_radius, window)
        window.blit(render_text(100, "Checkers", gold_color), (80, 70))


class Settings(Page):
    def load_settings(self, window: pg.Surface):
        pg.draw.rect(window, tan_color, [100, 25, 400, 80])
        window.blit(render_text(70, "Settings", black_color), (150, 5))
        window.blit(render_text(25, "Preferred color", black_color), (210, 320))


class OnePlayerOptions(Page):
    def load_1p_options(self, window: pg.Surface):
        pg.draw.rect(window, tan_color, [100, 25, 400, 80])
        window.blit(render_text(70, "New Game", black_color), (150, 5))
        window.blit(render_text(25, "Select color", black_color), (230, 320))


class TwoPlayerOptions(Page):
    def load_2p_options(self, window: pg.Surface):
        pg.draw.rect(window, tan_color, [100, 25, 400, 80])
        window.blit(render_text(70, "New Game", black_color), (150, 5))


class GamePage(Page):
    def __init__(self, ai_game=False):
        Page.__init__(self)
        self.initial_click = None
        self.piece = Pieces()
        self.gameState = GameState()
        self.gameState.get_all_legal_moves()
        self.AIgame = ai_game

    def load_board(self, window: pg.Surface):
        lower = 65
        upper = 105

        for i in range(8):
            for x in range(lower, upper, tile_size):
                for y in range(lower, upper, tile_size):
                    window.blit(Tiles.greyTile, (x, y))
                    pg.draw.rect(window, black_color, (x, y, tile_size, tile_size), 1)
                lower += 40
                upper += 40

        lower1, upper1, lower2, upper2, = 145, 185, 65, 105
        load_grey_tiles(window, lower1, upper1, lower2, upper2, 6)

        lower1, upper1, lower2, upper2, = 225, 265, 65, 105
        load_grey_tiles(window, lower1, upper1, lower2, upper2, 4)

        lower1, upper1, lower2, upper2, = 305, 346, 65, 105
        load_grey_tiles(window, lower1, upper1, lower2, upper2, 1)

        lower1, upper1, lower2, upper2, = 65, 105, 145, 185
        load_grey_tiles(window, lower1, upper1, lower2, upper2, 6)

        lower1, upper1, lower2, upper2, = 65, 105, 225, 265
        load_grey_tiles(window, lower1, upper1, lower2, upper2, 4)

        lower1, upper1, lower2, upper2, = 65, 105, 305, 345
        load_grey_tiles(window, lower1, upper1, lower2, upper2, 2)

        # draw white tiles
        lower1, upper1, lower2, upper2, = 105, 145, 65, 105
        load_white_tiles(window, lower1, upper1, lower2, upper2, 7)

        lower1, upper1, lower2, upper2, = 185, 225, 65, 105
        load_white_tiles(window, lower1, upper1, lower2, upper2, 5)

        lower1, upper1, lower2, upper2, = 265, 305, 65, 105
        load_white_tiles(window, lower1, upper1, lower2, upper2, 3)

        lower1, upper1, lower2, upper2, = 345, 385, 65, 105
        load_white_tiles(window, lower1, upper1, lower2, upper2, 1)

        lower1, upper1, lower2, upper2, = 65, 105, 105, 145
        load_white_tiles(window, lower1, upper1, lower2, upper2, 7)

        lower1, upper1, lower2, upper2, = 65, 105, 185, 225
        load_white_tiles(window, lower1, upper1, lower2, upper2, 5)

        lower1, upper1, lower2, upper2, = 65, 105, 265, 305
        load_white_tiles(window, lower1, upper1, lower2, upper2, 3)

        lower1, upper1, lower2, upper2, = 65, 105, 345, 385
        load_white_tiles(window, lower1, upper1, lower2, upper2, 1)

        # game border
        for x in range(55, 65, 10):
            for y in range(65, 385, 10):
                window.blit(Tiles.blackTile, (x, y))

        for x in range(385, 395, 10):
            for y in range(65, 385, 10):
                window.blit(Tiles.blackTile, (x, y))

        for x in range(55, 395, 10):
            for y in range(55, 65, 10):
                window.blit(Tiles.blackTile, (x, y))

        for x in range(55, 395, 10):
            for y in range(385, 395, 10):
                window.blit(Tiles.blackTile, (x, y))

        load_chatbox(window)

    def check_win(self):
        if self.gameState.is_game_over():
            if self.gameState.is_draw():
                return 2
            else:
                return self.gameState.is_win()
        return -1


class WinPage(Page):
    def __init__(self, winner):
        Page.__init__(self)
        self.winner = winner

    def load_win_page(self, window):
        if self.winner == 2:
            winnerColor1 = gold_outline
            winnerColor2 = gold_color
        elif self.winner == 0:
            winnerColor1 = red_outline
            winnerColor2 = red_color
        else:
            winnerColor1 = black_outline
            winnerColor2 = black_color
        # button("home", 950, 700, 300, 300, tan_color, tan_highlight, 'home')
        draw_circle(50, 50, winnerColor2, winnerColor1, 40, 45, window)
        draw_circle(550, 50, winnerColor2, winnerColor1, 40, 45, window)
        draw_circle(50, 400, winnerColor2, winnerColor1, 40, 45, window)
        draw_circle(550, 400, winnerColor2, winnerColor1, 40, 45, window)
        window.blit(render_text(25, "Play", gold_color), (530, 370))
        window.blit(render_text(25, "Again", gold_color), (525, 390))

        draw_circle(150, 400, gold_color, gold_outline, 25, 30, window)
        draw_circle(225, 400, gold_color, gold_outline, 25, 30, window)
        draw_circle(300, 400, gold_color, gold_outline, 25, 30, window)
        draw_circle(375, 400, gold_color, gold_outline, 25, 30, window)
        draw_circle(450, 400, gold_color, gold_outline, 25, 30, window)

        draw_circle(190, 325, gold_color, gold_outline, 25, 30, window)
        draw_circle(265, 325, gold_color, gold_outline, 25, 30, window)
        draw_circle(340, 325, gold_color, gold_outline, 25, 30, window)
        draw_circle(415, 325, gold_color, gold_outline, 25, 30, window)

        draw_circle(225, 250, gold_color, gold_outline, 25, 30, window)
        draw_circle(300, 250, gold_color, gold_outline, 25, 30, window)
        draw_circle(375, 250, gold_color, gold_outline, 25, 30, window)

        draw_circle(265, 175, gold_color, gold_outline, 25, 30, window)
        draw_circle(340, 175, gold_color, gold_outline, 25, 30, window)

        pygame.draw.circle(window, gold_outline, (300, 100), 30, 30)
        pygame.draw.circle(window, winnerColor2, (300, 100), 25, 25)

        if self.winner == 2:
            text = "It's a Draw!"
        else:
            text = "You Win!"
        window.blit(render_text(80, text, gold_color), (150, 5))


class ScreenControl(object):
    def __init__(self):
        pg.init()
        pg.display.set_caption(CAPTION)
        self.screen = pg.display.set_mode(SCREEN_START_SIZE, pg.RESIZABLE)
        self.screen_rect = self.screen.get_rect()
        self.image = pg.Surface(SCREEN_START_SIZE).convert()
        self.image_rect = self.image.get_rect()
        self.page = Intro()
        self.scale = 1
        self.clock = pg.time.Clock()
        self.fps = 15.0
        self.done = False
        self.keys = pg.key.get_pressed()
        self.client = None

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        cur = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        image_x = self.screen_rect.center[0] - (SCREEN_START_SIZE[0] * self.scale) / 2
        image_y = self.screen_rect.center[1] - (SCREEN_START_SIZE[1] * self.scale) / 2
        if (x + w) * self.scale + image_x > cur[0] > x * self.scale + image_x and\
                (y + h) * self.scale + image_y > cur[1] > y * self.scale + image_y:
            if action is not None and action != "home":
                pg.draw.rect(self.image, ac, (x, y, w, h))
            if click[0] == 1 and action is not None:
                if action == "quit":
                    self.done = True
                if action == "soundOn":
                    pass
                if action == "soundOff":
                    pass
                if action == "challenge" and self.client:
                    self.client.sendChallenge(msg)
                if action == 'listOnline':
                    if not self.client:
                        self.client = startClient()
                        self.client.pump()
                if action == "player1":
                    self.page = OnePlayerOptions()
                if action == "player2":
                    self.page = TwoPlayerOptions()
                if action == "settings":
                    self.page = Settings()  # loadSettingsPage()
                if action == "PlayOnline":
                    print("clicked play online")
                if action == "LocalGame":
                    self.page = GamePage(False)
                if action == "p1":                        # WHAT IS THIS
                    print("In action p1")
                if action == "p2":
                    print("In action p2")
                # game loop for one player
                if action == "main1":
                    self.page = GamePage(True)
                # game loop for two player
                if action == "main2":
                    self.page = GamePage(False)
                if action == "home":
                    self.page = Intro()
        else:
            if action is not None and action != "home":
                pg.draw.rect(self.image, ic, (x, y, w, h))

    def settings_quit_btn(self):
        if not isinstance(self.page, WinPage):
            self.button("quit", 515, 425, 70, 20, tan_color, tan_highlight, 'quit')
            self.image.blit(render_text(15, "Quit", black_color), (535, 423))
        if not isinstance(self.page, Settings) and not isinstance(self.page, WinPage):
            self.button("settings", 515, 20, 70, 20, tan_color, tan_highlight, 'settings')
            self.image.blit(render_text(15, "Settings", black_color), (520, 18))

    def load_intro_buttons(self):
        self.button("player1", 125, 300, 150, 34, tan_color, tan_highlight, 'player1')
        self.image.blit(render_text(28, "1-Player", black_color), (150, 295))
        self.button("player2", 325, 300, 150, 34, tan_color, tan_highlight, 'player2')
        self.image.blit(render_text(28, "2-Player", black_color), (350, 295))

    def load_settings_buttons(self):
        draw_red_circle(265, 385, settings_circle_radius, settings_outline_radius, self.image)
        draw_black_circle(335, 385, settings_circle_radius, settings_outline_radius, self.image)
        self.button("soundOn", 100, 150, 60, 20, tan_color, tan_highlight, 'soundOn')
        self.image.blit(render_text(12, "Sound On", black_color), (103, 152))
        self.button("soundOff", 175, 150, 60, 20, tan_color, tan_highlight, 'soundOff')
        self.image.blit(render_text(12, "Sound Off", black_color), (177, 152))
        self.button("listOnline", 350, 150, 150, 30, tan_color, tan_highlight, 'listOnline')
        self.image.blit(render_text(20, "List me online", black_color), (365, 150))
        self.button("2 player page", 350, 185, 150, 30, tan_color, tan_highlight, 'player2')
        self.image.blit(render_text(20, "2 player page", black_color), (365, 185))
        pg.draw.rect(self.image, tan_color, (210, 230, 180, 30))
        self.image.blit(render_text(20, "Update Username", black_color), (215, 230))
        pg.draw.rect(self.image, tan_color, (210, 270, 180, 30))
        self.image.blit(render_text(20, "Update Password", black_color), (215, 270))

    def load_1p_options_button(self):
        draw_red_circle(265, 385, settings_circle_radius, settings_outline_radius, self.image)
        draw_black_circle(335, 385, settings_circle_radius, settings_outline_radius, self.image)
        self.button("easy", 225, 150, 150, 30, tan_color, tan_highlight, 'main1')
        self.image.blit(render_text(24, "Easy", black_color), (270, 145))
        self.button("medium", 225, 205, 150, 30, tan_color, tan_highlight, 'main1')
        self.image.blit(render_text(24, "Medium", black_color), (260, 200))
        self.button("hard", 225, 260, 150, 30, tan_color, tan_highlight, 'main1')
        self.image.blit(render_text(24, "Hard", black_color), (270, 255))

    def load_2p_options_button(self):
        self.button("LocalGame", 100, 150, 150, 30, tan_color, tan_highlight, 'main2')
        self.image.blit(render_text(28, "Local Game", black_color), (105, 145))
        self.button("PlayOnline", 350, 150, 150, 30, tan_color, tan_highlight, 'PlayOnline')
        self.image.blit(render_text(28, "Play Online", black_color), (355, 145))

        xNum = 350
        yNum = 200
        if self.client and hasattr(self.client, "otherPlayers"):
            for player in self.client.otherPlayers:
                # I need to be able to make a button for each player too.
                self.button(player, xNum, yNum, 150, 30, tan_color, tan_highlight, "challenge")
                self.image.blit(render_text(20, player, black_color), (xNum, yNum))
                yNum += 30
        else:
            self.button("Find online players.", 350, 200, 180, 30, tan_color, tan_highlight, "listOnline")
            self.image.blit(render_text(20, "Find online players", black_color), (350, 200))

        self.button("player1", 210, 400, 75, 20, tan_color, tan_highlight, 'p1')
        self.image.blit(render_text(18, "Accept", black_color), (215, 395))
        self.button("player2", 315, 400, 75, 20, tan_color, tan_highlight, 'p2')
        self.image.blit(render_text(18, "Decline", black_color), (320, 395))

        if self.client and self.client.hasChallenge:
            self.client.pump()
            if hasattr(self.client, "challengeFrom"):
                self.button("Received challenge from " + self.client.challengeFrom + ". Do you want to accept?", xNum,
                            yNum + 50, 150, 30, tan_color, tan_highlight, 'main2')
                self.image.blit(render_text(20, "Received challenge", black_color), (xNum, 330))
            else:
                self.button("Sent challenge", xNum, yNum + 50, 150, 30, tan_color, tan_highlight, 'main2')
                self.image.blit(render_text(20, "Waiting for player to respond...", black_color), (xNum, 330))

    def load_winpage_buttons(self):
        self.button("home", 475, 350, 150, 150, tan_color, tan_highlight, 'home')

    def screen_event(self):
        for event in pg.event.get():
            self.keys = pg.key.get_pressed()
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type == pg.VIDEORESIZE:
                self.screen = pg.display.set_mode(event.size, pg.RESIZABLE)
                self.screen_rect = self.screen.get_rect()
            elif isinstance(self.page, GamePage) and (self.page.gameState.activePlayer == 0 or not self.page.AIgame) \
                    and event.type == pg.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    image_x = self.screen_rect.center[0] - (SCREEN_START_SIZE[0] * self.scale) / 2
                    image_y = self.screen_rect.center[1] - (SCREEN_START_SIZE[1] * self.scale) / 2
                    col = int((((pos[0] - image_x) / self.scale - 25) // 40) - 1)
                    row = int((((pos[1] - image_y) / self.scale - 25) // 40) - 1)

                    made_move = False
                    if self.page.initial_click:
                        for possibleMove in self.page.gameState.board[self.page.initial_click[0]][self.page.initial_click[1]].possibleMoves:
                            if row == possibleMove.endRow and col == possibleMove.endColumn:
                                print("moved from " + str(self.page.initial_click) + " to (" + str(row) + ", " + str(col) + ")")
                                made_move = True
                                self.page.gameState.update_game_state_with_move(possibleMove)
                                self.page.gameState.switch_player()
                                self.page.gameState.get_all_legal_moves()

                        if not made_move:
                            print("cannot move from " + str(self.page.initial_click) + " to (" + str(row) + ", " + str(col) + ")")
                            self.page.initial_click = None
                    possible_moves = self.page.gameState.send_possible_moves_for_network()   # NEED A BETTER PLACE FOR IT, MAYBE A PARAMTER IN CLASS
                    if (row, col) in possible_moves:
                        self.page.initial_click = (row, col)
                    if made_move:
                        is_win = self.page.check_win()
                        if is_win != -1:
                            self.page = WinPage(is_win)
        if self.client:
            self.client.pump()

    def screen_update(self):
        self.image.blit(self.page.get_background(), (0, 0))
        if isinstance(self.page, Intro):
            self.page.load_intro(self.image)
            self.load_intro_buttons()
        elif isinstance(self.page, Settings):
            if self.client:
                self.client.closeConnection()
            self.page.load_settings(self.image)
            self.load_settings_buttons()
        elif isinstance(self.page, OnePlayerOptions):
            self.page.load_1p_options(self.image)
            self.load_1p_options_button()
        elif isinstance(self.page, TwoPlayerOptions):
            self.page.load_2p_options(self.image)
            self.load_2p_options_button()
        elif isinstance(self.page, GamePage):
            self.page.load_board(self.image)
            self.page.piece.draw_pieces(self.image, self.page.gameState, self.page.initial_click)
        elif isinstance(self.page, WinPage):
            self.page.load_win_page(self.image)
            self.load_winpage_buttons()
        self.settings_quit_btn()
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
            self.screen_event()
            self.screen_update()
            pg.display.update()
            self.clock.tick(self.fps)
            if isinstance(self.page, GamePage) and self.page.AIgame and self.page.gameState.activePlayer == 1:
                self.page.gameState.update_game_state_with_move(self.page.gameState.get_ai_move())
                self.page.gameState.switch_player()
                self.page.gameState.get_all_legal_moves()
                is_win = self.page.check_win()
                if is_win != -1:
                    self.page = WinPage(is_win)
        if self.client:
            self.client.closeConnection()


if __name__ == "__main__":
    run_it = ScreenControl()
    run_it.main()
    pg.quit()
    sys.exit()
