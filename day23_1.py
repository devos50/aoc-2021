from copy import deepcopy


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


target_rooms_for_fish_types = {1: [12, 13], 2: [14, 15], 3: [16, 17], 4: [18, 19]}
#start_positions = (14, 13, 12, 15, 16, 17, 18, 19)  # Positions of a1, a2, b1, b2, c1, c2, d1, d2
#start_positions = (13, 19, 12, 16, 14, 17, 15, 18)  # Positions of a1, a2, b1, b2, c1, c2, d1, d2
start_positions = (15, 16, 14, 19, 13, 18, 12, 17)  # Positions of a1, a2, b1, b2, c1, c2, d1, d2

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
queue = [(start_positions, 0)]  # State = (positions, current score)
while queue:
    positions, cur_score = queue.pop(0)
    evaluated[positions] = cur_score
    #print("Considering situation %s" % list(positions))

    # Is this a final configuration?
    if positions[0] in [12, 13] and positions[1] in [12, 13] and \
       positions[2] in [14, 15] and positions[3] in [14, 15] and \
       positions[4] in [16, 17] and positions[5] in [16, 17] and \
       positions[6] in [18, 19] and positions[7] in [18, 19]:
        if cur_score < min_score:
            print("New minimum score: %d" % cur_score)
            min_score = cur_score
        continue

    # For each fish, find the possible movements and add them to the queue
    for fish_ind in range(0, 8):
        #print("Looking at movements of fish %d (cur pos: %d)" % (fish_ind, positions[fish_ind]))
        if (fish_ind in [0, 1] and positions[fish_ind] in [12, 13]) or \
           (fish_ind in [2, 3] and positions[fish_ind] in [14, 15]) or \
           (fish_ind in [4, 5] and positions[fish_ind] in [16, 17]) or \
           (fish_ind in [6, 7] and positions[fish_ind] in [18, 19]):

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

        # TODO check if fish is already in the right room and if so, ignore
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
                    if new_positions in evaluated:
                        # We evaluated this state before
                        evaluated_score = evaluated[new_positions]
                        if evaluated_score <= cur_score:
                            should_add = False

                    for qind in range(len(queue)):
                        qpos, qscore = queue[qind]
                        if qpos == new_positions:
                            if qscore <= new_score:  # There is already an item with a lower score in the queue
                                should_add = False
                                break

                    if should_add:
                        #print("Will append: fish %d move from %d to %d (steps: %d)" % (fish_ind, positions[fish_ind], adj_space.num, len(visited)))
                        queue.append((new_positions, new_score))  # Consider it for a final state

    step += 1
    # if step == 1:
    #     break
    if step % 1000 == 0:
        print(positions)
        print(len(queue))

print(len(evaluated))
