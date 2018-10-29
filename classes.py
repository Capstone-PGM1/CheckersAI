import copy
import sys


# lives in each Cell on the board
class Piece(object):
    def __init__(self, color, king=False):
        self.color = color  # 0 is red, 1 is white, 2 is Empty
        self.king = king


# a one move from Cell to Cell, part of LegalMove
class Move(object):
    def __init__(self, from_row, from_column, to_row, to_column):
        self.fromRow = from_row
        self.fromColumn = from_column
        self.toRow = to_row
        self.toColumn = to_column


# can be jump can be simple move
class LegalMove(object):
    def __init__(self, row, column, pieces, moves):
        self.endRow = row
        self.endColumn = column
        self.piecesNumber = pieces  # number of cells taken on this move
        self.moves = moves  # a list of Move from start cell to end cell, there are several Move for a jumping path \
        #  or only one Move for simple piece move

    # checks if there is already a LegalMove in the list with the same end Cell. If not - simply appends new
    # LegalMove to the list. If there is one, if the new LegalMove has more pieces taken - replace the one in the
    # list with new LegalMove, else - does nothing.
    # modifies the actual list, doesn't return anything
    def append_legal_jump(self, moves):
        found = False
        for m in moves:
            if m.endRow == self.endRow and m.endColumn == self.endColumn:
                if self.piecesNumber > m.piecesNumber:
                    moves.remove(m)
                    moves.append(self)
                found = True
                break
        if not found:
            moves.append(self)


# Occupies [row][column] in the board. Always has a piece (color=2 for empty Cell)
class Cell(object):
    possibleMoves: [LegalMove]  # a list of Possible moves for the piece in the Cell. Always empty for inactive player

    def __init__(self, color, king=False):
        self.piece = Piece(color, king)  # piece is 0 for red, 1 for black, 2 for empty
        self.possibleMoves = []

    def send_possible_moves_for_network(self):
        return [{"endRow": x.endRow, "endColumn": x.endColumn, "piecesNumber": x.piecesNumber,
                 "moves": {(y.fromRow, y.fromColumn): (y.toRow, y.toColumn) for y in x.moves}} for x in
                self.possibleMoves]


