"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 3", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    w1, _ = follow_wire(lines[0].split(","))
    w2, _ = follow_wire(lines[1].split(","))
    nearest = 0
    for l in w2:
        if l in w1:
            dist = abs(l[0]) + abs(l[1])
            if nearest == 0 or dist < nearest:
                nearest = dist
    return nearest

@runner("Day 3", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    w1, wp1 = follow_wire(lines[0].split(","))
    w2, wp2 = follow_wire(lines[1].split(","))
    nearest = 0
    for l in w2:
        if l in w1:
            wp1.index(l)
            dist = wp1.index(l) + wp2.index(l)
            if nearest == 0 or dist < nearest:
                nearest = dist
    return nearest

directions = {'R':(1,0), 'L':(-1,0), 'D':(0,1), 'U':(0,-1)}

def follow_wire(instructions: list[str]) -> tuple[set[tuple[int,int]],list[tuple[int,int]]]:
    """follow wire path to determine locations"""
    locations = set()
    path = list()
    loc = (0,0)
    path.append(loc)
    for i in instructions:
        adjust = directions[i[0]]
        steps = int(i[1:])
        for _ in range(steps):
            loc = (loc[0]+adjust[0], loc[1]+adjust[1])
            path.append(loc)
            locations.add(loc)
    return (locations, path)

# Data
data = read_lines("input/day03/input.txt")
sample = """R8,U5,L5,D3
U7,R6,D4,L4""".splitlines()

# Part 1
assert solve_part1(sample) == 6
assert solve_part1(data) == 1626

# Part 2
assert solve_part2(sample) == 30
assert solve_part2(data) == 27330
