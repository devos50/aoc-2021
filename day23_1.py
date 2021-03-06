from copy import deepcopy

NUM_FISHES = 8


class Space:

    def __init__(self, num, is_room):
        self.num = num
        self.is_room = is_room
        self.adjacent = []

    @staticmethod
    def connect(s1, s2):
        s1.adjacent.append(s2)
        s2.adjacent.append(s1)

    def is_in_front_of_door(self):
        return self.num in [3, 5, 7, 9]

    def get_adj_room(self):
        for adj in self.adjacent:
            if adj.is_room:
                return adj
        return None

    def __str__(self):
        return "Space %d" % self.num


def get_fish_type(fish_ind):
    if fish_ind in [0, 1]:
        return 1
    elif fish_ind in [2, 3]:
        return 2
    elif fish_ind in [4, 5]:
        return 3
    return 4


def encode_state(position):
    hash_sum = 0
    for ind in range(1, len(position) + 1):
        hash_sum += position[ind - 1] * (20 ** ind)
    return hash_sum


def decode_state(hash_sum, num_items):
    values = []
    for ind in range(num_items, 0, -1):
        values.append(hash_sum // (20 ** ind))
        hash_sum %= 20 ** ind
    return tuple(values[::-1])


target_rooms_for_fish_types = {1: [12, 13], 2: [14, 15], 3: [16, 17], 4: [18, 19]}
#start_positions = (14, 13, 12, 15, 16, 17, 18, 19)  # Positions of a1, a2, b1, b2, c1, c2, d1, d2
start_positions = (13, 19, 12, 16, 14, 17, 15, 18)  # Positions of a1, a2, b1, b2, c1, c2, d1, d2
#start_positions = (15, 16, 14, 19, 13, 18, 12, 17)  # Positions of a1, a2, b1, b2, c1, c2, d1, d2

# Prepare the field by creating spaces and connecting them
nodes = {}
for node_ind in range(1, 20):
    node = Space(node_ind, is_room=(node_ind >= 12))
    if node_ind >= 12:
        node.is_room = True
    nodes[node_ind] = node

for node_ind in range(1, 11):  # Connect hallway
    Space.connect(nodes[node_ind], nodes[node_ind + 1])
for node_ind in [3, 5, 7, 9]:  # Connect hallway <-> room
    Space.connect(nodes[node_ind], nodes[node_ind + 9])
for node_ind in [12, 14, 16, 18]:  # Connect room <-> room
    Space.connect(nodes[node_ind], nodes[node_ind + 1])

min_score = 100000000
step = 0

evaluated = {}
initial_state = [encode_state(start_positions), 0]
queue_entry_map = {encode_state(start_positions): initial_state}  # Maintain the board states for quick lookup, enc(positions) -> score
queue = [initial_state]  # State = (positions, current score)
while queue:
    encoded_state, cur_score = queue.pop(0)
    positions = decode_state(encoded_state, NUM_FISHES)
    queue_entry_map.pop(encoded_state)
    #print("Considering situation %s" % list(positions))

    # Is this a final configuration?
    fish_in_right_rooms = [positions[fish_ind] in target_rooms_for_fish_types[get_fish_type(fish_ind)] for fish_ind in range(NUM_FISHES)]
    if all(fish_in_right_rooms):
        if cur_score < min_score:
            print("New minimum score: %d" % cur_score)
            min_score = cur_score
        continue

    # For each fish, find the possible movements and add them to the queue
    for fish_ind in range(0, NUM_FISHES):
        #print("Looking at movements of fish %d (cur pos: %d)" % (fish_ind, positions[fish_ind]))
        is_in_right_room = positions[fish_ind] in target_rooms_for_fish_types[get_fish_type(fish_ind)]
        if is_in_right_room:
            # Check if we are in the right room and should move.
            our_target_rooms = target_rooms_for_fish_types[get_fish_type(fish_ind)]
            if positions[fish_ind] == our_target_rooms[1]:
                continue  # We are at the lower half - don't move, we're fine
            elif positions[fish_ind] == our_target_rooms[0] and our_target_rooms[1] in positions:
                # Only move if the fish below us is conflicting
                other_fish_type = get_fish_type(positions.index(our_target_rooms[1]))
                if other_fish_type == get_fish_type(fish_ind):
                    # Other fish is of the same type - we're good.
                    continue

        fish_pos_queue = [(positions[fish_ind], [positions[fish_ind]])]
        while fish_pos_queue:
            cur_fish_pos, visited = fish_pos_queue.pop()
            cur_fish_space = nodes[cur_fish_pos]

            for adj_space in cur_fish_space.adjacent:
                if adj_space.num in positions or adj_space.num in visited:
                    continue

                #print("Fish %d can move to %d (visited: %s)" % (fish_ind, adj_space.num, visited))

                # The space is free - consider this state if it's not in front of a door
                new_visited = visited.copy()
                new_visited.append(adj_space.num)

                if (adj_space.num, new_visited) not in fish_pos_queue:
                    fish_pos_queue.append((adj_space.num, new_visited))

                will_stop = True
                if adj_space.is_in_front_of_door():  # Rule 1
                    will_stop = False
                if adj_space.is_room:  # Rule 2
                    # We move to a room

                    # Check if this is the destination
                    if adj_space.num not in target_rooms_for_fish_types[get_fish_type(fish_ind)]:
                        will_stop = False

                    if adj_space.num in [12, 14, 16, 18] and (adj_space.num + 1) not in positions:
                        will_stop = False

                    # check if there is no 'conflicting' fish in the adjacent room
                    adj_room = adj_space.get_adj_room()
                    if adj_room.num in positions:
                        occupied_fish_type = get_fish_type(positions.index(adj_room.num))
                        if occupied_fish_type != get_fish_type(fish_ind):
                            will_stop = False
                if not nodes[positions[fish_ind]].is_room and not adj_space.is_room:  # Rule 3
                    will_stop = False

                if will_stop:
                    new_positions = list(deepcopy(positions))
                    new_positions[fish_ind] = adj_space.num
                    new_positions = tuple(new_positions)

                    additional_score = len(visited) * (10 ** (get_fish_type(fish_ind) - 1))
                    new_score = cur_score + additional_score

                    # Determine if we should evaluate this state - only do so if we
                    # a) have not determined a state with a lower score before
                    # b)
                    should_add = True
                    # if new_positions in evaluated:
                    #     # We evaluated this state before
                    #     evaluated_score = evaluated[new_positions]
                    #     if evaluated_score <= cur_score:
                    #         should_add = False

                    # for qind in range(len(queue)):
                    #     qpos, qscore = queue[qind]
                    #     if qpos == new_positions:
                    #         if qscore <= new_score:  # There is already an item with a lower score in the queue
                    #             should_add = False
                    #             break

                    new_state = encode_state(new_positions)
                    if new_state in queue_entry_map:
                        # We already have an entry like this in the queue - if the score in the queue is higher, replace the queue score with the new (lower) score
                        if queue_entry_map[new_state][1] > new_score:
                            queue_entry_map[new_state][1] = new_score
                        should_add = False

                    if should_add:
                        #print("Will append: fish %d move from %d to %d (steps: %d)" % (fish_ind, positions[fish_ind], adj_space.num, len(visited)))
                        queue_entry = [new_state, new_score]
                        queue.append(queue_entry)  # Consider it for a final state
                        queue_entry_map[new_state] = queue_entry

    step += 1
    # if step == 1:
    #     break
    if step % 1000 == 0:
        print(len(queue))
