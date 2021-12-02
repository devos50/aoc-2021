raw_depths = []
window_depths = []

with open("data/day1.txt") as in_file:
    raw_depths = [int(i) for i in in_file.readlines()]

# Compute depths based
for ind in range(0, len(raw_depths) - 2):
    window_depths.append((raw_depths[ind] + raw_depths[ind + 1] + raw_depths[ind + 2]) / 3)

# Find number of increases in the aggregated depths
increases = 0
for ind in range(1, len(window_depths)):
    if window_depths[ind] > window_depths[ind - 1]:
        increases += 1

print(increases)
