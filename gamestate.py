from classes import *
import copy


def can_jump_left(state, row, column):
    if column - 2 >= 0 and row + 2 < 8 and state.board[row + 2][column - 2].piece.color == 2:
        if (state.board[row][column].piece.color == 0 and
            state.board[row + 1][column - 1].piece.color == 1) or \
                (state.board[row][column].piece.color == 1 and state.board[row][column].piece.king and
                 state.board[row + 1][column - 1].piece.color == 0):
            return True
    return False


def can_jump_right(state, row, column):
    if column + 2 < 8 and row + 2 < 8 and state.board[row + 2][column + 2].piece.color == 2:
        if (state.board[row][column].piece.color == 0 and
            state.board[row + 1][column + 1].piece.color == 1) or \
                (state.board[row][column].piece.color == 1 and state.board[row][column].piece.king and
                 state.board[row + 1][column + 1].piece.color == 0):
            return True
    return False


def can_jump_back_left(state, row, column):
    if column - 2 >= 0 and row - 2 >= 0 and state.board[row - 2][column - 2].piece.color == 2:
        if (state.board[row][column].piece.color == 0 and state.board[row][column].piece.king and
            state.board[row - 1][column - 1].piece.color == 1) or \
                (state.board[row][column].piece.color == 1 and
                 state.board[row - 1][column - 1].piece.color == 0):
            return True
    return False


def can_jump_back_right(state, row, column):
    if column + 2 < 8 and row - 2 >= 0 and state.board[row - 2][column + 2].piece.color == 2:
        if (state.board[row][column].piece.color == 0 and state.board[row][column].piece.king and
            state.board[row - 1][column - 1].piece.color == 1) or \
                (state.board[row][column].piece.color == 1 and
                 state.board[row - 1][column + 1].piece.color == 0):
            return True
    return False


def can_move_left(state, row, column):
    column_left = column - 1
    row_left = row + 1
    if column_left >= 0 and row_left < 8 and state.board[row_left][column_left].piece.color == 2:
        if state.board[row][column].piece.color == 0 or state.board[row][column].piece.king:
            return True
    return False


def can_move_right(state, row, column):
    column_right = column + 1
    row_right = row + 1
    if column_right < 8 and row_right < 8 and state.board[row_right][column_right].piece.color == 2:
        if state.board[row][column].piece.color == 0 or state.board[row][column].piece.king:
            return True
    return False


def can_move_back_left(state, row, column):
    column_left = column - 1
    row_left = row - 1
    if column_left >= 0 and row_left >= 0 and state.board[row_left][column_left].piece.color == 2:
        if state.board[row][column].piece.color == 1 or state.board[row][column].piece.king:
            return True
    return False


def can_move_back_right(state, row, column):
    column_right = column + 1
    row_right = row - 1
    if column_right < 8 and row_right >= 0 and state.board[row_right][column_right].piece.color == 2:
        if state.board[row][column].piece.color == 1 or state.board[row][column].piece.king:
            return True
    return False


def calculate_simple_moves(state, c_row, c_column, path):
    if can_move_left(state, c_row, c_column):
        path.append(LegalMove(c_row + 1, c_column - 1, 0, [Move(c_row, c_column, c_row + 1, c_column - 1)]))
    if can_move_right(state, c_row, c_column):
        path.append(LegalMove(c_row + 1, c_column + 1, 0, [Move(c_row, c_column, c_row + 1, c_column + 1)]))
    if can_move_back_left(state, c_row, c_column):
        path.append(LegalMove(c_row - 1, c_column - 1, 0, [Move(c_row, c_column, c_row - 1, c_column - 1)]))
    if can_move_back_right(state, c_row, c_column):
        path.append(LegalMove(c_row - 1, c_column + 1, 0, [Move(c_row, c_column, c_row - 1, c_column + 1)]))


def append_legal_jump(moves, new_move):
    found = False
    for m in moves:
        if m.endRow == new_move.endRow and m.endColumn == new_move.endColumn:
            if new_move.piecesNumber > m.piecesNumber:
                moves.remove(m)
                moves.append(new_move)
            found = True
            break
    if not found:
        moves.append(new_move)


def is_king_condition(state, c_row, c_column, e_row):
    return not state.board[c_row][c_column].piece.king and\
                ((state.board[c_row][c_column].piece.color == 0 and e_row == 7) or
                 (state.board[c_row][c_column].piece.color == 1 and e_row == 0))


def calculate_legal_jumps(state, c_row, c_column, piece_number, c_path, all_paths):
    def recursive(e_row, e_column):
        move = [Move(c_row, c_column, e_row, e_column)]
        if is_king_condition(state, c_row, c_column, e_row):
            append_legal_jump(all_paths, LegalMove(e_row, e_column, piece_number, c_path + move))
            return
        new_state = copy.deepcopy(state)
        update_game_state_with_move(new_state, LegalMove(e_row, e_column, 1, move))
        calculate_legal_jumps(new_state, e_row, e_column, piece_number + 1, c_path + move, all_paths)
    not_returning = True
    if can_jump_left(state, c_row, c_column):
        recursive(c_row + 2, c_column - 2)
        not_returning = False
    if can_jump_right(state, c_row, c_column):
        recursive(c_row + 2, c_column + 2)
        not_returning = False
    if can_jump_back_left(state, c_row, c_column):
        recursive(c_row - 2, c_column - 2)
        not_returning = False
    if can_jump_back_right(state, c_row, c_column):
        recursive(c_row - 2, c_column + 2)
        not_returning = False
    if not_returning and len(c_path) > 0:
        append_legal_jump(all_paths, LegalMove(c_row, c_column, piece_number, c_path))


