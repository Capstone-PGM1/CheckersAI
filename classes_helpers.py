RED = 0
BLACK = 1
EMPTY = 2


def piece_to_letter(color: int, king: bool):
    if color == RED:
        letter = 'r'
    elif color == BLACK:
        letter = 'b'
    else:
        letter = 'x'  # just to return something. there should be error checking somewhere else
    if king:
        return letter.upper()
    else:
        return letter


def other_player(this_player):
    return (this_player + 1) % 2


# returns possible moves for the piece at the row and column
def piece_possible_moves(row, column, moves):
    return list(filter(lambda m: m.moves[0].fromRow == row and m.moves[0].fromColumn == column, moves))


def send_possible_moves_for_network(possible_moves):
    return [{"endRow": x.endRow, "endColumn": x.endColumn, "piecesNumber": x.piecesNumber,
             "moves": {(y.fromRow, y.fromColumn): (y.toRow, y.toColumn) for y in x.moves}} for x in possible_moves]


def qstate_to_string(state):
    return "".join(str(s) for s in state)


def new_qstate():
    return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
