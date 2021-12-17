#target_area = ((20, 30), (-10, -5))
target_area = ((135, 155), (-102, -78))
x_possibilities = set()

for start_velocity in range(1, target_area[0][1] + 1):
    for end_velocity in range(start_velocity, -1, -1):
        s = sum(range(end_velocity+1, start_velocity+1))
        if s >= target_area[0][0] and s <= target_area[0][1]:
            print("Possible: X = %d with steps %d" % (start_velocity, (start_velocity - end_velocity)))
            open_interval = False
            if end_velocity == 0:
                open_interval = True

            x_possibilities.add((start_velocity, start_velocity - end_velocity, open_interval))

# For each possibility, consider Y values
largest_y_start = -10000000
for start_x_velocity, max_steps, open_interval in x_possibilities:
    additional_steps_range = range(0, 1) if not open_interval else range(1, 300)
    for start_y_velocity in range(1, 200):  # Only consider positive Y values
        for additional_steps in additional_steps_range:
            final_y = sum(range(start_y_velocity, (start_y_velocity - max_steps - additional_steps), -1))
            if final_y >= target_area[1][0] and final_y <= target_area[1][1]:
                print("Will reach target area with X = %d, Y = %d in %d steps" % (start_x_velocity, start_y_velocity, max_steps))
                if start_y_velocity > largest_y_start:
                    largest_y_start = start_y_velocity

print(largest_y_start)
print(sum(range(1, largest_y_start + 1)))
