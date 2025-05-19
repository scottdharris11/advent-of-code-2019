"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 6", "Part 1")
def solve_part1(line: str):
    """part 1 solving function"""
    return 0

@runner("Day 6", "Part 2")
def solve_part2(line: str):
    """part 2 solving function"""
    return 0

# Data
data = read_lines("input/day06/input.txt")
sample = """""".splitlines()

# Part 1
assert solve_part1(sample) == 0
assert solve_part1(data) == 0

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
