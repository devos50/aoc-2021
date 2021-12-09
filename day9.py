map = []

with open("data/day9.txt") as in_file:
    map = [[int(num) for num in line.strip()] for line in in_file.readlines()]


def get_lowest_adj(x, y):
    lowest = 100000
    for (x_diff, y_diff) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if x_diff == 0 and y_diff == 0:
            continue

        cur_x = x + x_diff
        cur_y = y + y_diff
        if cur_x < 0 or cur_y < 0 or cur_x > len(map[0]) - 1 or cur_y > len(map) - 1:
            continue  # out of bounds

        if map[cur_y][cur_x] < lowest:
            lowest = map[cur_y][cur_x]

    return lowest


ans = 0
for y in range(len(map)):
    for x in range(len(map[0])):
        if get_lowest_adj(x, y) > map[y][x]:
            ans += 1 + map[y][x]

print(ans)