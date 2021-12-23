from copy import deepcopy

NUM_FISHES = 16


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

    def __str__(self):
        return "Space %d" % self.num


def get_fish_type(fish_ind):
    if fish_ind in [0, 1, 2, 3]:
        return 1
    elif fish_ind in [4, 5, 6, 7]:
        return 2
    elif fish_ind in [8, 9, 10, 11]:
        return 3
    return 4


def encode_state(position):
    hash_sum = 0
    for ind in range(1, len(position) + 1):
        hash_sum += position[ind - 1] * (30 ** ind)
    return hash_sum


def decode_state(hash_sum, num_items):
    values = []
    for ind in range(num_items, 0, -1):
        values.append(hash_sum // (30 ** ind))
        hash_sum %= 30 ** ind
    return tuple(values[::-1])


target_rooms_for_fish_types = {1: [12, 13, 14, 15], 2: [16, 17, 18, 19], 3: [20, 21, 22, 23], 4: [24, 25, 26, 27]}
#start_positions = (15, 22, 25, 27, 12, 18, 20, 21, 16, 17, 23, 26, 13, 14, 19, 24)
#start_positions = (12, 17, 14, 15, 16, 13, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27)
start_positions = (19, 20, 22, 25, 16, 18, 21, 27, 15, 17, 24, 26, 12, 13, 14, 23)

# Prepare the field by creating spaces and connecting them
nodes = {}
for node_ind in range(1, 28):
    node = Space(node_ind, is_room=(node_ind >= 12))
    if node_ind >= 12:
        node.is_room = True
    nodes[node_ind] = node

for node_ind in range(1, 11):  # Connect hallway
    Space.connect(nodes[node_ind], nodes[node_ind + 1])

# Connect hallway <-> room
Space.connect(nodes[3], nodes[12])
Space.connect(nodes[5], nodes[16])
Space.connect(nodes[7], nodes[20])
Space.connect(nodes[9], nodes[24])

for node_ind in [12, 16, 20, 24]:  # Connect room <-> room
    Space.connect(nodes[node_ind], nodes[node_ind + 1])
    Space.connect(nodes[node_ind + 1], nodes[node_ind + 2])
    Space.connect(nodes[node_ind + 2], nodes[node_ind + 3])

min_score = 100000000000
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
            # Check the fishes 'below' us
            is_ok = True
            cur_room = positions[fish_ind] + 1
            while cur_room not in [16, 20, 24, 28]:
                if cur_room in positions:
                    # Occupied room
                    other_fish_type = get_fish_type(positions.index(cur_room))
                    if other_fish_type != get_fish_type(fish_ind):
                        is_ok = False
                        break
                cur_room += 1

            if is_ok:
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

                    if adj_space.num in [12, 16, 20, 24] and (adj_space.num + 1) not in positions:
                        will_stop = False
                    if adj_space.num in [13, 17, 21, 25] and (adj_space.num + 1) not in positions:
                        will_stop = False
                    if adj_space.num in [14, 18, 22, 26] and (adj_space.num + 1) not in positions:
                        will_stop = False

                    # check if there is no 'conflicting' fish in the adjacent room
                    cur_room = adj_space.num + 1
                    while cur_room not in [16, 20, 24, 28]:
                        if cur_room in positions:
                            # Occupied room
                            other_fish_type = get_fish_type(positions.index(cur_room))
                            if other_fish_type != get_fish_type(fish_ind):
                                will_stop = False
                                break
                        cur_room += 1

                if not nodes[positions[fish_ind]].is_room and not adj_space.is_room:  # Rule 3
                    will_stop = False

                if will_stop:
                    new_positions = list(deepcopy(positions))
                    new_positions[fish_ind] = adj_space.num
                    new_positions = tuple(new_positions)

                    additional_score = len(visited) * (10 ** (get_fish_type(fish_ind) - 1))
                    new_score = cur_score + additional_score

                    should_add = True
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
    if step % 1000 == 0:
        print(len(queue))
