edges = {}
paths = set()

with open("data/day12.txt") as in_file:
    for line in in_file.readlines():
        parts = line.strip().split("-")
        if parts[0] not in edges:
            edges[parts[0]] = []
        edges[parts[0]].append(parts[1])

        if parts[1] not in edges:
            edges[parts[1]] = []
        edges[parts[1]].append(parts[0])

# BFS
queue = [("start", ["start"])]
while queue:
    cur_point, cur_path = queue.pop(0)
    if cur_point == "end":
        paths.add("-".join(cur_path))

    for next_point in edges[cur_point]:
        if next_point == "start":
            continue
        if next_point.isupper() or (next_point.islower() and next_point not in cur_path):
            queue.append((next_point, cur_path + [next_point]))

print(len(paths))
