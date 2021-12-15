from collections import defaultdict
from heapq import *

cave = []
edges = []
growth_factor = 5

with open("data/day15.txt") as in_file:
    for line in in_file.readlines():
        cave.append([int(c) for c in line.strip()])


def dijkstra(edges, f, t):  # Copied from https://gist.github.com/kachayev/5990802
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))

    q, seen, mins = [(0,f,())], set(), {f: 0}
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t:
                return (cost, path)
            for c, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))

    return float("inf"), None


# Convert risk map to edges so we can feed it to Dijkstra()
edges = []
for y in range(len(cave) * growth_factor):
    for x in range(len(cave[0]) * growth_factor):
        for x_diff, y_diff in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x = x + x_diff
            new_y = y + y_diff
            if new_x < 0 or new_y < 0 or new_x >= len(cave[0]) * growth_factor or new_y >= len(cave) * growth_factor:
                continue

            # Project coordinate on the original plane and determine the risk value based on the offset
            original_x = new_x % len(cave[0])
            original_y = new_y % len(cave)
            tile_x = new_x // len(cave[0])
            tile_y = new_y // len(cave)
            risk_value = ((cave[original_y][original_x] + tile_x + tile_y - 1) % 9) + 1

            #print("appending (%d, %d) -> (%d, %d) (%d)" % (x, y, new_x, new_y, risk_value))
            # print("(%d, %d) mapping to (%d, %d), tile: (%d, %d) => %d" % (new_x, new_y, original_x, original_y, tile_x, tile_y, risk_value))
            edges.append(((x, y), (new_x, new_y), risk_value))

print(dijkstra(edges, (0, 0), (len(cave[0]) * growth_factor - 1, len(cave) * growth_factor - 1))[0])
