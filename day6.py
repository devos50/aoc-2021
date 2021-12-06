days = [0] * 9

with open("data/day6.txt") as in_file:
    fishes_days = [int(t) for t in in_file.read().strip().split(",")]
    for d in fishes_days:
        days[d] += 1

cur_day = 0
while True:
    if cur_day == 256:
        break

    day0_fishes = days.pop(0)
    days[6] += day0_fishes
    days.append(day0_fishes)
    cur_day += 1

print(sum(days))
