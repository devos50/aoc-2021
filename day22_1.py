from dataclasses import dataclass
from typing import Tuple

cubes = []


@dataclass
class Cube:
    state: bool
    lx: Tuple[int, int]
    ly: Tuple[int, int]
    lz: Tuple[int, int]

    @classmethod
    def get_line_intersection(cls, l1: Tuple[int, int], l2: Tuple[int, int]):
        left_endpoint = max(l1[0], l2[0])
        right_endpoint = min(l1[1], l2[1])
        if left_endpoint <= right_endpoint:
            return left_endpoint, right_endpoint
        return None

    def get_intersecting_cube(self, other_cube, new_state=None):
        int1 = Cube.get_line_intersection(self.lx, other_cube.lx)
        int2 = Cube.get_line_intersection(self.ly, other_cube.ly)
        int3 = Cube.get_line_intersection(self.lz, other_cube.lz)
        if not int1 or not int2 or not int3:
            return None

        return Cube(self.state if not new_state else new_state, int1, int2, int3)

    def get_volume(self):
        return (abs(self.lx[0] - self.lx[1]) + 1) * (abs(self.ly[0] - self.ly[1]) + 1) * (abs(self.lz[0] - self.lz[1]) + 1)


def partial_volume(cubes_list):
    intersecting_cubes = []
    for c in cubes_list[1:]:
        ic = c.get_intersecting_cube(cubes_list[0], new_state=True)
        if ic:
            intersecting_cubes.append(ic)
    return cubes_list[0].get_volume() - sum_volume(intersecting_cubes)


def sum_volume(cubes_list):
    tot = 0
    for ind, cube in enumerate(cubes_list):
        if not cube.state:
            continue
        tot += partial_volume(cubes_list[ind:])

    return tot


with open("data/day22.txt") as in_file:
    for line in in_file.readlines():
        parts = line.strip().split(" ")
        state = parts[0] == "on"
        parts = parts[1].split(",")
        p1 = parts[0][2:].split("..")
        p2 = parts[1][2:].split("..")
        p3 = parts[2][2:].split("..")

        cube = Cube(state, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), (int(p3[0]), int(p3[1])))
        big_cube = Cube(True, (-50, 50), (-50, 50), (-50, 50))
        if cube.get_intersecting_cube(big_cube):
            cubes.append(cube)

    # Compute area of all cubes that are on
    print(sum_volume(cubes))
