from classes import *


def send_game_state_to_ui(state: GameState):
    print("", end="  ")
    for i in range(8):
        print(str(i), end=" ")
    print("")
    for row in range(8):
        print(row, end=" ")
        for column in range(8):
            if state.board[row][column] == 'x':
                if row % 2 == column % 2:
                    print("x", end=" ")
                else:
                    print("o", end=" ")
            else:
                print(state.board[row][column], end=" ")
        print("")


def get_move_from_player(state):
    if state.activePlayer == 0:
        name = "Red"
    else:
        name = "Black"
    print(name + " player's turn")
    if state.activePlayer == 1:
        show_moves = input("Y for show possible moves, N for input your move... ")
        moves = state.get_all_legal_moves()
        while show_moves != "N":
            row = int(input("row: "))
            column = int(input("column: "))
            for move in moves:
                if move.moves[0].fromRow == row and move.moves[0].fromColumn == column:
                    print('{0} {1} taking {2} pieces'.format(str(move.endRow), str(move.endColumn),
                                                             str(move.piecesNumber)))
            show_moves = input("Y for show possible moves, N for input your move... ")
        while True:
            print("Input the piece to move:")
            row = int(input("row: "))
            column = int(input("column: "))
            print("Where moving to?")
            row1 = int(input("row: "))
            column1 = int(input("column: "))
            if -1 < row < 8 and -1 < column < 8 and -1 < row1 < 8 and -1 < column1 < 8:
                for move in moves:
                    if move.endRow == row1 and move.endColumn == column1 and move.moves[0].fromRow == row and move.moves[0].fromColumn == column:
                        return move
    else:
        return state.get_ai_move(3)


# def get_move_from_player_for_network(possibleMoves):
#     show_moves = input("Y for show possible moves, N for input your move\n")
#     while show_moves != "N":
#         row = int(input("row: "))
#         column = int(input("column: "))
#         if (row, column) in possibleMoves:
#             for move in possibleMoves[(row, column)]:
#                 print(move)
#                 print('{0} {1} taking {2} pieces'.format(str(move['endRow']), str(move['endColumn']),
#                                                          str(move['piecesNumber'])))
#             show_moves = input("Y for show possible moves, N for input your move")
#     while True:
#         print("Input the piece to move: ")
#         row = int(input("row: "))
#         column = int(input("column: "))
#         print("Where moving to?")
#         row1 = int(input("row: "))
#         column1 = int(input("column: "))
#         if (row, column) in possibleMoves:
#             for move in possibleMoves[(row, column)]:
#                 if move['endRow'] == row1 and move['endColumn'] == column1:
#                     return {"startRow": row, "startColumn": column, "endRow": row1, "endColumn": column1}


def send_message_ui(message):
    print(message)


def run_game_state(game: GameState):  # game = GameState
    moves = game.get_all_legal_moves()
    while not game.is_game_over(moves)[0]:
        send_game_state_to_ui(game)
        move = get_move_from_player(game)
        game.update_game_state_with_move_helper(move)
        game.switch_player()
        moves = game.get_all_legal_moves()
    send_game_state_to_ui(game)
    if game.is_draw():
        send_message_ui("It's a draw")
    else:
        if game.is_win(moves) == 1:
            name = "Black"
        else:
            name = "Red"
        send_message_ui(name + " is a winner!")