# th main class - has board with Cells, active player's number & counter for empty moves
class GameState(object):
    activePlayer: int  # 0 - red, 1 - black
    board: [[Cell]]  # only activePlayer can have possibleMoves non-empty. Inactive player's list is always cleared
    emptyMoves: int

    def __repr__(self):
        string = "  "
        for i in range(8):
            string += str(i) + " "
        string += "\n"
        for row in range(8):
            string += str(row) + " "
            for column in range(8):
                if self.board[row][column].piece.color == 2:
                    if row % 2 == column % 2:
                        string += "_ "
                    else:
                        string += ". "
                elif self.board[row][column].piece.color == 0:
                    if self.board[row][column].piece.king:
                        string += "R "
                    else:
                        string += "r "
                else:
                    if self.board[row][column].piece.king:
                        string += "B "
                    else:
                        string += "b "
            string += "\n"

        return string

    def send_possible_moves_for_network(self):
        dct = dict()
        for row in range(8):
            for column in range(8):
                possibleMoves = self.board[row][column].send_possible_moves_for_network()
                if possibleMoves:
                    dct[(row, column)] = possibleMoves
        return dct

    def get_board_for_network(self):
        dct = dict()
        for row in range(8):
            for column in range(8):
                if self.board[row][column].piece.color == 2:
                    if row % 2 == column % 2:
                        # string += "x "
                        dct[(row, column)] = "_"
                    else:
                        dct[(row, column)] = "."
                elif self.board[row][column].piece.color == 0:
                    if self.board[row][column].piece.king:
                        dct[(row, column)] = "R"
                    else:
                        dct[(row, column)] = "r"
                else:
                    if self.board[row][column].piece.king:
                        dct[(row, column)] = "B"
                    else:
                        dct[(row, column)] = "b"
        return dct

    # Initializing to empty array doesn't work well in Python: https://docs.python-guide.org/writing/gotchas/
    # The first time, it works okay. The second time, that empty array has been mutated, and it becomes something else.
    def __init__(self, board=None, empty_moves=0, active_player=0):
        self.board = board if board else []
        if len(self.board) == 0:
            for row in range(8):
                temp_row = []
                for column in range(8):
                    if row % 2 == column % 2:
                        if row < 3:
                            temp_row.append(Cell(0))
                        elif row > 4:
                            temp_row.append(Cell(1))
                        else:
                            temp_row.append(Cell(2))
                    else:
                        temp_row.append(Cell(2))
                self.board.append(temp_row)
        self.emptyMoves = empty_moves  # for 40 moves definition of draw
        self.activePlayer = active_player  # 0 is red player, 1 is black

    def switch_player(self):
        self.activePlayer = (self.activePlayer + 1) % 2

    # I'll need it later for refactor, isn't used now
    def do_to_all_active_cells(self, method_to_apply):
        for row in range(8):
            for column in range(8):
                if self.board[row][column].piece.color == self.activePlayer:
                    method_to_apply(self.board[row][column])

    # Checks if the piece in board[row][column] can jump left. Does it's own checking for color against activePlayer
    # color and king/not king condition.
    def can_jump_left(self, row, column) -> bool:
        if column - 2 >= 0 and row + 2 < 8 and self.board[row + 2][column - 2].piece.color == 2:
            if (self.board[row][column].piece.color == 0 and
                self.board[row + 1][column - 1].piece.color == 1) or \
                    (self.board[row][column].piece.color == 1 and self.board[row][column].piece.king and
                     self.board[row + 1][column - 1].piece.color == 0):
                return True
        return False

    # Checks if the piece in board[row][column] can jump right. Does it's own checking for color against activePlayer
    # color and king/not king condition.
    def can_jump_right(self, row, column) -> bool:
        if column + 2 < 8 and row + 2 < 8 and self.board[row + 2][column + 2].piece.color == 2:
            if (self.board[row][column].piece.color == 0 and
                self.board[row + 1][column + 1].piece.color == 1) or \
                    (self.board[row][column].piece.color == 1 and self.board[row][column].piece.king and
                     self.board[row + 1][column + 1].piece.color == 0):
                return True
        return False

    # Checks if the piece in board[row][column] can jump back left. Does it's own checking for color against
    #  activePlayer color and king/not king condition.
    def can_jump_back_left(self, row, column) -> bool:
        if column - 2 >= 0 and row - 2 >= 0 and self.board[row - 2][column - 2].piece.color == 2:
            if (self.board[row][column].piece.color == 0 and self.board[row][column].piece.king and
                self.board[row - 1][column - 1].piece.color == 1) or \
                    (self.board[row][column].piece.color == 1 and
                     self.board[row - 1][column - 1].piece.color == 0):
                return True
        return False

    # Checks if the piece in board[row][column] can jump back right. Does it's own checking for color against
    # activePlayer color and king/not king condition.
    def can_jump_back_right(self, row, column) -> bool:
        if column + 2 < 8 and row - 2 >= 0 and self.board[row - 2][column + 2].piece.color == 2:
            if (self.board[row][column].piece.color == 0 and self.board[row][column].piece.king and
                self.board[row - 1][column + 1].piece.color == 1) or \
                    (self.board[row][column].piece.color == 1 and
                     self.board[row - 1][column + 1].piece.color == 0):
                return True
        return False

    # Checks if the piece in board[row][column] can make a simple move left. Does it's own checking for color against
    # activePlayer color and king/not king condition.
    def can_move_left(self, row, column) -> bool:
        column_left = column - 1
        row_left = row + 1
        if column_left >= 0 and row_left < 8 and self.board[row_left][column_left].piece.color == 2:
            if self.board[row][column].piece.color == 0 or self.board[row][column].piece.king:
                return True
        return False

    # Checks if the piece in board[row][column] can make a simple move right. Does it's own checking for color against
    # activePlayer color and king/not king condition.
    def can_move_right(self, row, column) -> bool:
        column_right = column + 1
        row_right = row + 1
        if column_right < 8 and row_right < 8 and self.board[row_right][column_right].piece.color == 2:
            if self.board[row][column].piece.color == 0 or self.board[row][column].piece.king:
                return True
        return False

    # Checks if the piece in board[row][column] can make a simple move left back. Does it's own checking for color
    # against activePlayer color and king/not king condition.
    def can_move_back_left(self, row, column) -> bool:
        column_left = column - 1
        row_left = row - 1
        if column_left >= 0 and row_left >= 0 and self.board[row_left][column_left].piece.color == 2:
            if self.board[row][column].piece.color == 1 or self.board[row][column].piece.king:
                return True
        return False

    # Checks if the piece in board[row][column] can make a simple move left right. Does it's own checking for color
    # against activePlayer color and king/not king condition.
    def can_move_back_right(self, row, column) -> bool:
        column_right = column + 1
        row_right = row - 1
        if column_right < 8 and row_right >= 0 and self.board[row_right][column_right].piece.color == 2:
            if self.board[row][column].piece.color == 1 or self.board[row][column].piece.king:
                return True
        return False

    # Calculates all possible simple moves (not jumps) for a piece. Appends it to path, doesn't return anything
    def calculate_simple_moves(self, c_row: int, c_column: int, path: [LegalMove]):
        if self.can_move_left(c_row, c_column):
            path.append(LegalMove(c_row + 1, c_column - 1, 0, [Move(c_row, c_column, c_row + 1, c_column - 1)]))
        if self.can_move_right(c_row, c_column):
            path.append(LegalMove(c_row + 1, c_column + 1, 0, [Move(c_row, c_column, c_row + 1, c_column + 1)]))
        if self.can_move_back_left(c_row, c_column):
            path.append(LegalMove(c_row - 1, c_column - 1, 0, [Move(c_row, c_column, c_row - 1, c_column - 1)]))
        if self.can_move_back_right(c_row, c_column):
            path.append(LegalMove(c_row - 1, c_column + 1, 0, [Move(c_row, c_column, c_row - 1, c_column + 1)]))

    # a condition to end jump sequence - checks if non-king piece reached king-row
    def is_king_condition(self, c_row, c_column, e_row) -> bool:
        return not self.board[c_row][c_column].piece.king and \
               ((self.board[c_row][c_column].piece.color == 0 and e_row == 7) or
                (self.board[c_row][c_column].piece.color == 1 and e_row == 0))

    # calculates all legal jumps for the piece and appends it to all_paths. Recursive. c_path is a collector for Move
    # for current LegalMove being built
    def calculate_legal_jumps(self, c_row, c_column, piece_number, c_path: [Move], all_paths: [LegalMove]):
        def recursive(e_row, e_column):
            move = [Move(c_row, c_column, e_row, e_column)]
            if self.is_king_condition(c_row, c_column, e_row):
                new_m = LegalMove(e_row, e_column, piece_number, c_path + move)
                new_m.append_legal_jump(all_paths)
                return
            new_state = copy.deepcopy(self)
            new_state.update_game_state_with_move(LegalMove(e_row, e_column, 1, move))
            new_state.calculate_legal_jumps(e_row, e_column, piece_number + 1, c_path + move, all_paths)

        not_returning = True
        if self.can_jump_left(c_row, c_column):
            recursive(c_row + 2, c_column - 2)
            not_returning = False
        if self.can_jump_right(c_row, c_column):
            recursive(c_row + 2, c_column + 2)
            not_returning = False
        if self.can_jump_back_left(c_row, c_column):
            recursive(c_row - 2, c_column - 2)
            not_returning = False
        if self.can_jump_back_right(c_row, c_column):
            recursive(c_row - 2, c_column + 2)
            not_returning = False
        if not_returning and len(c_path) > 0:
            new_move = LegalMove(c_row, c_column, piece_number, c_path)
            new_move.append_legal_jump(all_paths)

    # calculates all legal moves for the piece at board[row][column]
    # first look for jumps, if non available - looks for simple moves
    def calculate_legal_moves(self, row, column) -> [[LegalMove], bool]:
        path = []
        self.calculate_legal_jumps(row, column, 0, [], path)
        if len(path) == 0:
            is_jump = False
            self.calculate_simple_moves(row, column, path)
        else:
            is_jump = True
        return path, is_jump

    # gets all legal moves for all Cells for an activePlayer
    # clears possibleMoves list for inactive player
    def get_all_legal_moves(self):
        have_jumps = False
        for row in range(8):
            for column in range(8):
                if self.board[row][column].piece.color == self.activePlayer:
                    self.board[row][column].possibleMoves, is_jump = self.calculate_legal_moves(row, column)
                    have_jumps = have_jumps or is_jump
                else:
                    self.board[row][column].possibleMoves.clear()
        if have_jumps:
            for row in range(8):  # that is a lazy way. better find a way not to go through all board - eventually
                for column in range(8):
                    if self.board[row][column].piece.color == self.activePlayer:
                        if len(self.board[row][column].possibleMoves) > 0:
                            the_move = self.board[row][column].possibleMoves[0]
                            if abs(the_move.moves[0].fromRow - the_move.moves[0].toRow) != 2:
                                self.board[row][column].possibleMoves.clear()

    # updates the GameState with LegalMove - "moves" the pieces, removes "taken" pieces
    def update_game_state_with_move(self, legal_move: LegalMove):
        if len(legal_move.moves) > 0:
            start_row = legal_move.moves[0].fromRow
            start_column = legal_move.moves[0].fromColumn
            self.board[legal_move.endRow][legal_move.endColumn].piece = copy.deepcopy(
                self.board[start_row][start_column].piece)
            if self.is_king_condition(start_row, start_column, legal_move.endRow):
                self.board[legal_move.endRow][legal_move.endColumn].piece.king = True
            self.board[start_row][start_column].piece.color = 2
            if abs(start_row - legal_move.moves[0].toRow) == 2:
                self.emptyMoves = 0
                for move in legal_move.moves:
                    self.board[(move.fromRow + move.toRow) // 2][
                        (move.fromColumn + move.toColumn) // 2].piece.color = 2
            elif not self.board[start_row][start_column].piece.king:
                self.emptyMoves = 0
            else:
                self.emptyMoves = self.emptyMoves + 1
        else:
            print("BIG ERROR: legal_move doesn't have any moves in it")

    # checks if the game is over with win condition
    # returns color of the winner or 2 - if game is not over
    def is_win(self) -> int:
        possible_moves = 0
        for row in range(8):
            for column in range(8):
                if self.board[row][column].piece.color == self.activePlayer:
                    if len(self.board[row][column].possibleMoves) != 0:
                        possible_moves = possible_moves + 1
        if possible_moves == 0:
            return (self.activePlayer + 1) % 2
        else:
            for row in self.board:
                for cell in row:
                    if cell.piece.color == (self.activePlayer + 1) % 2:
                        return 2
        return self.activePlayer

    # checks if game is over with a draw
    def is_draw(self) -> bool:
        return self.emptyMoves >= 40

    # checks if the game is over
    def is_game_over(self) -> bool:
        return self.is_draw() or self.is_win() != 2

    # evaluation function for minimax - NEEDS MORE THOUGHTS ON IT
    def get_state_value(self, maximizing_player) -> int:
        if maximizing_player:
            max_player_number = self.activePlayer
        else:
            max_player_number = (self.activePlayer + 1) % 2
        if self.is_game_over():
            if self.is_draw():
                return 1000  # draw is good, but not as good as a win
            else:
                winner = self.is_win()
                if winner == max_player_number:
                    return sys.maxsize
                else:
                    return -sys.maxsize - 1
        else:
            if not maximizing_player:
                self.switch_player()
                self.get_all_legal_moves()
            max_player_kings = 0
            min_player_kings = 0
            max_player_pawns = 0
            min_player_pawns = 0
            max_player_corners = 0
            min_player_corners = 0
            max_player_first_row = 0
            min_player_first_row = 0
            max_player_blocked = 0
            min_player_blocked = 0

            if self.activePlayer == 0:
                max_first_row = 0
                min_first_row = 7
            else:
                max_first_row = 7
                min_first_row = 0

            # calculate all the pieces number
            for row in range(8):
                for column in range(8):
                    if self.board[row][column].piece.color == self.activePlayer:
                        if self.board[row][column].piece.king:
                            max_player_kings = max_player_kings + 1
                        else:
                            max_player_pawns = max_player_pawns + 1
                        if len(self.board[row][column].possibleMoves) == 0:
                            path = []
                            self.calculate_simple_moves(row, column, path)
                            if len(path) == 0:
                                max_player_blocked = max_player_blocked + 1
                        if column == 0 or column == 7:
                            max_player_corners = max_player_corners + 1
                        if row == max_first_row:
                            max_player_first_row = max_player_first_row + 1
                    elif self.board[row][column].piece.color != 2:
                        if self.board[row][column].piece.king:
                            min_player_kings = min_player_kings + 1
                        else:
                            min_player_pawns = min_player_pawns + 1
                        if row == min_first_row:
                            min_player_first_row  = min_player_first_row + 1
                        if column == 0 or column == 7:
                            min_player_corners = min_player_corners + 1
                        path = []
                        self.calculate_legal_jumps(row, column, 0, [], path)
                        if len(path) == 0:
                            self.calculate_simple_moves(row, column, path)
                            if len(path) == 0:
                                min_player_blocked = min_player_blocked + 1

            payoff = 50 + 10 * (max_player_kings + max_player_pawns - min_player_pawns -
                                min_player_kings)
            control = 0.087 * (max_player_kings - min_player_kings) + 0.042 * (max_player_pawns - min_player_pawns) + \
                0.03 * (max_player_corners - min_player_corners + max_player_first_row - min_player_first_row) - \
                0.03*(max_player_blocked - min_player_blocked)
            terminal = 0.083
            return terminal * payoff + (1 - terminal) * ((50 + 50 * control) * 0.659 + 0.341 * payoff)

    # get ai move for 1-player game. Currently calling for minimax algo to find out best move
    # if several moves has same value, use random number to select one of those
    def get_ai_move(self) -> LegalMove:
        cur_val, move = self.minimax_alphabeta(5, -sys.maxsize - 1, sys.maxsize, False)
        print("Moving to row " + str(move.endRow) + " column " + str(move.endColumn) + " from row " +
              str(move.moves[0].fromRow) + " column " + str(move.moves[0].fromColumn))
        return move

    # calculate value of state using minimax (no alpha-beta pruning yet - need to make sure it works as it is first)
    # based on pseudo-code from https://en.wikipedia.org/wiki/Minimax
    def minimax_alphabeta(self, depth, alpha, beta, maximizing_player) -> [int, LegalMove]:
        if depth == 0 or self.is_game_over():  # game over == terminal node
            return self.get_state_value(maximizing_player), LegalMove(0, 0, 0, [])
        move_to_return = LegalMove(0, 0, 0, [])
        if maximizing_player:
            val = -sys.maxsize - 1
            for row in range(8):
                for column in range(8):
                    if self.board[row][column].piece.color == self.activePlayer:
                        for move in self.board[row][column].possibleMoves:
                            state_copy = copy.deepcopy(self)
                            state_copy.update_game_state_with_move(move)
                            state_copy.switch_player()
                            state_copy.get_all_legal_moves()
                            new_val, m = state_copy.minimax_alphabeta(depth - 1, alpha, beta, False)
                            if new_val > val:
                                val = new_val
                                move_to_return = move
                            if beta <= val:
                                return new_val, move
                            if alpha < val:
                                alpha = val
                                move_to_return = move
            return val, move_to_return
        else:  # (*minimizing player *)
            val = sys.maxsize
            for row in range(8):
                for column in range(8):
                    if self.board[row][column].piece.color == self.activePlayer:
                        for move in self.board[row][column].possibleMoves:
                            state_copy = copy.deepcopy(self)
                            state_copy.update_game_state_with_move(move)
                            state_copy.switch_player()
                            state_copy.get_all_legal_moves()
                            new_val, m = state_copy.minimax_alphabeta(depth - 1, alpha, val, True)
                            if new_val < val:
                                val = new_val
                                move_to_return = move
                            if val <= alpha:
                                return val, move_to_return
                            if val < beta:
                                beta = val
                                move_to_return = move
            return val, move_to_return
