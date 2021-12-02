hor_pos = 0
depth = 0
aim = 0

with open("data/day2.txt") as in_file:
    for line in in_file.readlines():
        parts = line.strip().split(" ")
        if parts[0] == "forward":
            hor_pos += int(parts[1])
            depth += int(parts[1]) * aim
        elif parts[0] == "down":
            aim += int(parts[1])
        elif parts[0] == "up":
            aim -= int(parts[1])
print(hor_pos * depth)