"""
For game window resizing uses code from:
https://github.com/Mekire/pygame-samples/blob/master/resizable/resizable_aspect_ratio.py
"""

from graphics_helpers import *
from client import *
from pygame_textinput import *
from classes import *
import os.path
from random_usernames import *
import random
from datetime import datetime
from numpy import load

settings_file_name = "lyra_checkers_settings.txt"

class Pieces(object):
    def draw_pieces(self, window, board, possible_moves, selected, color):
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
        self.timeout = 45
        self.message = ""
        self.screen_rect = None
        self.scale = None
        self.image = None
        self.user_info = None

    def settings_quit_btn(self, set_done, set_page):
        if not isinstance(self, WinPage):
            self.button("Quit", 505, 410, 85, 30, tan_color, tan_highlight, lambda: set_done(True))
        if isinstance(self, WinPage):
            self.button("Quit", 510, 385, 80, 30, gold_color, tan_highlight, lambda: set_done(True))
        if not isinstance(self, Settings) and not isinstance(self, WinPage):
            self.button("Settings", 505, 10, 85, 30, tan_color, tan_highlight, lambda: set_page(Settings()))
        if not isinstance(self, Intro):
            if not isinstance(self, WinPage):
                self.button("Home", 10, 10, 85, 30, tan_color, tan_highlight, lambda: set_page(Intro()))
            else:
                self.button("Home", 10, 35, 80, 30, gold_color, tan_highlight, lambda: set_page(Intro()))

    def update(self, window: pg.Surface, screen_rect, scale, update_page, update_done, update_client, client, user_info):
        self.screen_rect = screen_rect
        self.scale = scale
        self.image = window
        self.user_info = user_info

        self.image.blit(self.background, (0, 0))

        self.load_background()
        self.load_buttons(update_page, update_client, client)
        self.settings_quit_btn(update_done, update_page)

    def update_user_settings(self):
        file = open(settings_file_name, 'w')
        file_text = "\n".join(self.user_info)
        file.write(file_text)
        file.close()

    def show_message(self, client, messagex = 100, messagey=370, acceptx = 210, accepty = 400):
        self.timeout -= 1

        if client:
            if self.message != client.game_message:
                self.message = client.game_message
                self.timeout = 45

            if client.pending_challenge and client.pending_challenge.challenge_to == client.id:
                self.button("Accept", acceptx, accepty, 75, 20, tan_color, tan_highlight,
                            lambda: client.respond_to_challenge(True))
                self.button("Decline", acceptx + 115, accepty, 75, 20, tan_color, tan_highlight,
                            lambda: client.respond_to_challenge(False))
            if self.timeout == 0:
                client.game_message = ""
                client.pending_challenge = None

        if self.timeout == 0:
            self.message = ""
            self.timeout = 45
        if self.timeout:
            render_centered_text(30, self.message, black_color, messagex, messagey, 400, 20, self.image)


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
               onClick=None, font_size = 28):
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
                render_centered_text_with_background(font_size, msg, black_color, top_left_x_coordinate, top_left_y_coordinate,
                                                     width, height,
                                                     self.image, active_color)
            if click[0] == 1 and onClick is not None:
                onClick()
        else:
            if onClick is not None and msg != "home":
                render_centered_text_with_background(font_size, msg, black_color, top_left_x_coordinate, top_left_y_coordinate,
                                                     width, height,
                                                     self.image, inactive_color)


class Intro(Page):
    def load_background(self):
        border(self.image)
        draw_black_circle(450, 150, intro_circle_radius, intro_outline_radius, self.image)
        draw_red_circle(350, 150, intro_circle_radius, intro_outline_radius, self.image)
        draw_black_circle(250, 150, intro_circle_radius, intro_outline_radius, self.image)
        draw_red_circle(150, 150, intro_circle_radius, intro_outline_radius, self.image)
        render_centered_text(100, "Checkers", gold_color, 265, 110, intro_circle_radius, intro_outline_radius,
                             self.image)

    def load_buttons(self, update_page=None, update_client=None, client=None):
        self.button("One Player", 125, 300, 150, 30, tan_color, tan_highlight, lambda: update_page(OnePlayerOptions(0)))
        self.button("Two Player", 325, 300, 150, 30, tan_color, tan_highlight, lambda: update_page(TwoPlayerOptions()))
        self.show_message(client)


