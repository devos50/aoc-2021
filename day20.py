enhance_algo = None
pixels = {}
left_top = (-1, -1)
right_bottom = (0, 0)
background_color = False  # start with dark


def get_pixel(x, y):
    if x < left_top[0] or x > right_bottom[0] or y < left_top[1] or y > right_bottom[1]:
        return background_color
    if (x, y) in pixels:
        return pixels[(x, y)]
    return False


def print_img():
    for y in range(left_top[1], right_bottom[1] + 1):
        pixstr = ""
        for x in range(left_top[0], right_bottom[0] + 1):
            pixstr += '#' if get_pixel(x, y) else '.'
        print("%s" % pixstr)


with open("data/day20.txt") as in_file:
    content = in_file.read()
    parts = content.split("\n\n")
    enhance_algo = parts[0]
    initial_picture = parts[1]
    y = 0
    lines = initial_picture.split("\n")
    right_bottom = (len(lines[0]), len(lines))
    for line in lines:
        x = 0
        for char in line.strip():
            if char == "#":
                pixels[(x, y)] = True
            x += 1
        y += 1


print(enhance_algo)
print(pixels)
print(right_bottom)
print_img()

for step in range(50):
    print("PERFORMING STEP")
    new_pixels = {}
    for y in range(left_top[1], right_bottom[1] + 1):
        for x in range(left_top[0], right_bottom[0] + 1):
            # Determine new pixel
            binnum = ""
            for grid_y in range(y - 1, y + 2):
                for grid_x in range(x - 1, x + 2):
                    binnum += "1" if get_pixel(grid_x, grid_y) else "0"

            new_pixel = enhance_algo[int(binnum, 2)]
            if new_pixel == '#':
                new_pixels[(x, y)] = True

    # Update the background color if we have to
    if not background_color and enhance_algo[0] == '#':
        background_color = True
    elif background_color and enhance_algo[-1] == '.':
        background_color = False

    # Grow image and repaint
    for x in range(left_top[0] - 1, right_bottom[0] + 2):
        new_pixels[(x, left_top[1] - 1)] = background_color
        new_pixels[(x, right_bottom[1] + 1)] = background_color
    for y in range(left_top[1] - 1, right_bottom[1] + 2):
        new_pixels[(left_top[0] - 1, y)] = background_color
        new_pixels[(right_bottom[0] + 1, y)] = background_color

    left_top = (left_top[0] - 1, left_top[1] - 1)
    right_bottom = (right_bottom[0] + 1, right_bottom[1] + 1)
    pixels = new_pixels
    print(pixels)

    print("After step %d: " % step)
    print_img()

num = 0
for val in pixels.values():
    if val:
        num += 1

print(num)