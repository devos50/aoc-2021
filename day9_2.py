map = []
basin_lowest_points = []
basin_sizes = []


with open("data/day9.txt") as in_file:
    map = [[int(num) for num in line.strip()] for line in in_file.readlines()]


def get_lowest_adj(x, y):
    lowest = 100000
    for (x_diff, y_diff) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        cur_x = x + x_diff
        cur_y = y + y_diff
        if cur_x < 0 or cur_y < 0 or cur_x > len(map[0]) - 1 or cur_y > len(map) - 1:
            continue  # out of bounds

        if map[cur_y][cur_x] < lowest:
            lowest = map[cur_y][cur_x]

    return lowest


for y in range(len(map)):
    for x in range(len(map[0])):
        if get_lowest_adj(x, y) > map[y][x]:
            basin_lowest_points.append((x, y))

print(basin_lowest_points)

for lowest_point in basin_lowest_points:
    basin_points = set()
    basin_points.add(lowest_point)
    queue = [lowest_point]
    while queue:
        x, y = queue.pop(0)
        for (x_diff, y_diff) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            cur_x = x + x_diff
            cur_y = y + y_diff
            if cur_x < 0 or cur_y < 0 or cur_x > len(map[0]) - 1 or cur_y > len(map) - 1:
                continue  # out of bounds

            if map[cur_y][cur_x] != 9 and (cur_x, cur_y) not in basin_points:
                basin_points.add((cur_x, cur_y))
                if (cur_x, cur_y) not in queue:
                    queue.append((cur_x, cur_y))

    print("Basin size for (%d, %d): %d" % (lowest_point[0], lowest_point[1], len(basin_points)))
    basin_sizes.append(len(basin_points))


ans = 1

for size in sorted(basin_sizes, reverse=True)[:3]:
    ans *= size
print(ans)