class Settings(Page):
    def __init__(self):
        Page.__init__(self)
        self.textinput = TextInput(repeat_keys_initial_ms=40000, repeat_keys_interval_ms=40000)

    def load_background(self):
        border(self.image)
        if len(self.textinput.get_text()) == 0 or len(self.textinput.get_text()) > 19:
            self.textinput = TextInput(repeat_keys_initial_ms=40000, repeat_keys_interval_ms=40000, initial_string = self.user_info[0])

        render_centered_text_with_background(70, "Settings", black_color, 100, 25, 400, 80, self.image, tan_color)
        render_centered_text_with_background(20, 'USERNAME', black_color, 100, 150, 150, 30, self.image, tan_color)
        render_centered_text_with_background(20, self.textinput.get_text(), black_color, 100, 180, 150, 30, self.image, white_color)
        render_centered_text_with_background(20, "STATISTICS", black_color, 100, 225, 150, 30, self.image, tan_color)
        render_centered_text_with_background(20, "Wins: " + self.user_info[1], black_color, 100, 255, 150, 30, self.image, tan_color)
        render_centered_text_with_background(20, "Losses: " + self.user_info[2], black_color, 100, 285, 150, 30, self.image, tan_color)
        render_centered_text_with_background(20, "Draws: " + self.user_info[3], black_color, 100, 315, 150, 30, self.image, tan_color)

    def load_buttons(self, update_page=None, update_client=None, client=None):
        if (client):
            self.button("Don't play online", 350, 225, 150, 30, tan_color, tan_highlight, lambda: update_client(None))
        else:
            self.button("List Online", 350, 225, 150, 30, tan_color, tan_highlight, lambda: update_client(startClient(self.user_info[0])))
        self.button("Save Username", 350, 150, 150, 30, tan_color, tan_highlight, lambda: self.update_username(), font_size=20)

        self.show_message(client)

    def get_text_input(self, events, client):
        if self.textinput.update(events):
            self.update_username()

    def update_username(self):
        text = self.textinput.get_text()
        if text:
            self.user_info[0] = text
            self.update_user_settings()
            return self.user_info


class OnePlayerOptions(Page):
    def __init__(self, color):
        Page.__init__(self)
        self.color = color

    def load_background(self):
        # TODO: update these numbers -- looks good on the Mac.
        border(self.image)
        render_centered_text_with_background(70, "New Game", black_color, 100, 25, 400, 80, self.image, tan_color)
        self.image.blit(render_text(25, "Select color", black_color)[0], (255, 320))
        if self.color == 1:
            select_black_circle(335, 385, settings_circle_radius, settings_outline_radius, self.image)
        else:
            select_red_circle(265, 385, settings_circle_radius, settings_outline_radius, self.image)

    def load_buttons(self, update_page=None, update_client=None, client=None):
        self.button("Red", 245, 365, 40, 40, tan_color, tan_highlight, lambda: update_page(OnePlayerOptions(0)))
        self.button("Black", 315, 365, 40, 40, tan_color, tan_highlight, lambda: update_page(OnePlayerOptions(1)))
        draw_red_circle(265, 385, settings_circle_radius, settings_outline_radius, self.image)
        draw_black_circle(335, 385, settings_circle_radius, settings_outline_radius, self.image)
        self.button("Easy", 225, 150, 150, 30, tan_color, tan_highlight, lambda: update_page(GamePage(True, 1, color = self.color, load_qtable=True)))
        self.button("Medium", 225, 205, 150, 30, tan_color, tan_highlight, lambda: update_page(GamePage(True, 3, color = self.color)))
        self.button("Hard", 225, 260, 150, 30, tan_color, tan_highlight, lambda: update_page(GamePage(True, 5, color = self.color)))


class TwoPlayerOptions(Page):
    def __init__(self, message = ""):
        Page.__init__(self)
        self.scroll = 0
        self.message = message

    def handle_event(self, event, set_page, client):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.scroll -= 1
            elif event.button == 5:
                self.scroll += 1

    def load_background(self):
        border(self.image)
        render_centered_text_with_background(70, "New Game", black_color, 100, 25, 400, 80, self.image, tan_color)

    def load_buttons(self, update_page=None, update_client=None, client=None):
        self.button("Local Game", 100, 150, 150, 30, tan_color, tan_highlight, lambda: update_page(GamePage(False)))
        if not client:
            self.button("Play Online", 100, 200, 150, 30, tan_color, tan_highlight, lambda: update_client(startClient(self.user_info[0])))
        else:
            self.button("Don't play online", 100, 200, 150, 30, tan_color, tan_highlight, lambda: update_client(None))
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
                                       client.other_players_usernames,
                                       black_color,
                                       [xNum, yNum, 180, 150],
                                       self.scroll,
                                       self.button,
                                       30,
                                       5,
                                       lambda playerId, playerName: client.send_challenge(playerId, playerName),
                                       client.other_players)


    def __del__(self):
        if hasattr(self, 'timeout'):
            self.timeout = 0


