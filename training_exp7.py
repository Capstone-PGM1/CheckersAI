from qlearning import *

np.random.seed()
print("EXPERIMENT 7, depth=2, gamma=0.3, alpha=0.1, probablity=0.6 to 0.3 (-0.1 @ every 100000)")
win = 0
lose = 0
draw = 0
q_table = np.load('450000_exp4.npy').item()
q_player = RED
probability = 0.6
for i in range(1, 500001):
    result = run_training_game(GameState(), q_player, q_table, 2, probability, 0.3)
    if result > 0:
        win = win + 1
    elif result == 0:
        draw = draw + 1
    else:
        lose = lose + 1
    q_player = other_player(q_player)
    if (i % 50000) == 0:
        np.save(str(i) + "_exp7", q_table)
        print(str(i) + " games: win " + str(win) + " lose " + str(lose) + " draw " + str(draw))
        win = 0
        lose = 0
        draw = 0
        if (i % 100000) == 0 and probability > 0.3:
            probability = probability - 0.1
