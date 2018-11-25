from classes import *
import numpy as np

ALPHA = 0.1
GAMMA = 0.5
PROBABILITY = 0.5

#     # 0 player_kings: int
#     # 1 other_player_kings: int
#     # 2 player_pawns: int
#     # 3 other_player_pawns: int
#     # 4 player_corners: int
#     # 5 other_player_corners: int
#     # 6 player_first_row: int
#     # 7 other_player_first_row: int
#     # 8 player_blocked: int
#     # 9 other_player_blocked : int
#     # 10 first_row: int
#     # 11 other_first_row: int


def new_state():
    return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def state_to_string(state):
    return "".join(str(s) for s in state)


def get_state_from_board(game: GameState, q_player: int):
    state = new_state()
    q_first_row = 0 if q_player == RED else 7
    min_first_row = 7 if q_player == RED else 0

    for row in range(8):
        for column in range(8):
            if game.board[row][column].upper() == piece_to_letter(q_player, True):
                if game.board[row][column].isupper():
                    state[0] = state[0] + 1
                else:
                    state[2] = state[2] + 11
                path = []
                game.calculate_legal_jumps(row, column, 0, [], path)
                if len(path) == 0:
                    game.calculate_simple_moves(row, column, path)
                    if len(path) == 0:
                        state[8] = state[8] + 1
                if column == 0 or column == 7:
                    state[4] = state[4] + 1
                if row == q_first_row:
                    state[10] = state[10] + 1
            elif game.board[row][column] != 'x':
                if game.board[row][column].isupper():
                    state[1] = state[1] + 1
                else:
                    state[2] = state[2] + 1
                if row == min_first_row:
                    state[11] = state[11] + 1
                if column == 0 or column == 7:
                    state[5] = state[5] + 1
                path = []
                game.calculate_legal_jumps(row, column, 0, [], path)
                if len(path) == 0:
                    game.calculate_simple_moves(row, column, path)
                    if len(path) == 0:
                        state[9] = state[9] + 1
    return state_to_string(state)


# Q_Table: {(state1: Q_State): {state2: QState, val )}}
def update_q_value(current_val, new_val):
    return (1 - ALPHA) * current_val + ALPHA * new_val


def get_new_q_val(reward, max_q):
    return reward + GAMMA * max_q


def run_training_game(game: GameState, q_player: int, q_table: dict, mm_depth: int):
    moves = game.get_all_legal_moves()
    while not game.is_game_over(moves)[0]:
        from_state = get_state_from_board(game, q_player)
        if q_table.get(from_state) is None:
            q_table.update({from_state: {}})
        # get next move
        if len(moves) == 1:
            move = moves[0]  # sometimes there is just 1 jump available
        else:
            if game.activePlayer == q_player:
                is_random = np.random.choice([True, False], p=[1.0 - PROBABILITY, PROBABILITY])
                if is_random:
                    move = np.random.choice(moves)
                else:  # finding move with biggest q val so far
                    max_q_val = -sys.maxsize - 1
                    move = moves[0]
                    for m in moves:
                        copy_game = GameState(copy.deepcopy(game.board), game.emptyMoves, game.activePlayer)
                        copy_game.update_game_state_with_move_helper(m)
                        to_state = get_state_from_board(copy_game, q_player)
                        state_val = q_table.get(from_state)
                        trans_val = state_val.get(to_state, 0)
                        if trans_val > max_q_val:
                            max_q_val = trans_val
                            move = m
                        elif trans_val == max_q_val:
                            move = np.random.choice([move, m])
            else:
                move = game.get_ai_move(mm_depth)
        game.update_game_state_with_move_helper(move)
        to_state = get_state_from_board(game, q_player)
        # need to find ax q_value for all transitions from to_state
        state_val = q_table.get(to_state)
        if state_val is not None and bool(state_val):
            max_trans_val = max(i for i in state_val.values())
        else:
            max_trans_val = 0
        # get the current val
        state_val = q_table.get(from_state)
        cur_val = state_val.get(to_state, 0)
        q_table[from_state].update({to_state: update_q_value(cur_val, get_new_q_val(0, max_trans_val))})
        game.switch_player()
        moves = game.get_all_legal_moves()
    if game.is_draw():
        print("DRAW")
        reward = sys.maxsize / 2
    else:
        if game.is_win(moves) == q_player:
            reward = sys.maxsize
            print("WIN")
        else:
            reward = -sys.maxsize - 1
            print("LOST")

    q_table[from_state].update({to_state: update_q_value(q_table[from_state].get(to_state),
                                                         get_new_q_val(reward, q_table[from_state].get(to_state)))})


def run_checking_game(game: GameState, q_player: int, q_table: dict, mm_depth: int):
    moves = game.get_all_legal_moves()
    while not game.is_game_over(moves)[0]:
        from_state = get_state_from_board(game, q_player)
        # get next move
        if len(moves) == 1:
            move = moves[0]  # sometimes there is just 1 jump available
        else:
            if game.activePlayer == q_player:
                state_val = q_table.get(from_state)
                if state_val is None:
                    print("New State")
                    move = np.random.choice(moves)
                else:
                    max_q_val = -sys.maxsize - 1
                    move = moves[0]
                    for m in moves:
                        copy_game = GameState(copy.deepcopy(game.board), game.emptyMoves, game.activePlayer)
                        copy_game.update_game_state_with_move_helper(m)
                        to_state = get_state_from_board(copy_game, q_player)
                        trans_val = state_val.get(to_state, 0)
                        if trans_val > max_q_val:
                            max_q_val = trans_val
                            move = m
                        elif trans_val == max_q_val:
                            move = np.random.choice([move, m])
            else:
                move = game.get_ai_move(mm_depth)
        game.update_game_state_with_move_helper(move)
        game.switch_player()
        moves = game.get_all_legal_moves()
    if game.is_draw():
        return 0
    else:
        if game.is_win(moves) == q_player:
            return 1
        else:
            return -1

