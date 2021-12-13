points = []
folds = []
paper = []
max_x = 0
max_y = 0

with open("data/day13.txt") as in_file:
    parsing_folds = False
    for line in in_file.readlines():
        if not parsing_folds:
            if line == "\n":
                parsing_folds = True
                continue
            else:
                parts = line.strip().split(",")
                point = (int(parts[0]), int(parts[1]))
                max_x = max(max_x, point[0])
                max_y = max(max_y, point[1])
                points.append(point)
        else:
            parts = line.strip().split(" ")[-1].split("=")
            folds.append((parts[0], int(parts[1])))

# Create and fill paper
for y in range(max_y + 1):
    paper.append(['.'] * (max_x + 1))

for point in points:
    paper[point[1]][point[0]] = '#'

# print("Start:")
# for y in range(len(paper)):
#     print("".join(paper[y]))

for ind in range(len(folds)):
    fold = folds[ind]
    print("Processing fold: %s" % str(fold))
    if fold[0] == 'y':
        max_y = fold[1]
        for y in range(fold[1] + 1, max_y * 2 + 1):
            for x in range(len(paper[0])):
                if y >= len(paper):
                    continue
                if paper[y][x] == '#':
                    new_y = fold[1] - (y - fold[1])
                    paper[new_y][x] = '#'
                    paper[y][x] = '.'
    elif fold[0] == 'x':
        max_x = fold[1]
        for y in range(len(paper)):
            for x in range(fold[1] + 1, max_x * 2 + 1):
                if paper[y][x] == '#':
                    new_x = fold[1] - abs(x - fold[1])
                    paper[y][new_x] = '#'
                    paper[y][x] = '.'

print("After:")
for y in range(max_y + 1):
    print("".join(paper[y][:(max_x + 1)]))

# Count dots
dots = 0
for y in range(max_y + 1):
    for x in range(max_x + 1):
        if paper[y][x] == '#':
            dots += 1

print(dots)