class GamePage(Page):
    def __init__(self, ai_game=False, ai_depth = 1, networked_game = False, color = 0, load_qtable=False):
        Page.__init__(self)
        self.initial_click = None
        self.piece = Pieces()
        self.gameState = GameState()
        self.board = self.gameState.get_board_for_network()
        self.possible_moves = []
        self.AIgame = ai_game
        self.scroll = 0
        # Weird variables -- basically it prevents the game from reading the same key being pressed too many times.
        self.textinput = TextInput(repeat_keys_initial_ms=40000, repeat_keys_interval_ms=40000)
        self.networked_game = networked_game
        self.AIdepth = ai_depth
        self.color = color
        self.qTable = {} if not load_qtable else load("450000_exp4.npy").item()

    def handle_event(self, event, set_page, client):
        if (self.gameState.activePlayer == self.color or not self.AIgame) and event.type == pg.MOUSEBUTTONDOWN:
            self.handleGameClick(client)
            if client and client.has_current_game and event.button == 4:
                self.scroll -= 1
            elif client and client.has_current_game and event.button == 5:
                self.scroll += 1
        elif self.AIgame and self.gameState.activePlayer != self.color and not self.gameState.is_game_over(self.gameState.get_all_legal_moves())[0]:
            self.gameState.update_game_state_with_move_helper(self.gameState.get_ai_move(self.AIdepth, self.qTable))
            self.gameState.switch_player()

    def get_text_input(self, events, client):
        if client and client.has_current_game:
            if self.textinput.update(events):
                text = self.textinput.get_text()
                if text:
                    client.sendMessage(self.textinput.get_text())
                    self.textinput.clear_text()

    def load_buttons(self, update_page=None, update_client=None, client=None):
        if self.networked_game and not (client and client.has_current_game):
            update_page(TwoPlayerOptions(), "There is a problem with the server.")
            return
        is_win = self.check_win(client)
        if is_win != -1:
            if self.networked_game or self.AIgame:
                if is_win == self.color:
                    self.user_info[1] = str(1 + int(self.user_info[1]))
                elif is_win == 2:
                    self.user_info[3] = str(1 + int(self.user_info[3]))
                else:
                    self.user_info[2] = str(1 + int(self.user_info[2]))
                self.update_user_settings()
            update_page(WinPage(is_win, self.get_winner_name(is_win, client)))
        elif client and client.has_current_game:
            self.scroll = load_chatbox(self.image, client.messages, self.scroll, self.textinput.get_text())
            self.board = client.board
            self.possible_moves = client.possible_moves if client.possible_moves else []
            self.color = client.color
        else:
            self.board = self.gameState.get_board_for_network(self.color)
            self.possible_moves = self.gameState.send_possible_moves_for_network(self.color)
        self.piece.draw_pieces(self.image, self.board, self.possible_moves, self.initial_click, self.color)

    def load_background(self):
        border(self.image)
        lower = 65

        for i in range(8):
            for j in range(8):
                tile = Tiles.greyTile if (i + j) % 2 else Tiles.whiteTile
                self.image.blit(tile, (lower + i * tile_size, lower + j * tile_size))
                pg.draw.rect(self.image, black_color, (lower + i * tile_size, lower + j * tile_size, tile_size, tile_size), 1)

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

    def check_win(self, client):
        if self.networked_game:
            return client.winner
        else:
            possible_moves = self.gameState.get_all_legal_moves()
            is_win, winner = self.gameState.is_game_over(possible_moves)
            if is_win:
                return winner
            return -1

    def get_winner_name(self, is_win, client):
        if self.networked_game:
            return client.winner_name

        win_color = "Red" if is_win == 0 else "Black"
        if self.AIgame:
            return self.user_info[0] if is_win == self.color else win_color
        else:
            return win_color

    def handleGameClick(self, client):
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
                    made_move = True
                    startRow = self.initial_click[0]
                    startCol = self.initial_click[1]
                    if not self.color:
                      col = 7 - col
                      row = 7 - row
                      startRow = 7 - startRow
                      startCol = 7 - startCol

                    game.update_game_state_with_move(startRow, startCol, row, col)
            if not made_move:
                self.initial_click = None

        if (row, col) in self.possible_moves:
            self.initial_click = (row, col)


