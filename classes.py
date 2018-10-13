class Piece(object):
    def __init__(self, color, king=False):
        self.color = color
        self.king = king


class Cell(object):
    def __init__(self, color, king=False):
        self.piece = Piece(color, king)  # piece is 0 for red, 1 for black, 2 for empty
        self.possibleMoves = []


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


class GameState(object):
    activePlayer: int

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
