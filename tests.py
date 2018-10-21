from gamestate import *


def make_empty_board():
    board = []
    for row in range(8):
        temp_row = []
        for column in range(8):
            temp_row.append(Cell(2))
        board.append(temp_row)
    return board


def red_simple():
    return Cell(0)


def red_king():
    return Cell(0, True)


def black_simple():
    return Cell(1)


def black_king():
    return Cell(1, True)


test_board = make_empty_board()

test_board[0][6] = red_simple()
test_board[1][5] = red_simple()
test_board[2][0] = red_simple()
test_board[3][3] = red_simple()
test_board[6][2] = red_simple()
test_board[7][3] = red_simple()
test_board[7][7] = red_simple()

test_board[2][6] = black_simple()
test_board[3][1] = black_simple()
test_board[6][6] = black_simple()

test_board[2][2] = red_king()
test_board[3][5] = red_king()

test_board[0][0] = black_king()
test_board[2][4] = black_king()
test_board[5][1] = black_king()
test_board[6][4] = black_king()
test_board[7][1] = black_simple()
test_board[7][5] = black_king()

game = GameState(test_board)
send_game_state_to_ui(game)

# test can_jump_left
false_set = [[0, 0], [1, 5], [2, 0], [6, 2], [6, 4], [7, 3]]
true_set = [[2, 2], [2, 4]]
print("Testing can_jump_left")
for case in false_set:
    if game.can_jump_left(case[0], case[1]):
        print("can_jump_left failed: returned True instead of false")
        print("Case: row " + str(case[0]) + " column " + str(case[1]))
for case in true_set:
    if not game.can_jump_left(case[0], case[1]):
        print("can_jump_left failed: returned False instead of True")
        print("Case: row " + str(case[0]) + " column " + str(case[1]))

# test can_jump_right
false_set = [[0, 0], [0, 6], [2, 2], [3, 3], [6, 2], [6, 4], [7, 3]]
true_set = [[2, 0], [2, 4]]
print("Testing can_jump_right")
for case in false_set:
    if game.can_jump_right(case[0], case[1]):
        print("can_jump_right failed: returned True instead of false")
        print("Case: row " + str(case[0]) + " column " + str(case[1]))
for case in true_set:
    if not game.can_jump_right(case[0], case[1]):
        print("can_jump_right failed: returned False instead of True")
        print("Case: row " + str(case[0]) + " column " + str(case[1]))

# test can_jump_left_back
false_set = [[0, 0], [2, 2], [3, 1], [3, 3], [7, 5], [7, 7]]
true_set = [[3, 5], [2, 6]]
print("Testing can_jump_left_back")
for case in false_set:
    if game.can_jump_back_left(case[0], case[1]):
        print("can_jump_back_left failed: returned True instead of false")
        print("Case: row " + str(case[0]) + " column " + str(case[1]))
for case in true_set:
    if not game.can_jump_back_left(case[0], case[1]):
        print("can_jump_back_left failed: returned False instead of True")
        print("Case: row " + str(case[0]) + " column " + str(case[1]))

# test can_jump_back_right
false_set = [[0, 0], [2, 0], [2, 4], [7, 3], [7, 5]]
true_set = [[3, 1], [3, 5], [7, 1]]
print("Testing can_jump_left_back")
for case in false_set:
    if game.can_jump_back_right(case[0], case[1]):
        print("can_jump_back_right failed: returned True instead of false")
        print("Case: row " + str(case[0]) + " column " + str(case[1]))
for case in true_set:
    if not game.can_jump_back_right(case[0], case[1]):
        print("can_jump_back_right failed: returned False instead of True")
        print("Case: row " + str(case[0]) + " column " + str(case[1]))

# test can_move_left
false_set = [[0, 0], [2, 0], [2, 2], [2, 4], [3, 1], [7, 3], [7, 5]]
true_set = [[3, 3], [3, 5], [5, 1]]
print("Testing can_move_left")
for case in false_set:
    if game.can_move_left(case[0], case[1]):
        print("can_move_left failed: returned True instead of false")
        print("Case: row " + str(case[0]) + " column " + str(case[1]))
