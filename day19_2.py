import math
import operator
import itertools

scanner_readings = {}


def distance(vec1, vec2):
    return math.sqrt((vec1[0] - vec2[0]) ** 2 + (vec1[1] - vec2[1]) ** 2 + (vec1[2] - vec2[2]) ** 2)


def vec_add(vec1, vec2):
    return tuple(map(operator.add, vec1, vec2))


def vec_sub(vec1, vec2):
    return tuple(map(operator.sub, vec1, vec2))


with open("data/day19.txt") as in_file:
    readings = []
    cur_scanner = None
    for line in in_file:
        if line == "\n":
            continue
        elif line.startswith("---"):
            if cur_scanner:
                scanner_readings[cur_scanner] = readings
                readings = []

            cur_scanner = line.strip().split(" ")[-2]

        else:
            parts = line.strip().split(",")
            readings.append((int(parts[0]), int(parts[1]), int(parts[2])))

    scanner_readings[cur_scanner] = readings

print(scanner_readings)

# Precompute distances between beacons
distances = {}
for scanner in scanner_readings.keys():
    distances[scanner] = {}
    for reading1_ind in range(len(scanner_readings[scanner])):
        for reading2_ind in range(len(scanner_readings[scanner])):
            if reading1_ind == reading2_ind:
                continue

            d = distance(scanner_readings[scanner][reading1_ind], scanner_readings[scanner][reading2_ind])
            distances[scanner][(reading1_ind, reading2_ind)] = d

scanner_positions = {"0": (0, 0, 0)}

# For each pair of scanners, determine common beacons
for r in range(8):
    for scanner1 in list(scanner_positions.keys()):  # We are sure that we know the absolute position of scanner1
        for scanner2 in scanner_readings.keys():
            if scanner1 == scanner2 or scanner2 in scanner_positions:
                continue

            #print("Comparing scanner %s and %s" % (scanner1, scanner2))

            scan_map = {}
            for s1_beacon_from_to, d1 in distances[scanner1].items():
                for s2_beacon_from_to, d2 in distances[scanner2].items():
                    eqs = 0
                    if d1 == d2:
                        if not s1_beacon_from_to[0] in scan_map:
                            scan_map[s1_beacon_from_to[0]] = {s2_beacon_from_to[0], s2_beacon_from_to[1]}
                        else:
                            scan_map[s1_beacon_from_to[0]] = scan_map[s1_beacon_from_to[0]].intersection({s2_beacon_from_to[0], s2_beacon_from_to[1]})
                        #print("Found possible mapping: %s, %s" % (s1_beacon_from_to, s2_beacon_from_to))

            print("BEACON MAPPING: %s" % scan_map)
            final_vectors = set()
            if len(scan_map.keys()) >= 5:
                # There's enough overlap - we now have to find the rotation/permutation that gives us the position of the scanner
                should_stop = False
                for perm in list(itertools.permutations([0, 1, 2])):
                    if should_stop:
                        break
                    for op1 in [1, -1]:
                        if should_stop:
                            break
                        for op2 in [1, -1]:
                            if should_stop:
                                break
                            for op3 in [1, -1]:
                                # Is this rotation ok?
                                final_vectors = set()
                                for from_beacon, to_set in scan_map.items():
                                    beacon_coords_s1 = scanner_readings[scanner1][from_beacon]
                                    if not to_set:
                                        continue
                                    to_beacon = list(to_set)[0]
                                    beacon_coords_s2 = (scanner_readings[scanner2][to_beacon][perm[0]] * op1,
                                                        scanner_readings[scanner2][to_beacon][perm[1]] * op2,
                                                        scanner_readings[scanner2][to_beacon][perm[2]] * op3)
                                    final_vectors.add(vec_add(beacon_coords_s1, beacon_coords_s2))

                                if len(final_vectors) == 1:
                                    should_stop = True
                                    # We found a final vector which should now be translated to absolute coordinates.
                                    print("FV: %s" % final_vectors)
                                    print(scanner_positions[scanner1])
                                    print(perm)
                                    print("o1: %d, o2: %d, o3: %d" % (op1, op2, op3))
                                    scanner_pos = list(final_vectors)[0]
                                    scanner_positions[scanner2] = scanner_pos
                                    print("Found position of scanner %s: %s" % (scanner2, scanner_positions[scanner2]))

                                    # Rotate all the readings accordingly
                                    for ind in range(len(scanner_readings[scanner2])):
                                        orig = scanner_readings[scanner2][ind]
                                        #print("Will translate reading %d, %d, %d" % orig)
                                        beacon_pos = vec_add(scanner_positions[scanner2], (orig[perm[0]] * -op1, orig[perm[1]] * -op2, orig[perm[2]] * -op3))
                                        #print("beacon at: %d, %d, %d" % beacon_pos)
                                        scanner_readings[scanner2][ind] = beacon_pos
            else:
                print("Not enough info to determine overlap between scanners %s and %s" % (scanner1, scanner2))


# We have a bunch of relative positions now -> reconstruct the map
#print(scanner_positions)
#scanner_positions = {"0": (0, 0, 0), "1": (68,-1246,-43), "2": (1105,-1205,1229), "3": (-92,-2380,-20), "4": (-20,-1133,1061)}

largest_dist = 0
for scanner1 in scanner_readings.keys():
    for scanner2 in scanner_readings.keys():
        if scanner1 == scanner2:
            continue

        s1p = scanner_positions[scanner1]
        s2p = scanner_positions[scanner2]
        dist = abs(s1p[0] - s2p[0]) + abs(s1p[1] - s2p[1]) + abs(s1p[2] - s2p[2])
        if dist > largest_dist:
            largest_dist = dist

print(largest_dist)