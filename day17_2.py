#target_area = ((20, 30), (-10, -5))
target_area = ((135, 155), (-102, -78))
x_possibilities = set()
x_y_possibilities = set()

for start_velocity in range(1, target_area[0][1] + 1):
    for end_velocity in range(start_velocity, -1, -1):
        s = sum(range(end_velocity+1, start_velocity+1))
        if s >= target_area[0][0] and s <= target_area[0][1]:
            # print("Possible: X = %d with steps %d" % (start_velocity, (start_velocity - end_velocity)))
            open_interval = False
            if end_velocity == 0:
                open_interval = True

            x_possibilities.add((start_velocity, start_velocity - end_velocity, open_interval))

# For each possibility, consider Y values
for start_x_velocity, max_steps, open_interval in x_possibilities:
    additional_steps_range = range(0, 1) if not open_interval else range(0, 200)
    for start_y_velocity in range(-300, 300):
        for additional_steps in additional_steps_range:
            r = range(start_y_velocity, (start_y_velocity - max_steps - additional_steps), -1)
            # print("Considering (%d, %d) => %s" % (start_x_velocity, start_y_velocity, list(r)))
            final_y = sum(r)
            if final_y >= target_area[1][0] and final_y <= target_area[1][1]:
                print("Will reach target area with X = %d, Y = %d in %d steps" % (start_x_velocity, start_y_velocity, max_steps))
                x_y_possibilities.add((start_x_velocity, start_y_velocity))

print(len(x_y_possibilities))
#print(x_y_possibilities)

# sets = """
# 23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
# 25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
# 8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
# 26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
# 20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
# 25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
# 25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
# 8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
# 24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
# 7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
# 23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
# 27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
# 8,-2    27,-8   30,-5   24,-7"""
# nums = [n.split(",") for n in " ".join(sets.split("\n")).split(" ") if n.strip()]
# for num in nums:
#     if((int(num[0]), int(num[1]))) not in x_y_possibilities:
#         print(num)
