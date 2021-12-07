from numpy import average

distances = []

with open("data/day7.txt") as in_file:
    distances = [int(n) for n in in_file.read().strip().split(",")]

distances = sorted(distances)
#avg = average(distances)
avg = 489

fuel_req = 0
for d in distances:
    steps = abs(d - avg)
    fuel_req += (steps / 2) * (1 + steps)

print(int(fuel_req))
