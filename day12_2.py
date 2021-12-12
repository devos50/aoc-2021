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
queue = [("start", ["start"], None)]
while queue:
    cur_point, cur_path, cave_visited_twice = queue.pop(0)
    if cur_point == "end":
        paths.add("-".join(cur_path))
        continue

    for next_point in edges[cur_point]:
        if next_point == "start":
            continue

        # Branch - either visit it twice or not
        if next_point.isupper():
            queue.append((next_point, cur_path + [next_point], cave_visited_twice))
        else:
            # Small cave
            if next_point not in cur_path:
                # We haven't visited the cave so far
                queue.append((next_point, cur_path + [next_point], cave_visited_twice))
            else:
                # We have visited the cave before
                if not cave_visited_twice:
                    queue.append((next_point, cur_path + [next_point], next_point))

print(len(paths))
