"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 24", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    bugs = parse_input(lines)
    previous = set()
    previous.add(frozenset(bugs))
    while True:
        bugs = next_bug_state(bugs)
        state = frozenset(bugs)
        if state in previous:
            break
        previous.add(state)
    return biodiversity(bugs)

@runner("Day 24", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    return 0

def biodiversity(bugs: set[tuple[int,int]]) -> int:
    """calcluate the biodiversity of the bug state"""
    rating = 0
    for y in range(5):
        for x in range(5):
            if (x,y) in bugs:
                p = (y * 5) + x
                rating += pow(2, p)
    return rating

def next_bug_state(bugs: set[tuple[int,int]]) -> set[tuple[int,int]]:
    """determine next bug state from current"""
    nbugs = set()
    for y in range(5):
        for x in range(5):
            adjancent = 0
            for moves in [(0,-1),(1,0),(0,1),(-1,0)]:
                ax = x + moves[0]
                ay = y + moves[1]
                if ax < 0 or ay < 0 or ax == 5 or ay == 5:
                    continue
                if (ax,ay) in bugs:
                    adjancent += 1
            if (x,y) in bugs:
                if adjancent == 1:
                    nbugs.add((x,y))
            else:
                if adjancent == 1 or adjancent == 2:
                    nbugs.add((x,y))
    return nbugs

def parse_input(lines: list[str]) -> set[tuple[int,int]]:
    """parse input for problem"""
    bugs = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                bugs.add((x,y))
    return bugs

# Data
data = read_lines("input/day24/input.txt")
sample = """....#
#..#.
#..##
..#..
#....""".splitlines()

# Part 1
assert solve_part1(sample) == 2129920
assert solve_part1(data) == 18371095

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
