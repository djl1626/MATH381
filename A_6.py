import pandas as p
import numpy as np
import random

# set starting score
x_01 = 301

# calculate areas of various sections of the board
double_bull = np.pi * 6.35 ** 2
single_bull = np.pi * 15.9 ** 2 - double_bull
inner_single_area = np.pi * 115 ** 2 - np.pi * 15.9 ** 2
triple_area = np.pi * 117 ** 2 - np.pi * 115 ** 2
outer_single_area = np.pi * 162 ** 2 - np.pi * 117 ** 2
double_area = np.pi * 170 ** 2 - np.pi * 162 ** 2
total_area = np.pi * 170 ** 2

# list of all numbers on the dart board
board_scores = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]
three_score_dict = {}
scores_angles_dict = {}
top_score_zones_dict = {0: [16, 7, 19], 1: [19, 3, 17], 2: [18, 1, 20], 3: [20, 5, 12]}

# create dictionary of each score and the angles that it is between (pos. X axis is zero)
for i in range(1, len(board_scores)):
    scores_angles_dict[board_scores[i]] = [18 * i - 9, 18 * (i + 1) - 9]

# create dictionary with all possible combinations of 3 numbers (grouped)
for i in range(len(board_scores) - 1):
    if i == len(board_scores) - 2:
        three_score_dict[i] = [board_scores[i], board_scores[i + 1], board_scores[0]]
        three_score_dict[i + 1] = [board_scores[i + 1], board_scores[0], board_scores[1]]
    else:
        three_score_dict[i] = [board_scores[i], board_scores[i + 1], board_scores[i + 2]]


# simulate the score of one dart throw for nonrandom throw
def one_dart_score_B(scores):
    angle = random.uniform(0, 54)
    radius = random.uniform(0, 170)
    if radius < 6.35:
        return 50
    elif radius < 15.9:
        return 25
    if angle < 18:
        if radius < 107:
            return scores[0]
        elif radius < 115:
            return 3 * scores[0]
        elif radius < 162:
            return scores[0]
        else:
            return 2 * scores[0]
    elif angle < 36:
        if radius < 107:
            return scores[1]
        elif radius < 115:
            return 3 * scores[1]
        elif radius < 162:
            return scores[1]
        else:
            return 2 * scores[1]
    else:
        if radius < 107:
            return scores[2]
        elif radius < 115:
            return 3 * scores[2]
        elif radius < 162:
            return scores[2]
        else:
            return 2 * scores[2]


# simulate the score of one dart throw for random throw
def one_dart_score_A():
    angle = random.uniform(0, 360)
    radius = random.uniform(0, 170)
    if radius < 6.35:
        return 50
    elif radius < 15.9:
        return 25
    if 125 > radius >= 117:
        multiplier = 3
    elif radius >= 162:
        multiplier = 2
    else:
        multiplier = 1
    if 9 >= angle >= 0 or 360 > angle > 351:
        return multiplier * 6
    else:
        for key in scores_angles_dict.keys():
            if scores_angles_dict[key][1] > angle >= scores_angles_dict[key][0]:
                return multiplier * key


# simulate one round of throws for random player
def one_round_A(player_score):
    darts = 0
    while player_score > 0 and darts < 3:
        player_score -= one_dart_score_A()
        darts += 1
    return player_score


# simulate one round of throws for nonrandom player
def one_round_B(player_score, scores):
    darts = 0
    while player_score > 0 and darts < 3:
        player_score -= one_dart_score_B(scores)
        darts += 1
    return player_score


# simulate one game between random player and nonrandom player
def one_game(player_b_scores):
    player_a_score = x_01
    player_b_score = x_01
    while player_a_score > 0 and player_b_score > 0:
        player_a_score = one_round_A(player_a_score)
        if player_a_score <= 0:
            return 0
        player_b_score = one_round_B(player_b_score, player_b_scores)
        if player_b_score <= 0:
            return 1


# simulate game between two players aiming at one of the top 4 score zones
def one_game_top_4_scores(player_a_scores, player_b_scores):
    player_a_score = x_01
    player_b_score = x_01
    first = random.randint(0, 1)
    if first == 0:
        while player_a_score > 0 and player_b_score > 0:
            player_a_score = one_round_B(player_a_score, player_a_scores)
            if player_a_score <= 0:
                return 0
            player_b_score = one_round_B(player_b_score, player_b_scores)
            if player_b_score <= 0:
                return 1
    else:
        while player_a_score > 0 and player_b_score > 0:
            player_b_score = one_round_B(player_b_score, player_b_scores)
            if player_b_score <= 0:
                return 1
            player_a_score = one_round_B(player_a_score, player_a_scores)
            if player_a_score <= 0:
                return 0


# calculate expected scores for the random player
def expected_scores_player_a():
    exp_score_a = 50 * double_bull / total_area + 25 * single_bull / total_area
    inner_single_area_one_score = inner_single_area / 20
    outer_single_area_one_score = outer_single_area / 20
    triple_area_one_score = triple_area / 20
    double_area_one_score = double_area / 20
    single_probability = (inner_single_area_one_score + outer_single_area_one_score) / total_area
    double_probability = double_area_one_score / total_area
    triple_probability = triple_area_one_score / total_area
    for val in board_scores:
        exp_score_a += val * (single_probability + 2 * double_probability + 3 * triple_probability)
    return exp_score_a


