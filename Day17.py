"""
--- Day 17: Clumsy Crucible ---

The lava starts flowing rapidly once the Lava Production Facility is operational. As you leave, the reindeer offers
you a parachute, allowing you to quickly reach Gear Island.

As you descend, your bird's-eye view of Gear Island reveals why you had trouble finding anyone on your way up: half
of Gear Island is empty, but the half below you is a giant factory city!

You land near the gradually-filling pool of lava at the base of your new lavafall. Lavaducts will eventually carry
the lava throughout the city, but to make use of it immediately, Elves are loading it into large crucibles on wheels.

The crucibles are top-heavy and pushed by hand. Unfortunately, the crucibles become very difficult to steer at high
speeds, and so it can be hard to go in a straight line for very long.

To get Desert Island the machine parts it needs as soon as possible, you'll need to find the best way to get the
crucible from the lava pool to the machine parts factory. To do this, you need to minimize heat loss while choosing a
route that doesn't require the crucible to go in a straight line for too long.

Fortunately, the Elves here have a map (your puzzle input) that uses traffic patterns, ambient temperature,
and hundreds of other parameters to calculate exactly how much heat loss can be expected for a crucible entering any
particular city block.

For example:

2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533

Each city block is marked by a single digit that represents the amount of heat loss if the crucible enters that
block. The starting point, the lava pool, is the top-left city block; the destination, the machine parts factory,
is the bottom-right city block. (Because you already start in the top-left block, you don't incur that block's heat
loss unless you leave that block and then return to it.)

Because it is difficult to keep the top-heavy crucible going in a straight line for very long, it can move at most
three blocks in a single direction before it must turn 90 degrees left or right. The crucible also can't reverse
direction; after entering each city block, it may only turn left, continue straight, or turn right.

One way to minimize heat loss is this path:

2>>34^>>>1323
32v>>>35v5623
32552456v>>54
3446585845v52
4546657867v>6
14385987984v4
44578769877v6
36378779796v>
465496798688v
456467998645v
12246868655<v
25465488877v5
43226746555v>

This path never moves more than three consecutive blocks in the same direction and incurs a heat loss of only 102.

Directing the crucible from the lava pool to the machine parts factory, but not moving more than three consecutive
blocks in the same direction, what is the least heat loss it can incur?


------------------- Part Two --------------------



"""

import numpy as np
import heapq
# import re
# from collections import OrderedDict
# import functools

heat_map = open('inputs/input_day17', 'r').read().splitlines()
heat_map = np.array([list(line) for line in heat_map]).astype(int)


def calculate_heat(start_node, max_steps, min_steps=0):
    start_node = (*start_node, 's' * max_steps)
    queue = [start_node]
    seen = set()
    m, n = heat_map.shape[0] - 1, heat_map.shape[1] - 1
    while queue:
        distance, x, y, last_steps = heapq.heappop(queue)
        if (x, y) == (m, n) and last_steps[-min_steps:] in {c * min_steps for c in 'udlr'}:
            return distance
        if x > 0 and (x - 1, y, last_steps[1:] + 'u') not in seen:
            if last_steps + 'u' != 'u' * (max_steps + 1) and last_steps[-1] != 'd':
                if not min_steps or last_steps[-min_steps:] in {c * min_steps for c in 'lrs'} or last_steps[-1] == 'u':
                    heapq.heappush(queue, (distance + heat_map[x - 1, y], x - 1, y, last_steps[1:] + 'u'))
                    seen.add((x - 1, y, last_steps[1:] + 'u'))
        if x < m and (x + 1, y, last_steps[1:] + 'd') not in seen:
            if last_steps + 'd' != 'd' * (max_steps + 1) and last_steps[-1] != 'u':
                if not min_steps or last_steps[-min_steps:] in {c * min_steps for c in 'lrs'} or last_steps[-1] == 'd':
                    heapq.heappush(queue, (distance + heat_map[x + 1, y], x + 1, y, last_steps[1:] + 'd'))
                    seen.add((x + 1, y, last_steps[1:] + 'd'))
        if y > 0 and (x, y - 1, last_steps[1:] + 'l') not in seen:
            if last_steps + 'l' != 'l' * (max_steps + 1) and last_steps[-1] != 'r':
                if not min_steps or last_steps[-min_steps:] in {c * min_steps for c in 'dus'} or last_steps[-1] == 'l':
                    heapq.heappush(queue, (distance + heat_map[x, y - 1], x, y - 1, last_steps[1:] + 'l'))
                    seen.add((x, y - 1, last_steps[1:] + 'l'))
        if y < n and (x, y + 1, last_steps[1:] + 'r') not in seen:
            if last_steps + 'r' != 'r' * (max_steps + 1) and last_steps[-1] != 'l':
                if not min_steps or last_steps[-min_steps:] in {c * min_steps for c in 'dus'} or last_steps[-1] == 'r':
                    heapq.heappush(queue, (distance + heat_map[x, y + 1], x, y + 1, last_steps[1:] + 'r'))
                    seen.add((x, y + 1, last_steps[1:] + 'r'))


def part1():
    heat = calculate_heat((0, 0, 0), 3)
    return heat


def part2():
    heat = calculate_heat((0, 0, 0), 10, 4)
    return heat


if __name__ == "__main__":
    print(part2())
