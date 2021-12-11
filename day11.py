levels = []
flashes = 0

with open("data/day11.txt") as in_file:
    levels = [[int(c) for c in line.strip()] for line in in_file.readlines()]

for day in range(1, 100000):
    print("Evaluating day %d" % day)
    did_flash = []
    for y in range(len(levels)):
            did_flash.append([0] * len(levels[0]))

    # 1) Increase energy
    for y in range(len(levels)):
        for x in range(len(levels[0])):
            levels[y][x] += 1

    # 2) Process flashes until there are no more
    while True:
        had_flashes = False
        for y in range(len(levels)):
            for x in range(len(levels[0])):
                #print("(%d, %d) -> %d, %d" % (x, y, levels[y][x], did_flash[y][x]))
                if levels[y][x] > 9 and not did_flash[y][x]:
                    #print("Flashing (%d, %d)" % (x, y))
                    # Flash
                    had_flashes = True
                    flashes += 1
                    did_flash[y][x] = True

                    for y_diff in [-1, 0, 1]:
                        for x_diff in [-1, 0, 1]:
                            if x_diff == 0 and y_diff == 0:
                                continue

                            adj_x = x + x_diff
                            adj_y = y + y_diff
                            if adj_x < 0 or adj_y < 0 or adj_x >= len(levels[0]) or adj_y >= len(levels):
                                continue

                            levels[adj_y][adj_x] += 1

                    # print("After flash:")
                    # for y2 in range(len(levels)):
                    #     print(levels[y2])

        if not had_flashes:
            break

    if all([all(row) for row in did_flash]):
        print(all(did_flash[0]))
        print("All: %d" % day)
        exit(0)

    # 3) Reset energy levels of flashed
    for y in range(len(levels)):
        for x in range(len(levels[0])):
            if did_flash[y][x]:
                levels[y][x] = 0

print(flashes)
for y in range(len(levels)):
    print(levels[y])
