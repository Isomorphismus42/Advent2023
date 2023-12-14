"""
--- Day 14: Parabolic Reflector Dish ---

You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish attached to the
side of another large mountain.

The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the shape of a parabolic
reflector dish, each individual mirror seems to be pointing in slightly the wrong direction. If the dish is meant to
focus light, all it's doing right now is sending it in a vague direction.

This system must be what provides the energy for the lava! If you focus the reflector dish, maybe you can go where
it's pointing and use the light to fix the lava production.

Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes and
pulleys to a large metal platform below the dish. The platform is covered in large rocks of various shapes. Depending
on their position, the weight of the rocks deforms the platform, and the shape of the platform controls which ropes
move and ultimately the focus of the dish.

In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets
you tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while the
cube-shaped rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks (your
puzzle input). For example:

O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....

Start by tilting the lever so all of the rocks will slide north as far as they will go:

OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....

You notice that the support beams along the north side of the platform are damaged; to ensure the platform doesn't
collapse, you should calculate the total load on the north support beams.

The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge
of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the amount
of load caused by each rock in each row is as follows:

OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1

The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.

Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support
beams?


------------------- Part Two --------------------

The parabolic reflector dish deforms, but not in a way that focuses the beam. To do that, you'll need to move the
rocks to the edges of the platform. Fortunately, a button on the side of the control panel labeled "spin cycle"
attempts to do just that!

Each cycle tilts the platform four times so that the rounded rocks roll north, then west, then south, then east.
After each tilt, the rounded rocks roll as far as they can before the platform tilts in the next direction. After one
cycle, the platform will have finished rolling the rounded rocks in those four directions in that order.

Here's what happens in the example above after each of the first few cycles:

After 1 cycle:
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....

After 2 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O

After 3 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O

This process should work if you leave it running long enough, but you're still worried about the north support beams.
To make sure they'll survive for a while, you need to calculate the total load on the north support beams after
1000000000 cycles.

In the above example, after 1000000000 cycles, the total load on the north support beams is 64.

Run the spin cycle for 1000000000 cycles. Afterward, what is the total load on the north support beams?

"""

import numpy as np
# import re
# from collections import OrderedDict
# import functools


def tilt_platform(platform):
    n = platform.shape[0]
    highest_obstacle_each_column = {j: -1 for j in range(platform.shape[1])}
    for i, row in enumerate(platform):
        for j, space in enumerate(row):
            if space == '#':
                highest_obstacle_each_column[j] = i
            elif space == 'O':
                next_obstacle = highest_obstacle_each_column[j]
                if next_obstacle == i - 1:
                    highest_obstacle_each_column[j] = i
                else:
                    platform[i, j] = '.'
                    highest_obstacle_each_column[j] += 1
                    platform[next_obstacle + 1, j] = 'O'
    return platform


def calculate_load(platform):
    return (platform == 'O') * (platform.shape[0] - np.indices(platform.shape)[0])


def part1():
    puzzle_input = open('inputs/input_day14', 'r').read().splitlines()
    tilted_platform_north = tilt_platform(np.array([list(line) for line in puzzle_input]))
    tilted_platform_north = calculate_load(np.array(tilted_platform_north))
    return np.sum(tilted_platform_north)


def part2():
    puzzle_input = open('inputs/input_day14', 'r').read().splitlines()
    platform = np.array([list(line) for line in puzzle_input])
    seen_configurations = list()
    period = 0
    np.set_printoptions(threshold=np.inf)
    for t in range(1000000000):
        for r in range(4):
            platform = tilt_platform(platform)
            platform = np.rot90(platform, axes=(1, 0))
        compare = np.array2string(platform, separator='').replace('\'', "")
        if compare in seen_configurations:
            steps = t + 1
            period = t - seen_configurations.index(compare)
            break
        seen_configurations.append(compare)
    if period:
        for t in range((1000000000 - steps) % period):
            for r in range(4):
                platform = tilt_platform(platform)
                platform = np.rot90(platform, axes=(1, 0))
    platform = calculate_load(platform)
    return np.sum(platform)


if __name__ == "__main__":
    print(part2())
