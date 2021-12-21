STARTING_POSITIONS = [5, 9]
WIN_SCORE = 21

states = {0: {}}  # {turn => (score_1, score_2, pos_1, pos_2)}
states[0][(0, 0, STARTING_POSITIONS[0] - 1, STARTING_POSITIONS[1] - 1)] = 1  # Base state

# Make a frequency map of the possibilities of three dice rolls
dice_possibilities = {}
for dice_roll_1 in [1, 2, 3]:
    for dice_roll_2 in [1, 2, 3]:
        for dice_roll_3 in [1, 2, 3]:
            dice_sum = dice_roll_1 + dice_roll_2 + dice_roll_3
            if dice_sum not in dice_possibilities:
                dice_possibilities[dice_sum] = 0
            dice_possibilities[dice_sum] += 1

print(dice_possibilities)

for turn in range(1, 21):
    current_player = (turn + 1) % 2
    states[turn] = {}
    print("Evaluating turn %d" % turn)
    # Extend all states of the previous turn
    for prior_state, prior_freq in states[turn - 1].items():
        # Do not extend states in which one of the players did win already
        if prior_state[0] >= WIN_SCORE or prior_state[1] >= WIN_SCORE:
            continue

        for dice_possibility, freq in dice_possibilities.items():
            # Compute the new position + new score of this player
            old_score = prior_state[0] if current_player == 0 else prior_state[1]
            old_pos = prior_state[2] if current_player == 0 else prior_state[3]
            new_pos = (old_pos + dice_possibility) % 10
            new_score = old_score + new_pos + 1
            if current_player == 0:
                new_state = (new_score, prior_state[1], new_pos, prior_state[3])
            else:
                new_state = (prior_state[0], new_score, prior_state[2], new_pos)

            if new_state not in states[turn]:
                states[turn][new_state] = prior_freq * freq
            else:
                states[turn][new_state] += prior_freq * freq


# Find all the states in which player 1 wins and sum them
p1_universes = 0
p2_universes = 0
for turn, tstates in states.items():
    for state, state_freq in tstates.items():
        if state[0] >= WIN_SCORE:
            p1_universes += state_freq
        if state[1] >= WIN_SCORE:
            p2_universes += state_freq

print(p1_universes)
print(p2_universes)