# calculate the expected scores for all score zones
def expected_scores_player_b():
    double_bull_in_zone = double_bull * .15
    single_bull_in_zone = single_bull * .15
    inner_single_area_one_score = inner_single_area / 20
    outer_single_area_one_score = outer_single_area / 20
    triple_area_one_score = triple_area / 20
    double_area_one_score = double_area / 20
    total_area_one_zone = double_bull_in_zone + single_bull_in_zone + 3 * (inner_single_area_one_score +
                                                                           outer_single_area_one_score +
                                                                           triple_area_one_score +
                                                                           double_area_one_score)
    single_probability = (inner_single_area_one_score + outer_single_area_one_score) / total_area_one_zone
    double_probability = double_area_one_score / total_area_one_zone
    triple_probability = triple_area_one_score / total_area_one_zone
    exp_scores_b_df = p.DataFrame({"Score Zone": [],
                                   "Expected Round Score": [],
                                   "Min Score": [],
                                   "Max Score": []})
    for val in three_score_dict.values():
        exp_score_b = 50 * double_bull_in_zone / total_area_one_zone + 25 * single_bull_in_zone / total_area_one_zone
        for k in range(0, len(val)):
            exp_score_b += val[k] * (single_probability + 2 * double_probability + 3 * triple_probability)
        exp_scores_b_df.loc[len(exp_scores_b_df)] = [str(val), exp_score_b * 3, min(val), max(val)]
    return exp_scores_b_df


if __name__ == '__main__':
    expected_score_random_player = expected_scores_player_a() * 3
    expected_score_df = expected_scores_player_b()
    wins_df = p.DataFrame({"Score Zone": [],
                           "Min Prob": [],
                           "Max Prob": [],
                           "Prob Win Conf Interval": []})
    convergence_df = p.DataFrame({})

    # run a simulation of games for random player vs nonrandom player for each score zone
    for element in three_score_dict.values():
        wins_list = []
        for i in range(0, 10):
            wins_list.append(0)
            if element == [6, 13, 4]:
                convergence_list = []
            for j in range(0, 100000):
                winner = one_game(element)
                if winner == 1:
                    wins_list[i] += 1
                if element == [6, 13, 4]:
                    convergence_list.append(wins_list[i] / (j + 1))
            if element == [6, 13, 4]:
                convergence_df[i + 1] = convergence_list
        print("done simulating " + str(element))
        wins_df.loc[len(wins_df.index)] = [str(element), min(wins_list) / 100000, max(wins_list) / 100000,
                                           str([min(wins_list) / 100000, max(wins_list) / 100000])]
        print([str(element), min(wins_list) / 100000, max(wins_list) / 100000,
               str([min(wins_list) / 100000, max(wins_list) / 100000])])
    print(expected_score_random_player)
    expected_score_df.to_csv("/Users/djl47/PycharmProjects/MATH_381/expected_scores_table.txt", index=False)
    convergence_df.to_csv("/Users/djl47/PycharmProjects/MATH_381/convergence_table.txt", index=False)
    wins_df.to_csv("/Users/djl47/PycharmProjects/MATH_381/simulations_table.txt", index=False)

    top_4_wins_df = p.DataFrame({"Score Zone A": [],
                                 "Score Zone B": [],
                                 "Min Win Prob A": [],
                                 "Max Win Prob A": [],
                                 "Prob A Win Conf Interval": []})
    run_probabilities_df = p.DataFrame({"Run": [],
                                        "Prob A Win": []})

    # run simulations for nonrandom player vs nonrandom player (top 4 score zones)
    for i in range(len(top_score_zones_dict.keys())):
        for j in range(i + 1, len(top_score_zones_dict.keys())):
            a_wins_list = []
            for r in range(1000):
                a_wins_list.append(0)
                for k in range(10000):
                    winner = one_game_top_4_scores(top_score_zones_dict[i], top_score_zones_dict[j])
                    if winner == 0:
                        a_wins_list[r] += 1
                if i == 0 and j == 1:
                    run_probabilities_df.loc[len(run_probabilities_df)] = [r + 1, a_wins_list[r]]
                if r % 100 == 99:
                    print("Done " + str(r + 1) + " simulations of " + str(top_score_zones_dict[i]) + " vs " +
                          str(top_score_zones_dict[j]))
            print("Done simulating " + str(top_score_zones_dict[i]) + " vs " + str(top_score_zones_dict[j]))
            top_4_wins_df.loc[len(top_4_wins_df.index)] = [str(top_score_zones_dict[i]), str(top_score_zones_dict[j]),
                                                           min(a_wins_list) / 10000, max(a_wins_list) / 10000,
                                                           str([min(a_wins_list) / 10000, max(a_wins_list) / 10000])]
    run_probabilities_df.to_csv("/Users/djl47/PycharmProjects/MATH_381/run_probabilities_table.txt", index=False)
    top_4_wins_df.to_csv("/Users/djl47/PycharmProjects/MATH_381/top_four_simulations_table.txt", index=False)