for case in true_set:
    if not game.can_move_left(case[0], case[1]):
        print("can_move_left failed: returned False instead of True")
        print("Case: row " + str(case[0]) + " column " + str(case[1]))

# test can_move_right
false_set = [[1, 5], [2, 0], [2, 2], [2, 4], [2, 6], [3, 1], [7, 3], [7, 5]]
true_set = [[0, 0], [0, 6], [3, 3]]
print("Testing can_move_right")
for case in false_set:
    if game.can_move_right(case[0], case[1]):
        print("can_move_right failed: returned True instead of false")
        print("Case: row " + str(case[0]) + " column " + str(case[1]))
for case in true_set:
    if not game.can_move_right(case[0], case[1]):
        print("can_move_right failed: returned False instead of True")
        print("Case: row " + str(case[0]) + " column " + str(case[1]))

# test can_move_back_left
false_set = [[0, 0], [0, 6], [2, 0], [2, 6], [3, 5], [7, 3], [7, 5]]
true_set = [[2, 2], [2, 4], [5, 1], [6, 4], [6, 6], [7, 1]]
print("Testing can_move_back_left")
for case in false_set:
    if game.can_move_back_left(case[0], case[1]):
        print("can_move_back_left failed: returned True instead of false")
        print("Case: row " + str(case[0]) + " column " + str(case[1]))
for case in true_set:
    if not game.can_move_back_left(case[0], case[1]):
        print("can_move_back_left failed: returned False instead of True")
        print("Case: row " + str(case[0]) + " column " + str(case[1]))

# test can_move_back_right
false_set = [[0, 0], [0, 6], [2, 0], [2, 4], [3, 1], [3, 5], [6, 2], [7, 3], [7, 5]]
true_set = [[2, 2], [2, 6], [5, 1], [6, 4], [6, 6]]
print("Testing can_move_back_right")
for case in false_set:
    if game.can_move_back_right(case[0], case[1]):
        print("can_move_back_right failed: returned True instead of false")
        print("Case: row " + str(case[0]) + " column " + str(case[1]))
for case in true_set:
    if not game.can_move_back_right(case[0], case[1]):
        print("can_move_back_right failed: returned False instead of True")
        print("Case: row " + str(case[0]) + " column " + str(case[1]))

# test append_legal_jump
print("Testing append_legal_jump")
moves = [LegalMove(2, 2, 5, [Move(0, 0, 0, 0)])]
not_to_add = LegalMove(2, 2, 4, [Move(0, 0, 0, 0)])
to_replace = LegalMove(2, 2, 6, [Move(0, 0, 0, 0)])
to_add = LegalMove(2, 3, 6, [Move(0, 0, 0, 0)])
not_to_add.append_legal_jump(moves)
if len(moves) > 0:
    if len(moves) != 1:
        print("append_legal_jump failed: added move that shouldn't be added")
    elif moves[0].piecesNumber == 4:
        print("append_legal_jump failed: a better move replaced with worse one")
else:
    print("append_legal_jump failed: list length is 0, should be 1")
to_replace.append_legal_jump(moves)
if len(moves) > 0:
    if len(moves) != 1:
        print("append_legal_jump failed: added move that shouldn't be added")
    elif moves[0].piecesNumber == 5:
        print("append_legal_jump failed: a better move didn't replaced the worse one")
else:
    print("append_legal_jump failed: list length is 0, should be 1")
to_add.append_legal_jump(moves)
if len(moves) > 0:
    if len(moves) != 2:
        print("append_legal_jump failed: didn't add a move to the path")
else:
    print("append_legal_jump failed: list length is 0, should be 1")

