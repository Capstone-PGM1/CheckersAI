import copy
import sys
from random import randint


class Piece(object):
    def __init__(self, color, king=False):
        self.color = color
        self.king = king


class Move(object):
    def __init__(self, from_row, from_column, to_row, to_column):
        self.fromRow = from_row
        self.fromColumn = from_column
        self.toRow = to_row
        self.toColumn = to_column


class LegalMove(object):
    def __init__(self, row, column, pieces, moves):
        self.endRow = row
        self.endColumn = column
        self.piecesNumber = pieces  # number of cells taken on this move
        self.moves = moves

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


class Cell(object):
    possibleMoves: [LegalMove]

    def __init__(self, color, king=False):
        self.piece = Piece(color, king)  # piece is 0 for red, 1 for black, 2 for empty
        self.possibleMoves = []


class GameState(object):
    activePlayer: int
    board: [[Cell]]

    def __init__(self, board=[], empty_moves=0, active_player=0):
        self.board = board
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

    def do_to_all_active_cells(self, method_to_apply):
        for row in range(8):
            for column in range(8):
                if self.board[row][column].piece.color == self.activePlayer:
                    method_to_apply(self.board[row][column])

    def can_jump_left(self, row, column):
        if column - 2 >= 0 and row + 2 < 8 and self.board[row + 2][column - 2].piece.color == 2:
            if (self.board[row][column].piece.color == 0 and
                self.board[row + 1][column - 1].piece.color == 1) or \
                    (self.board[row][column].piece.color == 1 and self.board[row][column].piece.king and
                     self.board[row + 1][column - 1].piece.color == 0):
                return True
        return False

    def can_jump_right(self, row, column):
        if column + 2 < 8 and row + 2 < 8 and self.board[row + 2][column + 2].piece.color == 2:
            if (self.board[row][column].piece.color == 0 and
                self.board[row + 1][column + 1].piece.color == 1) or \
                    (self.board[row][column].piece.color == 1 and self.board[row][column].piece.king and
                     self.board[row + 1][column + 1].piece.color == 0):
                return True
        return False

    def can_jump_back_left(self, row, column):
        if column - 2 >= 0 and row - 2 >= 0 and self.board[row - 2][column - 2].piece.color == 2:
            if (self.board[row][column].piece.color == 0 and self.board[row][column].piece.king and
                self.board[row - 1][column - 1].piece.color == 1) or \
                    (self.board[row][column].piece.color == 1 and
                     self.board[row - 1][column - 1].piece.color == 0):
                return True
        return False

    def can_jump_back_right(self, row, column):
        if column + 2 < 8 and row - 2 >= 0 and self.board[row - 2][column + 2].piece.color == 2:
            if (self.board[row][column].piece.color == 0 and self.board[row][column].piece.king and
                self.board[row - 1][column - 1].piece.color == 1) or \
                    (self.board[row][column].piece.color == 1 and
                     self.board[row - 1][column + 1].piece.color == 0):
                return True
        return False

    def can_move_left(self, row, column):
        column_left = column - 1
        row_left = row + 1
        if column_left >= 0 and row_left < 8 and self.board[row_left][column_left].piece.color == 2:
            if self.board[row][column].piece.color == 0 or self.board[row][column].piece.king:
                return True
        return False

    def can_move_right(self, row, column):
        column_right = column + 1
        row_right = row + 1
        if column_right < 8 and row_right < 8 and self.board[row_right][column_right].piece.color == 2:
            if self.board[row][column].piece.color == 0 or self.board[row][column].piece.king:
                return True
        return False

    def can_move_back_left(self, row, column):
        column_left = column - 1
        row_left = row - 1
        if column_left >= 0 and row_left >= 0 and self.board[row_left][column_left].piece.color == 2:
            if self.board[row][column].piece.color == 1 or self.board[row][column].piece.king:
                return True
        return False

    def can_move_back_right(self, row, column):
        column_right = column + 1
        row_right = row - 1
        if column_right < 8 and row_right >= 0 and self.board[row_right][column_right].piece.color == 2:
            if self.board[row][column].piece.color == 1 or self.board[row][column].piece.king:
                return True
        return False

    def calculate_simple_moves(self, c_row, c_column, path):
        if self.can_move_left(c_row, c_column):
            path.append(LegalMove(c_row + 1, c_column - 1, 0, [Move(c_row, c_column, c_row + 1, c_column - 1)]))
        if self.can_move_right(c_row, c_column):
            path.append(LegalMove(c_row + 1, c_column + 1, 0, [Move(c_row, c_column, c_row + 1, c_column + 1)]))
        if self.can_move_back_left(c_row, c_column):
            path.append(LegalMove(c_row - 1, c_column - 1, 0, [Move(c_row, c_column, c_row - 1, c_column - 1)]))
        if self.can_move_back_right(c_row, c_column):
            path.append(LegalMove(c_row - 1, c_column + 1, 0, [Move(c_row, c_column, c_row - 1, c_column + 1)]))

    def is_king_condition(self, c_row, c_column, e_row):
        return not self.board[c_row][c_column].piece.king and \
               ((self.board[c_row][c_column].piece.color == 0 and e_row == 7) or
                (self.board[c_row][c_column].piece.color == 1 and e_row == 0))

    def calculate_legal_jumps(self, c_row, c_column, piece_number, c_path, all_paths):
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

    def calculate_legal_moves(self, row, column):
        path = []
        self.calculate_legal_jumps(row, column, 0, [], path)
        if len(path) == 0:
            is_jump = False
            self.calculate_simple_moves(row, column, path)
        else:
            is_jump = True
        return path, is_jump

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

    def update_game_state_with_move(self, legal_move):
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

    def is_win(self):
        for row in self.board:
            for cell in row:
                if cell.piece.color == self.activePlayer:
                    if len(cell.possibleMoves) > 0:
                        return False
        return True

    def is_draw(self):
        return self.emptyMoves >= 40

    def is_game_over(self):
        self.is_draw() or self.is_win()

    def get_state_value(self, maximizing_player):
        if self.is_game_over():
            if self.is_win():
                if maximizing_player:
                    return -sys.maxsize - 1
                else:
                    return sys.maxsize
            else:
                return sys.maxsize - 100  # draw is good, but not as good as a win
        else:
            value = 0
            for row in range(8):
                for column in range(8):
                    piece = self.board[row][column].piece
                    if piece.color == self.activePlayer:
                        value = value + 10
                        if piece.king:
                            value = value + 5
                        else:
                            if self.activePlayer == 0:
                                dist_to_king = 7 - row
                            else:
                                dist_to_king = row
                            if dist_to_king < 4:
                                value = value + 4 - dist_to_king
                        if self.board[row][column].possibleMoves == 0:
                            value = value - 8
            return value

    def get_ai_move(self):
        max_val = -sys.maxsize - 1
        moves = []
        for row in range(8):
            for column in range(8):
                if self.board[row][column].piece.color == self.activePlayer:
                    for move in self.board[row][column].possibleMoves:
                        state_copy = copy.deepcopy(self)
                        state_copy.update_game_state_with_move(move)
                        cur_val = state_copy.minimax(2, True)
                        if max_val < cur_val:
                            max_val = cur_val
                            moves.clear()
                        if not max_val > cur_val:
                            moves.append(move)
        if len(moves) > 0:
            if len(moves) == 1:
                m = moves[0]
            else:
                m = moves[randint(0, len(moves) - 1)]
            print("Moving to row " + str(m.endRow) + " column " + str(m.endColumn) + " from row " +
                  str(m.moves[0].fromRow) + " column " + str(m.moves[0].fromColumn))
            return m

    # based on pseudo-code from https://en.wikipedia.org/wiki/Minimax
    def minimax(self, depth, maximizing_player):
        if depth == 0 or self.is_game_over():
            return self.get_state_value(maximizing_player)
        children_found = False
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
                            val = max(val, state_copy.minimax(depth - 1, False))
                            children_found = True
            if children_found:
                return val
            else:
                return self.get_state_value(maximizing_player)
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
                            val = min(val, state_copy.minimax(depth - 1, True))
                            children_found = True
            if children_found:
                return val
            else:
                return self.get_state_value(maximizing_player)