def calculate_legal_moves(state: GameState, row: int, column: int) -> [LegalMove]:
    path = []
    calculate_legal_jumps(state, row, column, 0, [], path)
    if len(path) == 0:
        is_jump = False
        calculate_simple_moves(state, row, column, path)
    else:
        is_jump = True
    return path, is_jump


def get_all_legal_moves(state):
    have_jumps = False
    for row in range(8):
        for column in range(8):
            if state.board[row][column].piece.color == state.activePlayer:
                state.board[row][column].possibleMoves, is_jump = calculate_legal_moves(state, row, column)
                have_jumps = have_jumps or is_jump
            else:
                state.board[row][column].possibleMoves.clear()
    if have_jumps:
        for row in range(8):  # that is a lazy way. better find a way not to go through all board - eventually
            for column in range(8):
                if state.board[row][column].piece.color == state.activePlayer:
                    if len(state.board[row][column].possibleMoves) > 0:
                        the_move = state.board[row][column].possibleMoves[0]
                        if abs(the_move.moves[0].fromRow - the_move.moves[0].toRow) != 2:
                            state.board[row][column].possibleMoves = []


def send_game_state_to_ui(state):
    print("", end="  ")
    for i in range(8):
        print(str(i), end=" ")
    print("")
    for row in range(8):
        print(row, end=" ")
        for column in range(8):
            if state.board[row][column].piece.color == 2:
                if row % 2 == column % 2:
                    print("x", end=" ")
                else:
                    print("o", end=" ")
            elif state.board[row][column].piece.color == 0:
                if state.board[row][column].piece.king:
                    print("K", end=" ")
                else:
                    print("R", end=" ")
            else:
                if state.board[row][column].piece.king:
                    print("Q", end=" ")
                else:
                    print("B", end=" ")
        print("")


def get_move_from_player(state):
    if state.activePlayer == 0:
        name = "Red"
    else:
        name = "Black"
    print(name + " player's turn")
    show_moves = input("Y for show possible moves, N for input your move")
    while show_moves != "N":
        row = int(input("row: "))
        column = int(input("column: "))
        for move in state.board[row][column].possibleMoves:
            print('{0} {1}taking {2}pieces'.format(str(move.endRow), str(move.endColumn),
                                                   str(move.piecesNumber)))
        show_moves = input("Y for show possible moves, N for input your move")
    print("Input the piece to move:")
    row = int(input("row: "))
    column = int(input("column: "))
    print("Where moving to?")
    row1 = int(input("row: "))
    column1 = int(input("column: "))
    for move in state.board[row][column].possibleMoves:
        if move.endRow == row1 and move.endColumn == column1:
            return move
    print("BIG ERROR, DIDN'T FIND THE LEGAL MOVE")


def update_game_state_with_move(state, legal_move):
    if len(legal_move.moves) > 0:
        start_row = legal_move.moves[0].fromRow
        start_column = legal_move.moves[0].fromColumn
        state.board[legal_move.endRow][legal_move.endColumn].piece = copy.deepcopy(state.board[start_row][start_column].piece)
        if is_king_condition(state, start_row, start_column, legal_move.endRow):
            state.board[legal_move.endRow][legal_move.endColumn].piece.king = True
        state.board[start_row][start_column].piece.color = 2
        if abs(start_row - legal_move.moves[0].toRow) == 2:
            state.emptyMoves = 0
            for move in legal_move.moves:
                state.board[(move.fromRow + move.toRow) // 2][(move.fromColumn + move.toColumn) // 2].piece.color = 2
        elif not state.board[start_row][start_column].piece.king:
            state.emptyMoves = 0
        else:
            state.emptyMoves = state.emptyMoves + 1
    else:
        print("BIG ERROR: legal_move doesn't have any moves in it")


def is_draw(state):
    return state.emptyMoves >= 40


def is_win(state):
    state_copy = copy.deepcopy(state)
    state_copy.activePlayer = (state.activePlayer + 1) % 2
    get_all_legal_moves(state_copy)
    for row in state_copy.board:
        for cell in row:
            if cell.piece.color == state_copy.activePlayer:
                if len(cell.possibleMoves) > 0:
                    return False
    return True


def is_game_over(state):
    is_draw(state) or is_win(state)


def send_message_ui(message):
    print(message)


def run_game(game):  # game = GameState
    while not is_game_over(game):
        get_all_legal_moves(game)
        send_game_state_to_ui(game)
        move = get_move_from_player(game)
        update_game_state_with_move(game, move)
        if is_draw(game):
            send_message_ui("It's a draw")
        elif is_win(game):
            if game.activePlayer == 0:
                name = "Red"
            else:
                name = "Black"
            send_message_ui(name + " is a winner!")
        else:
            game.activePlayer = (game.activePlayer + 1) % 2
