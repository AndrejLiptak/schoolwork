import random


def dice(prob_six=1 / 6):
    throw = random.random()
    if throw < prob_six:
        return 6
    else:
        return random.randint(1, 5)


def feedback(output, position, new_pos, throws, turn):
    if output:
        if len(throws) > 1:
            thr = tuple(throws)
        else:
            thr = "({0})".format(throws[0])
        print("{0} -> {1} in round {2} {3}"
              .format(position, new_pos, turn, thr))


def six_throw(throws, prob_six):
    while len(throws) < 3 and sum(throws) % 6 == 0:
        throws.append(dice(prob_six))
    if sum(throws) == 18:
        return 6
    else:
        return sum(throws)


def game(size, prob_six=1 / 6, output=True):
    if size < 2:
        if output:
            print("Error: plan too small!")
        return None
    turn = 0
    position = 0
    while position != size:
        turn += 1
        throws = []
        move = dice(prob_six)
        throws.append(move)
        if position == 0 and move == 6:
            feedback(output, position, 1, throws, turn)
            position = 1
            continue
        elif position == 0:
            feedback(output, position, 0, throws, turn)
            continue
        if move == 6:
            move = six_throw(throws, prob_six)
        if position + move >= size:
            feedback(output, position, size, throws, turn)
            if output:
                print("Game finished in round {}.".format(turn))
            return turn
        feedback(output, position, position + move, throws, turn)
        position += move


def average_game(size, games_count, prob_six=1 / 6):
    sum_of_turns = 0
    for _ in range(games_count):
        sum_of_turns += game(size, prob_six, False)
    return sum_of_turns / games_count


def find_optimal_probability(size, games_count=1000, partition=20,
                             show_output=False):
    lengths = []
    probabilities = []
    for i in range(1, partition):
        prob = (1 / partition) * i
        avg_len = average_game(size, games_count, prob)
        lengths.append(avg_len)
        probabilities.append(prob)
        if show_output:
            print("Probability of six: {0:.2f} Game length: {1:.2f}"
                  .format(prob, avg_len))
    return probabilities[(lengths.index(min(lengths)))]
