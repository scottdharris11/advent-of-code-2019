"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 1", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    fuel = 0
    for line in lines:
        fuel += req_fuel(int(line))
    return fuel

@runner("Day 1", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    fuel = 0
    for line in lines:
        fuel += module_fuel(int(line))
    return fuel

def req_fuel(mass: int) -> int:
    """calculate fuel for provided mass"""
    return int(mass/3) - 2

def module_fuel(mass: int) -> int:
    """calculate fuel for provided mass"""
    tf = req_fuel(mass)
    f = tf
    while True:
        f = req_fuel(f)
        if f <= 0:
            break
        tf += f
    return tf

# Data
data = read_lines("input/day01/input.txt")

# Part 1
assert req_fuel(12) == 2
assert req_fuel(14) == 2
assert req_fuel(1969) == 654
assert req_fuel(100756) == 33583
assert solve_part1(data) == 3256794

# Part 2
assert module_fuel(12) == 2
assert module_fuel(14) == 2
assert module_fuel(1969) == 966
assert module_fuel(100756) == 50346
assert solve_part2(data) == 4882337
