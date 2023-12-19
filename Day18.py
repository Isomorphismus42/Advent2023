"""
--- Day 18: Lavaduct Lagoon ---

Thanks to your efforts, the machine parts factory is one of the first factories up and running since the lavafall
came back. However, to catch up with the large backlog of parts requests, the factory will also need a large supply
of lava for a while; the Elves have already started creating a large lagoon nearby for this purpose.

However, they aren't sure the lagoon will be big enough; they've asked you to take a look at the dig plan (your
puzzle input). For example:

R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)

The digger starts in a 1 meter cube hole in the ground. They then dig the specified number of meters up (U),
down (D), left (L), or right (R), clearing full 1 meter cubes as they go. The directions are given as seen from
above, so if "up" were north, then "right" would be east, and so on. Each trench is also listed with the color that
the edge of the trench should be painted as an RGB hexadecimal color code.

When viewed from above, the above example dig plan would result in the following loop of trench (#) having been dug
out from otherwise ground-level terrain (.):

#######
#.....#
###...#
..#...#
..#...#
###.###
#...#..
##..###
.#....#
.######

At this point, the trench could contain 38 cubic meters of lava. However, this is just the edge of the lagoon; the
next step is to dig out the interior so that it is one meter deep as well:

#######
#######
#######
..#####
..#####
#######
#####..
#######
.######
.######

Now, the lagoon can contain a much more respectable 62 cubic meters of lava. While the interior is dug out,
the edges are also painted according to the color codes in the dig plan.

The Elves are concerned the lagoon won't be large enough; if they follow their dig plan, how many cubic meters of
lava could it hold?


------------------- Part Two --------------------

The Elves were right to be concerned; the planned lagoon would be much too small.

After a few minutes, someone realizes what happened; someone swapped the color and instruction parameters when
producing the dig plan. They don't have time to fix the bug; one of them asks if you can extract the correct
instructions from the hexadecimal codes.

Each hexadecimal code is six hexadecimal digits long. The first five hexadecimal digits encode the distance in meters
as a five-digit hexadecimal number. The last hexadecimal digit encodes the direction to dig: 0 means R, 1 means D,
2 means L, and 3 means U.

So, in the above example, the hexadecimal codes can be converted into the true instructions:

    #70c710 = R 461937
    #0dc571 = D 56407
    #5713f0 = R 356671
    #d2c081 = D 863240
    #59c680 = R 367720
    #411b91 = D 266681
    #8ceee2 = L 577262
    #caa173 = U 829975
    #1b58a2 = L 112010
    #caa171 = D 829975
    #7807d2 = L 491645
    #a77fa3 = U 686074
    #015232 = L 5411
    #7a21e3 = U 500254

Digging out this loop and its interior produces a lagoon that can hold an impressive 952408144115 cubic meters of lava.

Convert the hexadecimal color codes into the correct instructions; if the Elves follow this new dig plan,
how many cubic meters of lava could the lagoon hold?

"""

import numpy as np
# import heapq
# import re
# from collections import OrderedDict
# import functools
from shapely.geometry import Polygon

dig_plan = open('inputs/input_day18', 'r').read().splitlines()
dig_plan = [line.split(' ') for line in dig_plan]


def create_vertex_list(instructions):
    vertices = list()
    last_vertex = [1, 1]
    border_tiles = 0
    for line in instructions:
        x, y = last_vertex
        distance = int(line[1])
        border_tiles += distance
        instruction = line[0]
        if instruction == 'R':
            new_vertex = (x, y + distance)
        elif instruction == 'L':
            new_vertex = (x, y - distance)
        elif instruction == 'D':
            new_vertex = (x + distance, y)
        elif instruction == 'U':
            new_vertex = (x - distance, y)
        vertices.append(new_vertex)
        last_vertex = new_vertex
    return vertices, border_tiles


def part1():
    vertices, border_tiles = create_vertex_list([[line[0], line[1]] for line in dig_plan])
    polygon = Polygon(vertices)
    return int(polygon.area + border_tiles // 2 + 1)


def part2():
    instructions = list()
    for _, _, code in dig_plan:
        steps = int(code[2:7], 16)
        if code[7] == '0':
            direction = 'R'
        elif code[7] == '1':
            direction = 'D'
        elif code[7] == '2':
            direction = 'L'
        else:
            direction = 'U'
        instructions.append([direction, steps])
    vertices, border_tiles = create_vertex_list(instructions)
    polygon = Polygon(vertices)
    return int(polygon.area + border_tiles // 2 + 1)

    # Gaußsche Trapezformel
    # vertices = vertices[::-1]
    # area = 0
    # for i in range(len(vertices) - 1):
    #     area += (vertices[i][0] - vertices[i + 1][0]) * (vertices[i][1] + vertices[i + 1][1])
    # else:
    #     area += (vertices[-1][0] - vertices[0][0]) * (vertices[-1][1] + vertices[0][1])
    # return area//2 + border_tiles // 2 + 1


if __name__ == "__main__":
    print(part2())