class WinPage(Page):
    def __init__(self, winner, winner_name):
        Page.__init__(self)
        self.winner = winner
        self.winner_name = winner_name

    def load_background(self):
        border(self.image)
        if self.winner == 2:
            winnerColor1 = gold_outline
            winnerColor2 = gold_color
        elif self.winner == 0:
            winnerColor1 = red_outline
            winnerColor2 = red_color
        else:
            winnerColor1 = black_outline
            winnerColor2 = black_color

        for h in [50, 400]:
            draw_circle(50, h, winnerColor2, winnerColor1, 40, 45, self.image)
            draw_circle(550, h, winnerColor2, winnerColor1, 40, 45, self.image)

        # TODO: this isn't a button. If we turn it into a button, where should it lead to?
        # self.image.blit(render_text(25, "Play", gold_color)[0], (535, 385))
        # self.image.blit(render_text(25, "Again", gold_color)[0], (530, 405))

        for i in range(5):
            draw_circle(150 + 75 * i, 400, gold_color, gold_outline, 25, 30, self.image)

        for j in range(4):
            draw_circle(190 + 75 * j, 325, gold_color, gold_outline, 25, 30, self.image)

        for k in range(3):
            draw_circle(225 + 75 * k, 250, gold_color, gold_outline, 25, 30, self.image)

        for l in range(2):
            draw_circle(265 + 75 * l, 175, gold_color, gold_outline, 25, 30, self.image)

        pygame.draw.circle(self.image, gold_outline, (300, 100), 30, 30)
        pygame.draw.circle(self.image, winnerColor2, (300, 100), 25, 25)

        if self.winner == 2:
            text = "It's a Draw!"
        else:
            text = self.winner_name + " Wins!"

        font = pygame.font.Font(None, 60)
        t = font.render(text, True, gold_color)
        text_rect = t.get_rect(center=(300, 35))
        self.image.blit(t, text_rect)



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
        self.user_info = None

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
                         self.client, self.user_info)
        if self.screen_rect.size != SCREEN_START_SIZE:
            fit_to_rect = self.image_rect.fit(self.screen_rect)
            fit_to_rect.center = self.screen_rect.center
            scaled = pg.transform.smoothscale(self.image, fit_to_rect.size)
            self.scale = fit_to_rect.width / SCREEN_START_SIZE[0]
            self.screen.blit(scaled, fit_to_rect)
        else:
            self.screen.blit(self.image, (0, 0))


    def main(self):
        # Create a file if it doesn't already exist. If a corrupted file exists, replace it with a valid file.
        valid_file = False
        while valid_file == False:
            if not os.path.exists(settings_file_name):
                file = open(settings_file_name, 'x')
                # username, wins, losses, draws.
                username = usernames[random.randint(0, 88)]
                file.write(username + "\n0\n0\n0")
                file.close()
            user_info_file = open(settings_file_name, 'r')
            self.user_info = [x.rstrip() for x in user_info_file.readlines()]
            user_info_file.close()
            if len(self.user_info) == 4 and self.user_info[1].isdigit() and self.user_info[2].isdigit() and self.user_info[3].isdigit():
                valid_file = True
            else:
                os.remove(settings_file_name)

        while not self.done:
            if self.client and self.client.error:
                self.client = None
                self.page.message = "There was a problem connecting to the server."
            if self.client and self.client.has_current_game and not isinstance(self.page, GamePage):
                self.set_page(GamePage(False, networked_game=True))
            self.screen_event()
            self.screen_update()
            pg.display.update()
            self.clock.tick(self.fps)

    def set_page(self, page, message = ""):
        if isinstance(page, WinPage) and self.client and self.client.has_current_game:
            self.client.clear_game_info()
        if isinstance(self.page, GamePage) and self.client and self.client.has_current_game:
            self.client.resign_game()
            self.client.has_current_game = False
        self.page = page
        if message:
            self.page.message = message

    def set_client(self, client):
        self.client = client

    def set_done(self, done):
        self.done = done


if __name__ == "__main__":
    random.seed(datetime.now())
    run_it = ScreenControl()
    run_it.main()
    pg.quit()
    sys.exit()
