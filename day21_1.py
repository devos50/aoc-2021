DICE_SIDES = 100
STARTING_POSITIONS = [5, 9]

dice_rolled = 0
cur_player_ind = 0
player_scores = [0, 0]
player_positions = [STARTING_POSITIONS[0] - 1, STARTING_POSITIONS[1] - 1]
dice_counter = 0

while True:
    print("Turn of player %d" % (cur_player_ind + 1))
    dice_sum = (dice_counter % DICE_SIDES + 1 + (dice_counter + 1) % DICE_SIDES + 1 + (dice_counter % DICE_SIDES + 2) + 1)
    dice_counter = (dice_counter + 3) % DICE_SIDES
    player_positions[cur_player_ind] = (player_positions[cur_player_ind] + dice_sum) % 10
    player_scores[cur_player_ind] += player_positions[cur_player_ind] + 1
    print("Total score after turn: %d" % player_scores[cur_player_ind])
    dice_rolled += 3
    if player_scores[cur_player_ind] >= 1000:
        print("Player %d wins!" % (cur_player_ind + 1))
        break
    cur_player_ind = (cur_player_ind + 1) % 2

losing_player_ind = (cur_player_ind + 1) % 2
print(dice_rolled)
print(player_scores[losing_player_ind] * dice_rolled)