# test calculate_simple_moves
print("Testing calculate_simple_moves")
game.board = make_empty_board()
game.board[0][0] = black_king()
game.board[0][0] = black_king()
game.board[1][1] = red_simple()
game.board[1][3] = red_simple()
game.board[1][5] = red_simple()
game.board[3][3] = red_simple()
game.board[3][5] = red_simple()
game.board[6][2] = black_king()
game.activePlayer = 1
path = []
game.calculate_simple_moves(6, 2, path)
if len(path) != 4:
    print("calculate_simple_moves failed: wrong number of moves in the path")
else:
    if path[0].endRow != 7 or path[0].endColumn != 1:
        print("calculate_simple_moves failed: wrong first move destination")
    if path[1].endRow != 7 or path[1].endColumn != 3:
        print("calculate_simple_moves failed: wrong 2nd move destination")
    if path[2].endRow != 5 or path[2].endColumn != 1:
        print("calculate_simple_moves failed: wrong 3d move destination")
    if path[3].endRow != 5 or path[3].endColumn != 3:
        print("calculate_simple_moves failed: wrong 4th move destination")
    for m in path:
        if m.piecesNumber != 0:
            print("calculate_simple_moves failed: pieces number is not 0")

# testing update_game_state_with_move
print("Testing update_game_state_with_move")
game.board = make_empty_board()
red_pieces_list = [[1, 1], [1, 3], [1, 5], [3, 3], [3, 5]]
game.board[0][0] = black_king()
for p in red_pieces_list:
    game.board[p[0]][p[1]] = red_simple()
move = LegalMove(2, 2, 5, [Move(0, 0, 2, 2), Move(2, 2, 4, 4), Move(4, 4, 2, 6), Move(2, 6, 0, 4), Move(0, 4, 2, 2)])
game.update_game_state_with_move(move)
for p in red_pieces_list:
    if game.board[p[0]][p[1]].piece.color != 2:
        print("failed update_game_state_with_move: game state was not updated - the piece was not removed")
        print("piece's row " + str(p[0]) + " column " + str(p[1]))
if game.board[0][0].piece.color != 2:
    print("failed update_game_state_with_move: game state was not updated - the acting piece was not removed")
if game.board[2][2].piece.color != 1:
    print("failed update_game_state_with_move: game state was not updated - the acting piece was not moved to\
    the right spot")

# test calculate_legal_jumps
print("Testing calculate_legal_jumps")
game.board = make_empty_board()
game.board[0][0] = black_king()
game.board[6][6] = black_king()
red_pieces_list = red_pieces_list + [[5, 3]]
for p in red_pieces_list:
    game.board[p[0]][p[1]] = red_simple()
path = []
game.calculate_legal_jumps(0, 0, 0, [], path)
if len(path) != 2:
    print("failed calculate_legal_jumps: wrong number of possible jumps")
found_first = False
found_second = False
for jump in path:
    if jump.endRow == 6 and jump.endColumn == 2 and jump.piecesNumber == 5 and len(jump.moves) == 5:
        found_first = True
    if jump.endRow == 2 and jump.endColumn == 2 and jump.piecesNumber == 5 and len(jump.moves) == 5:
        found_second = True
if not found_first or not found_second:
    print("failed calculate_legal_jumps: missing a correct jump")

# test get_all_legal_moves
print("Testing get_all_legal_moves")
game.get_all_legal_moves()
if len(game.board[0][0].possibleMoves) != 2:
    print("failed get_all_legal_moves: wrong number of moves for [0, 0]")
else:
    for move in game.board[0][0].possibleMoves:
        if move.piecesNumber != 5:
            print("failed get_all_legal_moves: something's wrong with jump computation")
if len(game.board[6][6].possibleMoves) != 0:
    print("failed get_all_legal_moves: wrong number of moves for [6, 6]")
else:
    for move in game.board[6][6].possibleMoves:
        if move.piecesNumber != 0:
            print("failed get_all_legal_moves: something's wrong with jump computation")


run_game_state(GameState())
