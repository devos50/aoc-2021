from dataclasses import dataclass
from enum import Enum


class Orientation(Enum):
    HOR = 0
    VER = 1
    DIAG = 2


@dataclass
class Point:
    x: int = 0
    y: int = 0

    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)


@dataclass
class Segment:
    start: Point = None
    end: Point = None
    orientation: Orientation = None

    def determine_orientation(self):
        if segment.start.y == segment.end.y:
            self.orientation = Orientation.HOR
        elif segment.start.x == segment.end.x:
            self.orientation = Orientation.VER
        else:
            self.orientation = Orientation.DIAG

    def __str__(self):
        return "%s -> %s" % (self.start, self.end)


segments = []
field = []
intersects = set()

max_x = 0
max_y = 0


with open("data/day5.txt") as in_file:
    for line in in_file.readlines():
        parts = line.split(" -> ")
        start_raw = parts[0].split(",")
        end_raw = parts[1].split(",")
        start = Point(int(start_raw[0]), int(start_raw[1]))
        end = Point(int(end_raw[0]), int(end_raw[1]))

        # Only consider horizontal/vertical lines
        # if (start.x != end.x) and (start.y != end.y):
        #     continue

        max_x = max(max_x, start.x)
        max_y = max(max_y, start.y)
        max_x = max(max_x, end.x)
        max_y = max(max_y, end.y)

        segment = Segment(start, end)
        segment.determine_orientation()
        segments.append(segment)

for cur_y in range(max_y + 1):
    arr = [0] * (max_x + 1)
    field.append(arr)

for segment in segments:
    if segment.orientation == Orientation.HOR:
        for cur_x in range(min(segment.start.x, segment.end.x), max(segment.start.x, segment.end.x) + 1):
            field[segment.start.y][cur_x] += 1
            if field[segment.start.y][cur_x] > 1:
                intersects.add((cur_x, segment.start.y))
    elif segment.orientation == Orientation.VER:
        for cur_y in range(min(segment.end.y, segment.start.y), max(segment.end.y, segment.start.y) + 1):
            field[cur_y][segment.start.x] += 1
            if field[cur_y][segment.start.x] > 1:
                intersects.add((segment.start.x, cur_y))
    else:
        # determine if we should go up or left
        go_down = (segment.end.y > segment.start.y)
        go_right = (segment.end.x > segment.start.x)
        steps = abs(segment.start.x - segment.end.x) + 1
        for step in range(steps):
            new_y = (segment.start.y + step) if go_down else (segment.start.y - step)
            new_x = (segment.start.x + step) if go_right else (segment.start.x - step)
            field[new_y][new_x] += 1
            if field[new_y][new_x] > 1:
                intersects.add((new_x, new_y))

print(len(intersects))
