import copy
import sys
from classes_helpers import *
from numpy import random


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


# th main class - has board with Cells, active player's number & counter for empty moves
class GameState(object):
    activePlayer: int
    emptyMoves: int
    board: [[str]]

    def __repr__(self):
        string = "  "
        for i in range(8):
            string += str(i) + " "
        string += "\n"
        for row in range(8):
            string += str(row) + " "
            for column in range(8):
                if self.board[row][column] == 'x':
                    if row % 2 == column % 2:
                        string += "_ "
                    else:
                        string += ". "
                else:
                    string += self.board[row][column]
            string += "\n"
        return string

    def send_possible_moves_for_network(self, color = 0):
        dct = dict()
        possible_moves = self.get_all_legal_moves()
        for row in range(8):
            for column in range(8):
                moves = piece_possible_moves(row, column, possible_moves)
                if len(moves) > 0:
                    dct[(row if color else 7 - row, column if color else 7 - column)] = [{"endRow": x.endRow if color else 7 - x.endRow, "endColumn": x.endColumn if color else 7 - x.endColumn, "piecesNumber": x.piecesNumber,
                                           "moves": {(y.fromRow if color else 7 - y.fromRow, y.fromColumn if color else 7 - y.fromColumn): (y.toRow if color else 7 - y.toRow, y.toColumn if color else 7 - y.toColumn) for y in x.moves}} for x in moves]
        return dct

    def get_board_for_network(self, color = 0):
        dct = dict()
        for row in range(8):
            for column in range(8):
                row_index = row if color else 7 - row
                column_index = column if color else 7 - column
                if self.board[row][column] == 'x':
                    if row % 2 == column % 2:
                        dct[(row_index, column_index)] = "_"
                    else:
                        dct[(row_index, column_index)] = "."
                else:
                    dct[(row_index, column_index)] = self.board[row][column]
        return dct

    # Initializing to empty array doesn't work well in Python: https://docs.python-guide.org/writing/gotchas/
    # The first time, it works okay. The second time, that empty array has been mutated, and it becomes something else.
    def __init__(self, board=None, empty_moves=0, active_player=RED):
        self.board = board if board else []
        if len(self.board) == 0:
            for row in range(8):
                temp_row = []
                for column in range(8):
                    if row % 2 != column % 2:
                        if row < 3:
                            temp_row.append('r')
                        elif row > 4:
                            temp_row.append('b')
                        else:
                            temp_row.append('x')
                    else:
                        temp_row.append('x')
                self.board.append(temp_row)
        self.emptyMoves = empty_moves  # for 40 moves definition of draw
        self.activePlayer = active_player  # 0 is red player, 1 is black

    def switch_player(self):
        self.activePlayer = other_player(self.activePlayer)

    # Checks if the piece in board[row][column] can jump left. Does it's own checking for color against activePlayer
    # color and king/not king condition.
    def can_jump_left(self, row, column) -> bool:
        if column - 2 >= 0 and row + 2 < 8 and self.board[row + 2][column - 2] == 'x':
            if (self.board[row][column].upper() == 'R' and
                self.board[row + 1][column - 1].upper() == 'B') or \
                    (self.board[row][column] == 'B' and self.board[row + 1][column - 1].upper() == 'R'):
                return True
        return False

    # Checks if the piece in board[row][column] can jump right. Does it's own checking for color against activePlayer
    # color and king/not king condition.
    def can_jump_right(self, row, column) -> bool:
        if column + 2 < 8 and row + 2 < 8 and self.board[row + 2][column + 2] == 'x':
            if (self.board[row][column].upper() == 'R' and
                self.board[row + 1][column + 1].upper() == 'B') or \
                    (self.board[row][column] == 'B' and self.board[row + 1][column + 1].upper() == 'R'):
                return True
        return False

    # Checks if the piece in board[row][column] can jump back left. Does it's own checking for color against
    #  activePlayer color and king/not king condition.
    def can_jump_back_left(self, row, column) -> bool:
        if column - 2 >= 0 and row - 2 >= 0 and self.board[row - 2][column - 2] == 'x':
            if (self.board[row][column] == 'R' and self.board[row - 1][column - 1].upper() == 'B') or \
                    (self.board[row][column].upper() == "B" and
                     self.board[row - 1][column - 1].upper() == "R"):
                return True
        return False

    # Checks if the piece in board[row][column] can jump back right. Does it's own checking for color against
    # activePlayer color and king/not king condition.
    def can_jump_back_right(self, row, column) -> bool:
        if column + 2 < 8 and row - 2 >= 0 and self.board[row - 2][column + 2] == 'x':
            if (self.board[row][column] == 'R' and self.board[row - 1][column + 1].upper() == 'B') or \
                    (self.board[row][column].upper() == 'B' and
                     self.board[row - 1][column + 1].upper() == 'R'):
                return True
        return False

    # Checks if the piece in board[row][column] can make a simple move left. Does it's own checking for color against
    # activePlayer color and king/not king condition.
    def can_move_left(self, row, column) -> bool:
        column_left = column - 1
        row_left = row + 1
        if column_left >= 0 and row_left < 8 and self.board[row_left][column_left] == 'x':
            if self.board[row][column].upper() == 'R' or self.board[row][column] == 'B':
                return True
        return False

    # Checks if the piece in board[row][column] can make a simple move right. Does it's own checking for color against
    # activePlayer color and king/not king condition.
    def can_move_right(self, row, column) -> bool:
        column_right = column + 1
        row_right = row + 1
        if column_right < 8 and row_right < 8 and self.board[row_right][column_right] == 'x':
            if self.board[row][column].upper() == 'R' or self.board[row][column] == 'B':
                return True
        return False

    # Checks if the piece in board[row][column] can make a simple move left back. Does it's own checking for color
    # against activePlayer color and king/not king condition.
    def can_move_back_left(self, row, column) -> bool:
        column_left = column - 1
        row_left = row - 1
        if column_left >= 0 and row_left >= 0 and self.board[row_left][column_left] == 'x':
            if self.board[row][column].upper() == 'B' or self.board[row][column] == 'R':
                return True
        return False

    # Checks if the piece in board[row][column] can make a simple move left right. Does it's own checking for color
    # against activePlayer color and king/not king condition.
    def can_move_back_right(self, row, column) -> bool:
        column_right = column + 1
        row_right = row - 1
        if column_right < 8 and row_right >= 0 and self.board[row_right][column_right] == 'x':
            if self.board[row][column].upper() == 'B' or self.board[row][column] == 'R':
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
        return ((self.board[c_row][c_column] == 'r' and e_row == 7) or
                (self.board[c_row][c_column] == 'b' and e_row == 0))

    # calculates all legal jumps for the piece and appends it to all_paths. Recursive. c_path is a collector for Move
    # for current LegalMove being built
    def calculate_legal_jumps(self, c_row, c_column, piece_number, c_path: [Move], all_paths: [LegalMove]):
        def recursive(e_row, e_column):
            move = [Move(c_row, c_column, e_row, e_column)]
            if self.is_king_condition(c_row, c_column, e_row):
                new_m = LegalMove(e_row, e_column, piece_number + 1, c_path + move)
                new_m.append_legal_jump(all_paths)
                return
            new_state = GameState(copy.deepcopy(self.board), self.emptyMoves, self.activePlayer)
            new_state.update_game_state_with_move_helper(LegalMove(e_row, e_column, 1, move))
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
        all_moves = []
        for row in range(8):
            for column in range(8):
                if self.board[row][column].upper() == piece_to_letter(self.activePlayer, True):
                    new_moves, is_jump = self.calculate_legal_moves(row, column)
                    all_moves = all_moves + new_moves
                    have_jumps = have_jumps or is_jump
        if have_jumps:
            return list(filter(lambda m: m.piecesNumber > 0, all_moves))
        else:
            return all_moves

    # updates the GameState with LegalMove - "moves" the pieces, removes "taken" pieces
    def update_game_state_with_move_helper(self, legal_move: LegalMove):
        if len(legal_move.moves) > 0:
            start_row = legal_move.moves[0].fromRow
            start_column = legal_move.moves[0].fromColumn
            moving_piece = self.board[start_row][start_column]
            self.board[legal_move.endRow][legal_move.endColumn] = moving_piece.upper() if\
                self.is_king_condition(start_row, start_column, legal_move.endRow) else moving_piece
            if abs(start_row - legal_move.moves[0].toRow) == 2:
                self.emptyMoves = 0
                for move in legal_move.moves:
                    self.board[(move.fromRow + move.toRow) // 2][
                        (move.fromColumn + move.toColumn) // 2] = 'x'
            elif self.board[start_row][start_column] != 'R' and self.board[start_row][start_column] != "B":
                self.emptyMoves = 0
            else:
                self.emptyMoves = self.emptyMoves + 1
            self.board[start_row][start_column] = 'x'
        else:
            print("BIG ERROR: legal_move doesn't have any moves in it")

    # Ignores invalid moves. If move is valid, the game is updated, and the board is ready for the next player.
    def update_game_state_with_move(self, start_row, start_column, end_row, end_column):
        moves = self.get_all_legal_moves()
        for m in moves:
            if m.endRow == end_row and m.endColumn == end_column and m.moves[0].fromRow == start_row \
                    and m.moves[0].fromColumn == start_column:
                self.update_game_state_with_move_helper(m)
        self.switch_player()

    # checks if the game is over with win condition
    # returns color of the winner or 2 - if game is not over
    def is_win(self, possible_moves) -> int:
        if len(possible_moves) == 0:
            return other_player(self.activePlayer)
        other_piece = piece_to_letter(other_player(self.activePlayer), True)
        for row in self.board:
            for cell in row:
                if cell.upper() == other_piece:
                    return 2
        return self.activePlayer

    # checks if game is over with a draw
    def is_draw(self) -> bool:
        return self.emptyMoves >= 40

    # checks if the game is over
    def is_game_over(self, possible_moves) -> (bool, int):
        winner = self.is_win(possible_moves)
        return self.is_draw() or winner != 2, winner

    # evaluation function for minimax - NEEDS MORE THOUGHTS ON IT
    def get_state_value(self, maximizing_player) -> int:
        moves = self.get_all_legal_moves()
        if maximizing_player:
            max_player_number = self.activePlayer
        else:
            max_player_number = other_player(self.activePlayer)
        game_over, winner = self.is_game_over(moves)
        if game_over:
            if self.is_draw():
                return 1000  # draw is good, but not as good as a win
            else:
                if winner == max_player_number:
                    return sys.maxsize
                else:
                    return -sys.maxsize - 1
        else:
            if not maximizing_player:
                self.switch_player()
            moves = self.get_all_legal_moves()
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

            max_first_row = 0 if self.activePlayer == RED else 7
            min_first_row = 7 if self.activePlayer == RED else 0

            # calculate all the pieces number
            for row in range(8):
                for column in range(8):
                    if self.board[row][column].upper() == piece_to_letter(self.activePlayer, True):
                        if self.board[row][column].isupper():
                            max_player_kings = max_player_kings + 1
                        else:
                            max_player_pawns = max_player_pawns + 1
                        if len(piece_possible_moves(row, column, moves)) == 0:
                            path = []
                            self.calculate_simple_moves(row, column, path)
                            if len(path) == 0:
                                max_player_blocked = max_player_blocked + 1
                        if column == 0 or column == 7:
                            max_player_corners = max_player_corners + 1
                        if row == max_first_row:
                            max_player_first_row = max_player_first_row + 1
                    elif self.board[row][column] != 'x':
                        if self.board[row][column].isupper():
                            min_player_kings = min_player_kings + 1
                        else:
                            min_player_pawns = min_player_pawns + 1
                        if row == min_first_row:
                            min_player_first_row = min_player_first_row + 1
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
    def get_ai_move(self, depth, q_table={}) -> LegalMove:
        if depth != 1:
            cur_val, move = self.minimax_alphabeta(depth, -sys.maxsize - 1, sys.maxsize, False)
        else:
            move = self.get_qlearner_move(self.activePlayer, q_table)
        # print("Moving to row " + str(move.endRow) + " column " + str(move.endColumn) + " from row " + str(move.moves[0].fromRow) + " column " + str(move.moves[0].fromColumn))
        return move

    # calculate value of state using minimax  with alpha-beta pruning
    # based on pseudo-code from https://en.wikipedia.org/wiki/Minimax
    def minimax_alphabeta(self, depth, alpha, beta, is_maximizing) -> [int, LegalMove]:
        moves = self.get_all_legal_moves()
        if depth == 0 or self.is_game_over(moves)[0]:  # game over == terminal node
            return self.get_state_value(is_maximizing), LegalMove(0, 0, 0, [])
        move_to_return = moves[0]
        if is_maximizing:
            val = -sys.maxsize - 1
            for move in moves:
                state_copy = GameState(copy.deepcopy(self.board), self.emptyMoves, self.activePlayer)
                state_copy.update_game_state_with_move_helper(move)
                state_copy.switch_player()
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
            for move in moves:
                state_copy = GameState(copy.deepcopy(self.board), self.emptyMoves, self.activePlayer)
                state_copy.update_game_state_with_move_helper(move)
                state_copy.switch_player()
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

    def get_qstate_from_board(self, q_player: int):
        state = new_qstate()
        q_first_row = 0 if q_player == RED else 7
        min_first_row = 7 if q_player == RED else 0

        for row in range(8):
            for column in range(8):
                if self.board[row][column].upper() == piece_to_letter(q_player, True):
                    if self.board[row][column].isupper():
                        state[0] = state[0] + 1
                    else:
                        state[2] = state[2] + 11
                    path = []
                    self.calculate_legal_jumps(row, column, 0, [], path)
                    if len(path) == 0:
                        self.calculate_simple_moves(row, column, path)
                        if len(path) == 0:
                            state[8] = state[8] + 1
                    if column == 0 or column == 7:
                        state[4] = state[4] + 1
                    if row == q_first_row:
                        state[10] = state[10] + 1
                elif self.board[row][column] != 'x':
                    if self.board[row][column].isupper():
                        state[1] = state[1] + 1
                    else:
                        state[2] = state[2] + 1
                    if row == min_first_row:
                        state[11] = state[11] + 1
                    if column == 0 or column == 7:
                        state[5] = state[5] + 1
                    path = []
                    self.calculate_legal_jumps(row, column, 0, [], path)
                    if len(path) == 0:
                        self.calculate_simple_moves(row, column, path)
                        if len(path) == 0:
                            state[9] = state[9] + 1
        return qstate_to_string(state)

    def get_qlearner_move(self, q_player: int, q_table: dict):
        moves = self.get_all_legal_moves()
        from_state = self.get_qstate_from_board(q_player)
        if len(moves) == 1:
            move = moves[0]  # sometimes there is just 1 jump available
        else:
            state_val = q_table.get(from_state)
            if state_val is None:
                print("New State")
                move = random.choice(moves)
            else:
                max_q_val = -sys.maxsize - 1
                move = moves[0]
                for m in moves:
                    copy_game = GameState(copy.deepcopy(self.board), self.emptyMoves, self.activePlayer)
                    copy_game.update_game_state_with_move_helper(m)
                    to_state = copy_game.get_qstate_from_board(q_player)
                    trans_val = state_val.get(to_state, 0)
                    if trans_val > max_q_val:
                        max_q_val = trans_val
                        move = m
                    elif trans_val == max_q_val:
                        move = random.choice([move, m])
        return move
